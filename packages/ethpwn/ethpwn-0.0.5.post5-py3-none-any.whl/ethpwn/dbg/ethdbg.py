#!/usr/bin/env python3

import argparse
import functools
import os
import re
import sys
import cmd
import traceback

from hexdump import hexdump
from typing import List
from alive_progress import alive_bar

from hexbytes import HexBytes
from web3.datastructures import AttributeDict
from pyevmasm import disassemble_one, Instruction

import rich
from rich import print as rich_print
from rich.table import Table
from rich.tree import Tree

from eth_utils import keccak

from functools import wraps

from ethpwn.ethlib.config.misc import get_default_node_url, get_default_network


from ..ethlib.prelude import *
from ..ethlib.evm.analyzer import *
from ..ethlib.utils import normalize_contract_address
from ..ethlib.config.wallets import get_wallet
from ..ethlib.config.dbg import DebugConfig
from ..ethlib.config import get_default_global_config_path
from ..ethlib.assembly_utils import disassemble_all
from ..ethlib.evm.txn_condom import TransactionCondom

from .breakpoint import Breakpoint, ETH_ADDRESS
from .utils import *
from .ethdbg_exceptions import ExitCmdException, InvalidBreakpointException, RestartDbgException, InvalidTargetException

from eth_utils.curried import to_canonical_address

FETCHED_VERIFIED_CONTRACTS = set()

def get_contract_for(contract_address: HexBytes):
    global FETCHED_VERIFIED_CONTRACTS
    contract_address = normalize_contract_address(contract_address)
    registry = contract_registry()


    if contract_address not in FETCHED_VERIFIED_CONTRACTS and registry.get(contract_address) is None:
        # try to fetch the verified contract
        try:
            fetch_verified_contract(contract_address, None) # auto-detect etherscan api key and fetch the code
        except Exception as ex:
            # print traceback
            #traceback.print_exc()
            print(f"Failed to fetch verified source code for {contract_address}: {ex}")
        FETCHED_VERIFIED_CONTRACTS.add(contract_address)

    return registry.get(contract_address)


def get_source_code_view_for_pc(debug_target: TransactionCondom, contract_address: HexBytes, pc: int=None):
    contract = get_contract_for(contract_address)
    if contract is None:
        return None

    if contract_address == 'None' or int.from_bytes(HexBytes(contract_address), byteorder='big') == 0:
        closest_instruction_idx = contract.metadata.closest_instruction_index_for_constructor_pc(pc, fork=debug_target.fork)
        source_info = contract.metadata.source_info_for_constructor_instruction_idx(closest_instruction_idx)
    else:
        closest_instruction_idx = contract.metadata.closest_instruction_index_for_runtime_pc(pc, fork=debug_target.fork)
        source_info = contract.metadata.source_info_for_runtime_instruction_idx(closest_instruction_idx)
    if source_info is None:
        return None
    return source_info.pretty_print_source(context_lines=3)


def read_storage_typed_value(read_storage, storage_layout, storage_value):

    storage_type = storage_layout['types'][storage_value['type']]

    # read_storage = function taking a slot and returning a value
    if storage_type['encoding'] == 'inplace':
        if int(storage_type['numberOfBytes']) > 32:
            import ipdb; ipdb.set_trace()
            # assert False, "Don't know how to handle this yet"
            return "<UNSUPPORTED STORAGE TYPE>"
        value = read_storage(int(storage_value['slot']))
        # lower-order-alignment means it's easier to flip it, index, flip it back
        value = value[::-1]
        value = value[int(storage_value['offset']):int(storage_value['offset']) + int(storage_type['numberOfBytes'])]
        value = value[::-1]
        # TODO format it out of the bytes based on the label?
        if storage_type['label'].split()[0] == 'address' or storage_type['label'].split()[0] == 'contract':
            # so far seen: "address", "address payable", "contract <name>"
            return HexBytes(value).hex()
        elif re.fullmatch('uint[0-9]+', storage_type['label']):
            num_bits = int(storage_type['label'][4:])
            assert num_bits % 8 == 0
            num_bytes = num_bits // 8
            assert len(value) == num_bytes
            assert storage_type['numberOfBytes'] == str(num_bytes)
            return int.from_bytes(value, byteorder='big')
        elif storage_type['label'] == 'bool':
            assert len(value) == 1
            assert storage_type['numberOfBytes'] == '1'
            return int.from_bytes(value, byteorder='big') != 0
        elif re.match('bytes[0-9]+', storage_type['label']):
            if int(storage_type['label'][5:]) > 32:
                import ipdb; ipdb.set_trace()
                assert False, "Don't know how to handle this yet"
            assert len(value) <= 32
            assert int(storage_type['numberOfBytes']) <= 32
            return value
        else:
            import ipdb; ipdb.set_trace()
            # assert False, "Don't know how to handle this yet"
            return "<UNSUPPORTED STORAGE TYPE>"
        return HexBytes(value)

    elif storage_type['encoding'] == 'mapping':

        # TODO implement and print this:
        '''
        The value corresponding to a mapping key k is located at keccak256(h(k) . p) where . is concatenation and h is a function that is applied to the key depending on its type:

        for value types, h pads the value to 32 bytes in the same way as when storing the value in memory.

        for strings and byte arrays, h(k) is just the unpadded data.

        '''
        slot = int(storage_value['slot'])
        return None

    elif storage_type['encoding'] == 'dynamic_array':
        num_elements = read_storage(int(storage_value['slot']))
        num_elements = int.from_bytes(num_elements, byteorder='big')
        element_type = storage_layout['types'][storage_type['base']]
        element_size = int(element_type['numberOfBytes'])
        num_slots = (num_elements * element_size + 31) // 32
        slot_start = int.from_bytes(keccak(int.to_bytes(int(storage_value['slot']), 32, byteorder='big')), byteorder='big')
        # TODO: Lukas: decode nicer
        slots = [HexBytes(read_storage(slot_start + i))[-element_size:] for i in range(num_slots)]
        return {
            'data_start_slot': slot_start,
            'num_elements': num_elements,
            'element_type': element_type,
            'slots': slots,
        }

    elif storage_type['encoding'] == 'bytes':
        slot = read_storage(int(storage_value['slot']))

        if slot[-1] & 1 == 0:
            length = slot[-1] // 2
            assert length <= 31
            data_read = HexBytes(slot[:length]) # inplace bytes, less than 32 bytes in length
        else:
            length = int.from_bytes(slot, byteorder='big') // 2
            num_slots = (length + 31) // 32
            slots = [read_storage(int(storage_value['slot']) + i) for i in range(num_slots)]
            data_read = HexBytes(b''.join(slots))
        if storage_type['label'] == 'string':
            data_read = data_read.decode('utf-8')
        else:
            assert storage_type['label'] == 'bytes'
        return data_read

    else:
        raise Exception(f'Unknown storage encoding {storage_type["encoding"]}')


def _get_storage_layout_table_for(read_storage, title, storage_layout, contract_address=None):
    if title is None:
        if contract_address is None:
            title = "Storage layout"
        else:
            title = f"Storage layout for {contract_address}"
    table = Table(title=title, show_header=True, header_style="bold magenta")
    table.add_column("Name")
    table.add_column("Type", style='dim')
    table.add_column("Slot", style='dim')
    table.add_column("Offset", style='dim')
    table.add_column("Value")
    table.add_column("Contract")

    for storage_value in sorted(storage_layout['storage'], key=lambda x: int(x['slot'])):
        type = storage_value['type']
        value = read_storage_typed_value(read_storage, storage_layout, storage_value)
        table.add_row(
            storage_value['label'],
            storage_layout['types'][type]['label'],
            str(int(storage_value['slot'])),
            str(int(storage_value['offset'])),
            repr(value),
            os.path.basename(storage_value['contract']),
        )
    return table

def get_storage_layout_table_for(read_storage, contract_address: HexBytes):
    contract_address = normalize_contract_address(contract_address)
    registry = contract_registry()
    contract = registry.get(contract_address)
    if contract is None:
        return None
    storage_layout = contract.metadata.storage_layout
    if storage_layout is None:
        return None
    return _get_storage_layout_table_for(read_storage, f"Storage layout as interpreted by {contract_address}", storage_layout, contract_address)

def get_storage_layout_table(read_storage, code_contract_address, storage_contract_address):
    table_code: Table = get_storage_layout_table_for(read_storage, code_contract_address)
    if code_contract_address == storage_contract_address:
        return table_code
    table_storage: Table = get_storage_layout_table_for(read_storage, storage_contract_address)
    if table_code is None and table_storage is None:
        return None
    if table_code is None:
        return table_storage
    if table_storage is None:
        return table_code

    table = Table(title="Storage layout", show_header=True, header_style="bold magenta")
    table.add_column("Contract")
    table.add_column("Storage")
    table.add_row('Code', table_code)
    table.add_row('Storage', table_storage)
    return table

def get_config(wallet_id):
    # Parse file using ConfigParser
    return get_wallet(wallet_id)

class CallFrame():
    def __init__(self, address, msg_sender, tx_origin, value, calltype, callsite):
        # Initialize attributes with args
        self.address = address
        self.msg_sender = msg_sender
        self.tx_origin = tx_origin
        self.value = value
        self.calltype = calltype
        self.callsite = callsite

# Save the original implementation of the function that extracts the message sender
ORIGINAL_extract_transaction_sender = eth._utils.transactions.extract_transaction_sender

class EthDbgShell(cmd.Cmd):

    prompt = f'\001\033[1;31m\002ethdbg➤\001\033[0m\002 '

    def __init__(self, wallet_conf, debug_target, breaks=None, **kwargs):
        # call the parent class constructor
        super().__init__(**kwargs)

        # The config for ethdbg
        self.tty_rows, self.tty_columns = get_terminal_size()
        self.wallet_conf = wallet_conf
        self.account = Account.from_key(self.wallet_conf.private_key)

        self.show_opcodes_desc = DebugConfig.show_opcodes_desc

        # EVM stuff
        self.w3 = context.w3

        self.debug_target: TransactionCondom = debug_target
        self.debug_target.set_defaults(
            gas=6_000_000, # silly default value
            gas_price=(10 ** 9) * 1000,
            value=0,
            calldata='',
            to='0x0',
            origin=self.debug_target.source_address,
            sender=self.debug_target.source_address,
 nonce=self.w3.eth.get_transaction_count(self.debug_target.source_address),
        )

        # The *CALL trace between contracts
        self.callstack = []

        if self.debug_target._target_address is not None:
            self.root_tree_node =  Tree(self.debug_target._target_address)
        else:
            self.root_tree_node =  Tree("0x0")

        self.curr_tree_node = self.root_tree_node
        self.list_tree_nodes = [self.curr_tree_node]

        # Recording here the SSTOREs, the dictionary is organized
        # per account so we can keep track of what storages slots have
        # been modified for every single contract that the transaction touched
        self.sstores = {}
        self.hide_sstores = DebugConfig.hide_sstores
        # Recording here the SLOADs, the dictionary is organized
        # per account so we can keep track of what storages slots have
        # been modified for every single contract that the transaction touched
        self.sloads = {}
        self.hide_sloads = DebugConfig.hide_sloads

        # list of logs emitted by the transaction
        self.logs = []

        self.context_layout = DebugConfig.context_layout
        self.source_view_cutoff = DebugConfig.source_view_cutoff

        # Debugger state
        # ==============
        #  Whether the debugger is running or not
        self.started = False
        #  Breakpoints PCs
        self.breakpoints: List[Breakpoint] = breaks if breaks else list()

        # Used for finish command
        self.temp_break_finish = False
        self.finish_curr_stack_depth = None

        #  History of executed opcodes
        self.history = list()
        #  The computation object of py-evm
        self.comp = None
        #  The name of the fork we are using
        self.vm_fork_name = ''
        # The current opcode
        self.curr_opcode = None
        #  Used for step command
        self.temp_break = False
        #  Whether we want to display the execute ops
        self.log_op = False
        # Whether we want to stop on RETURN/STOP operations
        self.stop_on_returns = DebugConfig.stop_on_returns
        self.stop_on_reverts = DebugConfig.stop_on_reverts
        # List of addresses of contracts that reverted
        self.reverted_contracts = set()

        self.tx_start_gas = None

    def precmd(self, line):
        # Check if the command is valid, if yes, we save it
        if line != None and line != '' and "do_" + line.split(' ')[0] in [c for c in self.get_names() if "do" in c]:
            save_cmds_history(line)
        return line

    # === DECORATORS ===
    def only_when_started(func):
        @wraps(func)
        def wrapper(self, *args, **kwargs):
            if self.started:
                return func(self, *args, **kwargs)
            else:
                print("You need to start the debugger first. Use 'start' command")
        return wrapper

    # === COMMANDS ===
    def do_chain(self, arg):
        '''
        Print the current chain context
        Usage: chain
        '''
        print(f'{self.debug_target.chain}@{self.debug_target.block_number!r}:{self.w3.provider.endpoint_uri}')

    def do_options(self, arg):
        '''
        Print the options of the debugger
        Usage: options
        '''
        print(f'chain: {self.debug_target.chain}@{self.debug_target.block_number!r}')
        print(f'w3-endpoint: {self.w3.provider.endpoint_uri}')
        print(f'full-context: {self.debug_target.full_context}')
        print(f'log_ops: {self.log_op}')
        print(f'stop_on_returns: {self.stop_on_returns}')
        print(f'stop_on_reverts: {self.stop_on_reverts}')
        print(f'hide_sstores: {self.hide_sstores}')
        print(f'hide_sloads: {self.hide_sloads}')
        print(f'context-layout: {self.context_layout}')


    def do_block(self, arg):
        '''
        Set the block number for this tx (if not started)
        Get the block number for this tx (if started)
        '''
        if arg and not self.started:
            self.debug_target.block_number = int(arg,10)
        print(f'{self.debug_target.block_number}')

    def do_account(self, arg):
        '''
        Get the account sender for this tx (if started)
        Usage: account
        '''
        if self.debug_target.debug_type == "replay":
            print(f'{self.debug_target.source_address} (impersonating)')
        else:
            print(f'{self.debug_target.source_address}')

    def do_target(self, arg):
        '''
        Set the target for this tx (if not started)
        Get the target for this tx (if started)
        Usage: target [<address>]
        '''
        if arg and not self.started:
            self.debug_target.target_address = arg
        else:
            print(f'{self.debug_target.target_address}')

    def do_hextostr(self, arg):
        '''
        Convert a hex string to a string if possible
        Usage: hextostr <hex_number>
        '''
        try:
            print(f'"{HexBytes(arg).decode("utf-8")}"')
        except Exception:
            print(f'Invalid hex string')

    def do_guessfuncid(self, arg):
        '''
        Given a function signature, try to fetch the function name
        from 4bytes.directory
        Usage: guessfuncid <function_signature>
        '''
        try:
            res = decode_function_input(None, arg, guess=True)
            if res is None:
                print(f'Could not retrieve function signature :(')
                return
            _contract, _metadata, _decoded_func = res
            sig, args = _decoded_func
            print(f" → {sig}({', '.join(map(repr,args))})")
        except Exception as e:
            print(f'Could not retrieve function signature :(')
            print(f'{RED_COLOR}{e}{RESET_COLOR}')

    do_guess = do_guessfuncid

    def do_funcid(self, arg):
        '''
        Calculate the function id for a given function name
        Usage: funcid <function_name>
        '''
        arg = arg.encode('utf-8')
        funcid = keccak(arg).hex()[0:8]
        print("Function signature: 0x{}".format(funcid))

    def do_value(self, arg):
        '''
        Set the amount of value sent for this tx (if not started)
        Get the amount of value sent for this tx (if started)
        Usage: value
        '''
        if arg and not self.started:
            self.debug_target.value = int(arg,10)
        else:
            print(f'{self.debug_target.value}')

    def do_gas(self, arg):
        '''
        Set the amount of gas sent for this tx (if not started)
        Get the amount of gas sent for this tx (if started)
        Usage: gas
        '''
        if arg and not self.started:
            self.debug_target.gas = int(arg,10)
        else:
            print(f'{self.debug_target.gas} wei')

    def do_start(self, arg):
        '''
        Start the execution of the EVM
        '''
        if self.started:
            answer = input("Debugger already started. Do you want to restart the debugger? [y/N] ")
            if answer.lower() == 'y':
                raise RestartDbgException()
            return
        if self.debug_target.target_address == "0x0":
            print("No target set. Use 'target' command to set it.")
            return

        # Is this a shellcode emulation?
        if self.debug_target.debug_type == 'shellcode':

            # We need to deploy the shellcode as a contract before starting the debugger
            analyzer = EVMAnalyzer.from_block_number(self.w3, self.debug_target.block_number)
            vm = analyzer.vm
            vm.state.set_balance(to_canonical_address(self.account.address), 100000000000000000000000000)

            self.debug_target.set_default('fork', vm.fork)

            txn = self.debug_target.get_transaction_dict()
            raw_txn = bytes(self.account.sign_transaction(txn).rawTransaction)
            txn = vm.get_transaction_builder().decode(raw_txn)

            receipt, computation = analyzer.apply(txn)
            deployed_address = computation.msg.storage_address.hex()

            # Now we build the new debug target object to execute the deployed contract
            new_debug_target = TransactionCondom(context.w3)
            new_debug_target.set_defaults(
                gas=6_000_000, # silly default value
                gas_price=(10 ** 9) * 1000,
                value=0,
                calldata='',
                to=deployed_address,
                origin=self.debug_target.source_address,
                sender=self.debug_target.source_address,
                nonce=self.w3.eth.get_transaction_count(self.debug_target.source_address),
            )
            new_debug_target.new_transaction(to=deployed_address,
                                             sender=self.debug_target.sender,
                                             value=self.debug_target.value,
                                             calldata=self.debug_target.calldata,
                                             block_number=self.debug_target.block_number,
                                             wallet_conf=self.wallet_conf,
                                             full_context=False,
                                             custom_balance=self.debug_target.custom_balance)
            # Set the new debug target!
            self.debug_target = new_debug_target
            self.debug_target.debug_type = 'shellcode'

            # Hook the EVM!
            analyzer.hook_vm(self._myhook)

        # If not shellcode, we check if the target address is a contract.
        elif self.debug_target.target_address is not None:
            if self.w3.eth.get_code(self.debug_target.target_address, self.debug_target.block_number) == b'':
                print(f"{RED_COLOR}Target address {self.debug_target.target_address} is not a contract {RESET_COLOR}.")
                print(f"  {RED_COLOR}(network used: {get_chain_name(self.debug_target.chain_id)}) | (block: {self.debug_target.block_number}){RESET_COLOR}")
                sys.exit(0)

        if not self.debug_target.calldata and self.started == False:
            print("No calldata set. Proceeding with empty calldata.")

        if self.debug_target.debug_type == "replay":
            analyzer = EVMAnalyzer.from_block_number(self.w3, self.debug_target.block_number)
            vm = analyzer.vm

            if self.debug_target.full_context:
                block = self.w3.eth.get_block(self.debug_target.block_number)
                num_prev_txs = len(block["transactions"][0:self.debug_target.transaction_index])
                print(f'Applying previous {num_prev_txs} transactions...')

                with alive_bar(num_prev_txs) as bar:
                    # Now we need to get the position of the transaction in the block
                    for prev_tx in block["transactions"][0:self.debug_target.transaction_index]:

                        prev_tx_target = TransactionCondom(self.w3)
                        prev_tx_target.replay_transaction(prev_tx)
                        prev_tx_target.set_default('fork', vm.fork)
                        txn = prev_tx_target.get_transaction_dict()

                        def extract_transaction_sender(source_address, transaction: SignedTransactionAPI) -> Address:
                            return bytes(HexBytes(source_address))
                        eth.vm.forks.frontier.transactions.extract_transaction_sender = functools.partial(extract_transaction_sender, prev_tx_target.source_address)

                        raw_txn = bytes(self.account.sign_transaction(txn).rawTransaction)
                        txn = vm.get_transaction_builder().decode(raw_txn)
                        #txn, receipt, _ = analyzer.next_transaction()
                        receipt, comp = vm.apply_transaction(
                            header=vm.get_header(),
                            transaction=txn,
                        )
                        bar()

            analyzer.hook_vm(self._myhook)
        elif self.debug_target.debug_type == "new":
            # get the analyzer
            analyzer = EVMAnalyzer.from_block_number(self.w3, self.debug_target.block_number, hook=self._myhook)
            vm = analyzer.vm
            vm.state.set_balance(to_canonical_address(self.account.address), 100000000000000000000000000)

        #if self.debug_target.debug_type == "replay":
        def extract_transaction_sender(source_address, transaction: SignedTransactionAPI) -> Address:
            return bytes(HexBytes(source_address))
        eth.vm.forks.frontier.transactions.extract_transaction_sender = functools.partial(extract_transaction_sender, self.debug_target.source_address)
        #else:
        #    eth._utils.transactions.extract_transaction_sender = ORIGINAL_extract_transaction_sender

        if self.debug_target.custom_balance:
            vm.state.set_balance(to_canonical_address(self.debug_target.source_address), int(self.debug_target.custom_balance))

        assert self.debug_target.fork is None or self.debug_target.fork == vm.fork
        self.vm_fork_name = vm.fork

        self.debug_target.set_default('fork', vm.fork)
        txn = self.debug_target.get_transaction_dict()
        raw_txn = bytes(self.account.sign_transaction(txn).rawTransaction)

        txn = vm.get_transaction_builder().decode(raw_txn)

        self.started = True

        addr = 'None' if self.debug_target.target_address is None else '0x'+self.debug_target.target_address.replace('0x','').zfill(40)

        origin_callframe = CallFrame(
            addr,
            self.debug_target.source_address,
            self.debug_target.source_address,
            self.debug_target.value,
            "-",
            "-")
        self.callstack.append(origin_callframe)

        self.temp_break = True
        self.tx_start_gas = self.debug_target.gas

        try:
            receipt, comp = vm.apply_transaction(
                header=vm.get_header(),
                transaction=txn,
            )
        except eth.exceptions.InsufficientFunds:
            print(f'❌ ERROR: Insufficient funds for account {self.debug_target.source_address}')
            sys.exit(0)
        except RestartDbgException:
            # If it's our restart, let's just re-raise it.
            raise RestartDbgException()
        except Exception as e:
            if "Account Balance cannot be negative" in str(e):
                print(f'❌ ERROR: Insufficient funds for account {self.debug_target.source_address}. Try with option --balance.')
                sys.exit(0)
            else:
                # Otherwise, something is terribly wrong, print and exit.
                print(f'❌ Transaction validation error: {e}')
                raise e

        # Overwrite the origin attribute
        comp.transaction_context._origin = to_canonical_address(self.debug_target.source_address)

        if hasattr(comp, 'error'):
            if type(comp.error) == eth.exceptions.OutOfGas:
                self._display_context(cmdloop=False, with_message=f'❌ {RED_BACKGROUND} ERROR: Out Of Gas{RESET_COLOR}')
            elif type(comp.error) == eth.exceptions.Revert:
                self._handle_revert()
                # Grab only the printable characters from the rever error
                revert_error = comp.error.args[0].decode('ascii', 'ignore')
                revert_error = ''.join([c for c in revert_error if c.isprintable()])
                self._display_context(cmdloop=False, with_message=f'❌ {RED_BACKGROUND} ERROR: Reverted: {revert_error}{RESET_COLOR}')
        else:
            self._display_context(cmdloop=False, with_message=f'✔️ {GREEN_BACKGROUND} Execution Terminated!{RESET_COLOR}')

    def do_context(self, arg):
        '''
        Print the context of the current execution
        Usage: context
        '''
        if self.started:
            self._display_context(cmdloop=False, with_message=None)
        else:
            quick_view = self._get_quick_view(arg)
            print(quick_view)

    def do_hextoint(self, arg):
        # make sure arg is valid hex number and return integer representation
        try:
            num = int(arg, 16)
            print(f'{num}')
        except Exception:
            print(f'Invalid hex number')
            return None

    def do_inttohex(self, arg):
        # make sure arg is valid hex number and return integer representation
        try:
            num = int(arg, 10)
            print(f'{hex(num)}')
        except Exception:
            print(f'Invalid hex number')
            return None

    @only_when_started
    def do_disass(self, args):
        '''
        Disassemble bytecode starting from a specific pc
        Usage: disass <pc> <num_instructions>
        '''
        read_args = args.split(" ")
        if len(read_args) != 2:
            print("Usage: disass <pc> <num_instructions>")
            return
        else:
            try:
                pc, num_isns = args.split(" ")[0], args.split(" ")[1]

                num_isns = int(read_args[1], 0)
                pc = int(read_args[0], 16)

                with self.comp.code.seek(pc):
                    opcode_bytes = self.comp.code.read(64) # max 32 byte immediate + 32 bytes should be enough, right???

                assert self.debug_target.fork is not None

                if opcode_bytes:
                    insn: Instruction = disassemble_one(opcode_bytes, pc=pc, fork=self.debug_target.fork)
                    assert insn is not None, "64 bytes was not enough to disassemble?? or this is somehow an invalid opcode??"
                else:
                    return

                _next_opcodes_str = f''

                for _ in range(0,num_isns):
                    pc += insn.size
                    with self.comp.code.seek(pc):
                        opcode_bytes = self.comp.code.read(64)
                    if opcode_bytes:
                        insn: Instruction = disassemble_one(opcode_bytes, pc=pc, fork=self.debug_target.fork)
                        if insn is None:
                            # we are done here
                            break
                        else:
                            hex_bytes = ' '.join(f'{b:02x}' for b in insn.bytes[:5])
                            if insn.size > 5: hex_bytes += ' ...'
                            if self.show_opcodes_desc:
                                _next_opcodes_str += f'  {pc:#06x}  {hex_bytes:18} {str(insn):20}    // {insn.description}\n'
                            else:
                                _next_opcodes_str += f'  {pc:#06x}  {hex_bytes:18} {str(insn):20}\n'
                    else:
                        break

                print(_next_opcodes_str)

            except Exception as e:
                print(f'{RED_COLOR}Error during disassemble: {e}{RESET_COLOR}')

    def do_calldata(self, args):
        '''
        Print the original calldata of the transaction
        Usage: calldata
        '''
        if not self.started:
            target_calldata = self.debug_target.calldata
        else:
            target_calldata = self.comp.msg.data.hex()

        read_args = args.split(" ")

        # Ok there are arguments
        if len(read_args) >= 1 and read_args[0] != '':

            if read_args[0].startswith('+'):
                # Sliced display
                try:
                    start_offset = int(read_args[0][1:], 10) * 2
                except Exception:
                    print(f'Invalid offset')
                    return None

                # Did the user also specify a size?
                if len(read_args) > 1:
                    try:
                        size = int(read_args[1], 10) * 2
                        end_offset = min(start_offset + size, len(target_calldata))
                    except Exception:
                        print(f'Invalid size')
                        return None
                else:
                    end_offset = len(target_calldata)

                print(f'{target_calldata[start_offset:end_offset]}')

            else:
                # Just want to set the calldata to something else
                # this is valid ONLY if the debugger is not started yet.
                if not self.started and self.debug_target.debug_type != 'shellcode':
                    self.debug_target.calldata = args
                else:
                    print(f'{target_calldata}')
        else:
            # Ok, just print the whole thing
            print(f'{target_calldata}')

    def do_weitoeth(self, arg):
        '''
        Convert wei to eth
        Usage: weitoeth <wei_amount>
        '''
        try:
            print(f'{int(arg) / 10**18} ETH')
        except Exception:
            print(f'Invalid wei amount')

    def do_ethtowei(self, arg):
        '''
        Convert eth to wei
        Usage: ethtowei <eth_amount>
        '''
        try:
            print(f'{int(float(arg) * 10**18)} wei')
        except Exception:
            print(f'Invalid ETH amount')

    @only_when_started
    def do_source(self, arg):
        '''
        Print the source code of the current contract if available
        Usage: source
        '''
        source_view = self._get_source_view(cutoff=None)
        if source_view is not None:
            print(source_view)
        else:
            print(f"No source code available for contract {normalize_contract_address(self.comp.msg.code_address)}")

    @only_when_started
    def do_storagelayout(self, arg):
        '''
        Print detailed information regarding the storage layout of the current contract
        Usage: storagelayout
        '''
        storage_layout_view = self._get_storage_layout_view()
        if storage_layout_view is not None:
            print(storage_layout_view)
        else:
            print(f"No storage layout available for contract {normalize_contract_address(self.comp.msg.code_address)}")

    @only_when_started
    def do_storage_history(self, arg):
        storage_view = self._get_storage_history_view()
        print(storage_view)

    @only_when_started
    def do_storageat(self, arg):
        '''
        Get the value of a storage slot of the current contract or of a given contract
        Usage: storageat [<address>:]<slot>
        '''
        if not arg:
            print("Usage: storageat [<address>:]<slot>")
            return

        address = None

        try:
            if ':' in arg:
                address, slot = arg.split(':')
                address = HexBytes(address)
                slot = int(slot, 16)
            else:
                address = self.comp.msg.storage_address if self.started else self.debug_target.target_address
                slot = int(arg, 16)
        except Exception:
            return
        try:
            value_read = self.comp.state.get_storage(address, slot)
        except Exception as e:
            print("Something went wrong while fetching storage:")
            print(f' Error: {RED_COLOR}{e}{RESET_COLOR}')

        value_read = "0x" + hex(value_read).replace("0x",'').zfill(64)

        print(f' {CYAN_COLOR}[r]{RESET_COLOR} Slot: {hex(slot)} | Value: {value_read}')

    def do_callhistory(self, arg):
        '''
        Print the call history of the current transaction.
        Usage: callhistory
        '''
        rich_print(self.root_tree_node)

    @only_when_started
    def do_sstores(self, arg):
        '''
        Print all the SSTOREs that have been executed so far targeting the current storage address or
        a given contract.
        Usage: sstores [<address>]
        '''
         # Check if there is an argument
        if arg and arg in self.sstores.keys():
            sstores_account = self.sstores[arg]
            for sstore_slot, sstore_val in sstores_account.items():
                if arg not in self.reverted_contracts:
                    print(f' {YELLOW_COLOR}[w]{RESET_COLOR} Slot: {sstore_slot} | Value: {sstore_val}')
                else:
                    _log = f' [w] Slot: {sstore_slot} | Value: {sstore_val}'
                    res = ''
                    for c in _log:
                        res = res + c + STRIKETHROUGH
                    print(f'{res} ❌')
        else:
            for ref_account, sstores in self.sstores.items():
                print(f'Account: {BOLD_TEXT}{BLUE_COLOR}{ref_account}{RESET_COLOR}:')
                for sstore_slot, sstore_val in sstores.items():
                    print(f' {YELLOW_COLOR}[w]{RESET_COLOR} Slot: {sstore_slot} | Value: {sstore_val}')

    @only_when_started
    def do_sloads(self, arg):
        '''
        Print all the SLOADs that have been executed so far targeting the current storage address or
        a given contract.
        Usage: sstores [<address>]
        '''
        if arg and arg in self.sloads.keys():
            sloads_account = self.sloads[arg]
            for sload_slot, sload_val in sloads_account.items():
                print(f' {CYAN_COLOR}[r]{RESET_COLOR} Slot: {sload_slot} | Value: {HexBytes(sload_val).hex()}')
        else:
            for ref_account, sloads in self.sloads.items():
                print(f'Account: {BOLD_TEXT}{BLUE_COLOR}{ref_account}{RESET_COLOR}:')
                for sload_slot, sload_val in sloads.items():
                    print(f' {CYAN_COLOR}[r]{RESET_COLOR} Slot: {sload_slot} | Value: {HexBytes(sload_val).hex()}')

    @only_when_started
    def do_logs(self, arg):
        '''
        Print all the logs that have been emitted so far
        Usage: logs
        '''
        for idx_log, log in enumerate(self.logs):
            code_addr = log[0]
            mnemonic = log[1]
            topics = log[2]
            print(f' {GREEN_COLOR} 📨 Contract: {code_addr} | Mnemonic: {mnemonic} {RESET_COLOR}')
            for tidx, t in enumerate(topics):
                print(f'  {YELLOW_COLOR}Topic{tidx}:{RESET_COLOR} {t} ')

    def do_breaks(self,arg):
        '''
        Print all the breakpoints
        Usage: breaks
        '''
        # Print all the breaks
        for b_idx, b in enumerate(self.breakpoints):
            print(f'Breakpoint {b_idx} | {b}')

    def do_break(self, arg):
        '''
        Set a breakpoint
        Usage: break <what><when><value>,<what><when><value>
        '''
        # parse the arg
        if not arg.strip():
            self.do_breaks(arg)
            return

        break_args = arg.split(",")
        try:
            bp = Breakpoint(break_args)
            if bp.signature not in [b.signature for b in self.breakpoints]:
                self.breakpoints.append(bp)
        except InvalidBreakpointException:
            print(f'{RED_COLOR}Invalid breakpoint{RESET_COLOR}:')
            print(f'{RED_COLOR} Valid syntax is: <what><when><value>,<what><when><value>{RESET_COLOR}')
            print(f'{RED_COLOR}  <when> in (=, ==, !=, >, <, >=, <=){RESET_COLOR}')
            print(f'{RED_COLOR}  <what> in (addr, saddr, op, pc, value, gas_remaining){RESET_COLOR}')

    def do_tbreak(self, arg):
        '''
        Set a temporary breakpoint
        Usage: tbreak <what><when><value>,<what><when><value>
        '''
        if not arg.strip():
            self.do_breaks(arg)
            return

        # parse the arg
        break_args = arg.split(",")
        try:
            bp = Breakpoint(break_args, temp=True)
            if bp.signature not in [b.signature for b in self.breakpoints]:
                self.breakpoints.append(bp)
        except InvalidBreakpointException:
            print(f'{RED_COLOR}Invalid breakpoint{RESET_COLOR}:')
            print(f'{RED_COLOR} Valid syntax is: <what><when><value>,<what><when><value>{RESET_COLOR}')
            print(f'{RED_COLOR}  <when> in (=, ==, !=, >, <, >=, <=){RESET_COLOR}')
            print(f'{RED_COLOR}  <what> in (addr, saddr, op, pc, value, gas_remaining){RESET_COLOR}')

    do_b = do_break
    do_tb = do_tbreak

    @only_when_started
    def do_finish(self, arg):
        '''
        Execute until the end of the current call frame
        Usage: finish
        '''
        if len(self.callstack) > 1:
            self.temp_break_finish = True
            self.finish_curr_stack_depth = len(self.callstack)
            self._resume()


    def do_ipython(self, arg):
        '''
        Drop into an IPython shell
        Usage: ipython
        '''
        import IPython; IPython.embed()

    @only_when_started
    def do_continue(self, arg):
        '''
        Continue the execution of the EVM
        Usage: continue
        '''
        self._resume()

    do_c = do_continue
    do_cont = do_continue

    @only_when_started
    def do_step(self, arg):
        '''
        Go to the next opcode (if the next opcode is in a different contract, it will follow the call)
        Usage: step
        '''
        if self.started == False:
            print("No execution started. Use 'start' command to start it.")
            return
        else:
            # We set the breakpoint to the next instruction
            self.temp_break = True
            self._resume()

    do_s = do_step

    def do_next(self, arg):
        '''
        Go to the next opcode (if the next opcode is in a different contract, it will NOT follow the call)
        Usage: next
        '''
        pc = self.curr_pc
        with self.comp.code.seek(pc):
            opcode_bytes = self.comp.code.read(64) # max 32 byte immediate + 32 bytes should be enough, right???

        assert self.debug_target.fork is not None

        if opcode_bytes:
            insn: Instruction = disassemble_one(opcode_bytes, pc=pc, fork=self.debug_target.fork)
            assert insn is not None, "64 bytes was not enough to disassemble?? or this is somehow an invalid opcode??"
            assert insn.mnemonic == self.curr_opcode.mnemonic, "disassembled opcode does not match the opcode we're currently executing??"
            next_pc = hex(pc + insn.size)
            curr_account_code = normalize_contract_address(self.comp.msg.code_address)
            self.do_tbreak(f'pc={next_pc},addr={curr_account_code}')
            self._resume()

    def do_clear(self, arg):
        '''
        Clear all the breakpoints or a specific one
        Usage: clear [<breakpoint_id>]
        '''
        if arg:
            if arg == "all":
                self.breakpoints = []
                print("All breakpoints cleared")
            else:
                # Check if arg is a hex number
                try:
                    arg = int(arg,16)
                    del self.breakpoints[arg]
                    print(f'Breakpoint cleared at {arg}')
                except Exception:
                    print("Invalid breakpoint")

    do_del = do_clear

    def do_log_op(self, arg):
        '''
        Log and display all the opcodes executed (toggleable)
        Usage: log_op
        '''
        self.log_op = not self.log_op
        print(f'Logging opcodes: {self.log_op}')

    def do_context_layout(self, arg):
        if arg:
            for val in arg.split(','):
                if val not in DebugConfig.VALID_CONTEXT_LAYOUT_STRINGS:
                    print(f'Invalid context layout string: {val}')
                    return
            self.context_layout = arg
        else:
            print(f'Context layout: {self.context_layout}')

    def do_hide_sloads(self, arg):
        '''
        Hide/Show the SLOADs view (toggleable)
        Usage: hide_sloads
        '''
        self.hide_sloads = not self.hide_sloads
        print(f'Hiding sloads: {self.hide_sloads}')

    def do_hide_sstores(self, arg):
        '''
        Hide/Show the SSTOREs view (toggleable)
        Usage: hide_sloads
        '''
        self.hide_sstores = not self.hide_sstores
        print(f'Hiding sstores: {self.hide_sstores}')

    def do_source_view_cutoff(self, arg):
        '''
        Set the cutoff for the source code view. -1 means no cutoff.
        Usage: source_view_cutoff <cutoff>
        '''
        if not arg:
            print(f'Source view cutoff: {self.source_view_cutoff}')
            return
        try:
            source_view_cutoff = int(arg, 10)
            if source_view_cutoff < -1:
                print(f'Invalid cutoff value: {self.source_view_cutoff}')
                return
            if source_view_cutoff == -1:
                source_view_cutoff = None
            self.source_view_cutoff = source_view_cutoff
            print(f'Source view cutoff: {self.source_view_cutoff}')
        except Exception:
            print(f'Invalid cutoff value: {self.source_view_cutoff}')

    def do_stop_on_returns(self, arg):
        '''
        Whether to stop on RETURN/STOP operations (toggleable)
        Usage: stop_on_returns
        '''
        self.stop_on_returns = not self.stop_on_returns
        print(f'Stopping on returns: {self.stop_on_returns}')

    def do_stop_on_reverts(self, arg):
        '''
        Whether to stop on REVERT operations (toggleable)
        Usage: stop_on_reverts
        '''
        self.stop_on_reverts = not self.stop_on_reverts
        print(f'Stopping on reverts: {self.stop_on_reverts}')

    def do_quit(self, arg):
        '''
        Quit the debugger
        Usage: quit
        '''
        sys.exit()

    def do_EOF(self, arg):
        # quit if user says yes or hits ctrl-d again
        try:
            if input(f"\n {BLUE_COLOR}[+] EOF, are you sure you want to quit? (y/n) {RESET_COLOR}") == 'y':
                self.do_quit(arg)
        except EOFError:
            self.do_quit(arg)
        except KeyboardInterrupt:
            pass

    def do_clearscr(self, arg):
        '''
        Clean the screen
        Usage: clear
        '''
        os.system('clear')

    do_q = do_quit

    @only_when_started
    def do_memory(self, args):
        '''
        Display the memory of the EVM at a given offset and length
        Usage: memory <offset> <length>
        '''
        read_args = args.split(" ")
        if len(read_args) != 2:
            print("Usage: memory <offset> <length>")
            return
        else:
            try:
                offset, length = args.split(" ")[0], args.split(" ")[1]

                length = int(read_args[1], 0)
                data = self.comp._memory.read(int(offset,16), length)
                hexdump(data.tobytes())
            except Exception as e:
                print(f'{RED_COLOR}Error reading memory: {e}{RESET_COLOR}')

    # === INTERNALS ===

    def _resume(self):
        raise ExitCmdException()

    def _handle_revert(self):
        # We'll mark the sstores as reverted
        curr_storage_contract = normalize_contract_address(self.comp.msg.storage_address)
        curr_code_contracts = normalize_contract_address(self.comp.msg.code_address)

        reverting_contracts = [curr_storage_contract, curr_code_contracts]
        self.reverted_contracts.add(curr_storage_contract)
        self.reverted_contracts.add(curr_code_contracts) # this is useless but ok

        worklist = set()
        for x in self.list_tree_nodes:
            worklist.add(x)

        while len(worklist) != 0:
            node = worklist.pop()
            if curr_storage_contract in node.label or (curr_code_contracts is not None and curr_code_contracts in node.label):
                offset = node.label.find(curr_storage_contract)
                if offset == -1:
                    offset = node.label.find(curr_code_contracts)
                assert(offset != -1)

                new_label = node.label[:offset]

                for c in node.label[offset:]:
                    if c.isascii():
                        new_label = new_label + c + STRIKETHROUGH
                node.label = new_label + ' (revert) ❌'
            for child in node.children:
                worklist.add(child)

    def _handle_out_of_gas(self):
        # We'll mark the sstores as reverted
        curr_storage_contract =  normalize_contract_address(self.comp.msg.storage_address)
        curr_code_contracts = normalize_contract_address(self.comp.msg.code_address)

        reverting_contracts = [curr_storage_contract, curr_code_contracts]
        self.reverted_contracts.add(curr_storage_contract)
        self.reverted_contracts.add(curr_code_contracts) # this is useless but ok

        worklist = set()
        for x in self.list_tree_nodes:
            worklist.add(x)

        while len(worklist) != 0:
            node = worklist.pop()
            if curr_code_contracts in node.label:
                offset = node.label.find(curr_storage_contract)
                if offset == -1:
                    offset = node.label.find(curr_code_contracts)
                assert(offset != -1)

                new_label = node.label[:offset]

                for c in node.label[offset:]:
                    if c.isascii():
                        new_label = new_label + c + STRIKETHROUGH
                node.label = new_label + ' (out of gas) 🪫'
            for child in node.children:
                worklist.add(child)

    def _get_callstack(self):
        message = f"{GREEN_COLOR}Callstack {RESET_COLOR}"

        fill = HORIZONTAL_LINE
        align = '<'
        width = max(self.tty_columns,0)

        title = f'{message:{fill}{align}{width}}'+'\n'

        calls_view = ''
        max_call_opcode_length = max(len('CallType'), max((len(call.calltype) for call in self.callstack), default=0))
        max_pc_length = max(len('CallSite'), max((len(call.callsite) for call in self.callstack), default=0))
        calltype_string_legend = 'CallType'.ljust(max_call_opcode_length)
        callsite_string_legend = 'CallSite'.rjust(max_pc_length)
        legend = f'{"[ Legend: Address":44} | {calltype_string_legend} | {callsite_string_legend} | {"msg.sender":44} | {"msg.value":12} | Contract Name ]\n'
        for call in self.callstack[::-1]:
            calltype_string = f'{call.calltype}'
            if call.calltype == "CALL":
                color = PURPLE_COLOR
            elif call.calltype == "DELEGATECALL" or call.calltype == "CODECALL":
                color = RED_COLOR
            elif call.calltype == "STATICCALL":
                color = BLUE_COLOR
            elif call.calltype == "CREATE":
                color = GREEN_COLOR
            elif call.calltype == "CREATE2":
                color = PURPLE_COLOR
            else:
                color = ''
            calltype_string = calltype_string.ljust(max_call_opcode_length)
            callsite_string = call.callsite.rjust(max_pc_length)
            call_addr = call.address
            if call_addr != 'None':
                registry_contract = contract_registry().get(call_addr)
                contract_name = registry_contract.metadata.contract_name if registry_contract else ''
            else:
                contract_name = ''
            msg_sender = call.msg_sender
            if msg_sender is None:
                msg_sender =  normalize_contract_address(self.comp.msg.sender.hex())
            calls_view += f'{call_addr:44} | {color}{calltype_string}{RESET_COLOR} | {callsite_string} | {msg_sender:44} | {call.value:12} | {contract_name}\n'

        return title + legend + calls_view

    def _get_disass(self):
        message = f"{GREEN_COLOR}Disassembly {RESET_COLOR}"

        fill = HORIZONTAL_LINE
        align = '<'
        width = max(self.tty_columns,0)

        title = f'{message:{fill}{align}{width}}'+'\n'

        # print the last 10 instructions, this can be configurable later
        _history = ''
        rev_history = self.history[::-1]
        curr_ins = rev_history[0]
        slice_history = rev_history[1:3]
        slice_history = slice_history[::-1]
        for insn in slice_history:
            _history += '  ' + insn + '\n'
        _history += f'→ {RED_COLOR}{self.history[-1]}{RESET_COLOR}' + '\n'

        # Let's see what's next
        pc = self.curr_pc
        with self.comp.code.seek(pc):
            opcode_bytes = self.comp.code.read(64) # max 32 byte immediate + 32 bytes should be enough, right???

        assert self.debug_target.fork is not None

        if opcode_bytes:
            insn: Instruction = disassemble_one(opcode_bytes, pc=pc, fork=self.debug_target.fork)
            assert insn is not None, "64 bytes was not enough to disassemble?? or this is somehow an invalid opcode??"
            assert insn.mnemonic == self.curr_opcode.mnemonic, "disassembled opcode does not match the opcode we're currently executing??"

        _next_opcodes_str = f''

        # print 5 instruction after
        for _ in range(0,5):
            pc += insn.size
            with self.comp.code.seek(pc):
                opcode_bytes = self.comp.code.read(64)
            if opcode_bytes:
                insn: Instruction = disassemble_one(opcode_bytes, pc=pc, fork=self.debug_target.fork)
                assert insn is not None, "64 bytes was not enough to disassemble?? or this is somehow an invalid opcode??"
                hex_bytes = ' '.join(f'{b:02x}' for b in insn.bytes[:5])
                if insn.size > 5: hex_bytes += ' ...'
                if self.show_opcodes_desc:
                    _next_opcodes_str += f'  {pc:#06x}  {hex_bytes:18} {str(insn):20}    // {insn.description}\n'
                else:
                    _next_opcodes_str += f'  {pc:#06x}  {hex_bytes:18} {str(insn):20}\n'
            else:
                break

        return title + _history + _next_opcodes_str

    def _get_metadata(self):
        message = f"{GREEN_COLOR}Metadata {RESET_COLOR}"

        fill = HORIZONTAL_LINE
        align = '<'
        width = max(self.tty_columns,0)

        title = f'{message:{fill}{align}{width}}'+'\n'

        # Fetching the metadata from the state of the computation
        curr_account_code = normalize_contract_address(self.comp.msg.code_address)
        curr_account_storage = normalize_contract_address(self.comp.msg.storage_address)
        curr_origin = normalize_contract_address(self.comp.transaction_context.origin)
        curr_balance = self.comp.state.get_balance(self.comp.msg.storage_address)
        curr_balance_eth = int(curr_balance) / 10**18

        gas_remaining = self.comp.get_gas_remaining() + self.comp.get_gas_refund()
        gas_used = self.debug_target.gas - self.comp.get_gas_remaining() - self.comp.get_gas_refund()
        gas_limit = self.comp.state.gas_limit

        _metadata = f'EVM fork: [[{self.debug_target.fork}]] | Block: {self.debug_target.block_number!r} | Origin: {curr_origin}\n'
        _metadata += f'Current Code Account: {YELLOW_COLOR}{curr_account_code}{RESET_COLOR} | Current Storage Account: {YELLOW_COLOR}{curr_account_storage}{RESET_COLOR}\n'
        _metadata += f'💰 Balance: {curr_balance} wei ({curr_balance_eth} ETH) | ⛽ Start Gas: {self.tx_start_gas} | ⛽ Gas Used: {gas_used} | ⛽ Gas Remaining: {gas_remaining}'

        return title + _metadata

    def _get_stack(self, attempt_decode=False):
        message = f"{GREEN_COLOR}Stack {RESET_COLOR}"

        fill = HORIZONTAL_LINE
        align = '<'
        width = max(self.tty_columns,0)

        title = f'{message:{fill}{align}{width}}'+'\n'

        _stack = ''

        for entry_slot, entry in enumerate(self.comp._stack.values[::-1][0:10]):
            entry_type = entry[0]
            entry_val = entry[1]

            entry_val = int.from_bytes(HexBytes(entry_val), byteorder='big')

            _stack += f'{hex(entry_slot)}│ {"0x"+hex(entry_val).replace("0x", "").zfill(64)}\n'

        # Decoration of the stack given the current opcode
        if self.curr_opcode.mnemonic == "SLOAD":
            _more_stack = _stack.split("\n")[1:]
            _stack = _stack.split("\n")[0:1]

            slot_id = int(_stack[0].split(" ")[1],16)
            _stack[0] += f'{BRIGHT_YELLOW_COLOR} (slot_id) {RESET_COLOR}'
            value_at_slot = self.comp.state.get_storage(self.comp.msg.storage_address, slot_id)
            value_at_slot = "0x"+hex(value_at_slot).replace("0x",'').zfill(64)
            _stack[0] += f'→ {ORANGE_COLOR}{value_at_slot}{RESET_COLOR}'

            return title + '\n'.join(_stack) + '\n' + '\n'.join(_more_stack)

        elif self.curr_opcode.mnemonic == "SSTORE":
            _more_stack = _stack.split("\n")[2:]
            _stack = _stack.split("\n")[0:2]

            slot_id = int(_stack[0].split(" ")[1],16)
            new_value = int(_stack[1].split(" ")[1],16)
            new_value = "0x"+hex(new_value).replace("0x",'').zfill(64)
            _stack[0] += f'{BRIGHT_YELLOW_COLOR} (slot_id) {RESET_COLOR}'
            value_at_slot = self.comp.state.get_storage(self.comp.msg.storage_address, slot_id)
            value_at_slot = "0x"+hex(value_at_slot).replace("0x",'').zfill(64)
            _stack[0] += f'→ {ORANGE_COLOR}{value_at_slot}{RESET_COLOR}'
            _stack[1] += f'{BRIGHT_YELLOW_COLOR} (slotval){RESET_COLOR} → '

            _diff_string = ''
            for idx, byte in enumerate(value_at_slot):
                if byte != new_value[idx]:
                    _diff_string += f'{RED_COLOR}{new_value[idx]}{RESET_COLOR}'
                else:
                    _diff_string += f'{GREEN_COLOR}{byte}{RESET_COLOR}'
            _stack[1] += _diff_string

            # do a diff between the value at the slot and the new value and print
            # every byte of the new value in green if they are the same, in red if they are different

            return title + '\n'.join(_stack) + '\n' + '\n'.join(_more_stack)

        elif self.curr_opcode.mnemonic == "CALL":
            _more_stack = _stack.split("\n")[7:]
            _stack = _stack.split("\n")[0:7]

            gas = int(_stack[0].split(" ")[1],16)
            value = int(_stack[2].split(" ")[1],16)
            argOffset =  int(_stack[3].split(" ")[1],16)
            argSize   =  int(_stack[4].split(" ")[1],16)

            argSizeHuge = False

            if argSize > 20:
                argSize = 20
                argSizeHuge = True

            _stack[0] += f' ({gas}) {BRIGHT_YELLOW_COLOR} (gas) {RESET_COLOR}'
            _stack[1] += f'{BRIGHT_YELLOW_COLOR} (target) {RESET_COLOR}'
            _stack[2] += f' ({value}){BRIGHT_YELLOW_COLOR} (value) {RESET_COLOR}'
            _stack[3] += f'{BRIGHT_YELLOW_COLOR} (argOffset) {RESET_COLOR}'
            _stack[4] += f'{BRIGHT_YELLOW_COLOR} (argSize) {RESET_COLOR}'

            memory_at_offset = self.comp._memory.read(argOffset,argSize).hex()

            if argSizeHuge:
                _stack[3] += f'{ORANGE_COLOR}→ {GREEN_COLOR}{BOLD_TEXT}[0x{memory_at_offset[0:8]}]{RESET_COLOR}{ORANGE_COLOR}{memory_at_offset[8:]}...{RESET_COLOR}'
            else:
                _stack[3] += f'{ORANGE_COLOR}→ {GREEN_COLOR}{BOLD_TEXT}[0x{memory_at_offset[0:8]}]{RESET_COLOR}{ORANGE_COLOR}{memory_at_offset[8:]}{RESET_COLOR}'

            _stack[5] += f'{BRIGHT_YELLOW_COLOR} (retOffset) {RESET_COLOR}'
            _stack[6] += f'{BRIGHT_YELLOW_COLOR} (retSize) {RESET_COLOR}'

            return title + '\n'.join(_stack) + '\n' + '\n'.join(_more_stack)
        elif self.curr_opcode.mnemonic == "DELEGATECALL":
            _more_stack = _stack.split("\n")[7:]
            _stack = _stack.split("\n")[0:7]

            gas = int(_stack[0].split(" ")[1],16)
            argOffset =  int(_stack[2].split(" ")[1],16)
            argSize   =  int(_stack[3].split(" ")[1],16)

            argSizeHuge = False

            if argSize > 50:
                argSize = 50
                argSizeHuge = True

            _stack[0] += f' ({gas}) {BLUE_COLOR} (gas) {RESET_COLOR}'
            _stack[1] += f'{BLUE_COLOR} (target) {RESET_COLOR}'
            _stack[2] += f'{BLUE_COLOR} (argOffset) {RESET_COLOR}'
            _stack[3] += f'{BLUE_COLOR} (argSize) {RESET_COLOR}'

            memory_at_offset = self.comp._memory.read(argOffset,argSize).hex()

            if argSizeHuge:
                _stack[2] += f'{ORANGE_COLOR}→ {GREEN_COLOR}{BOLD_TEXT}[0x{memory_at_offset[0:8]}]{RESET_COLOR}{ORANGE_COLOR}{memory_at_offset[8:]}...{RESET_COLOR}'
            else:
                _stack[2] += f'{ORANGE_COLOR}→ {GREEN_COLOR}{BOLD_TEXT}[0x{memory_at_offset[0:8]}]{RESET_COLOR}{ORANGE_COLOR}{memory_at_offset[8:]}{RESET_COLOR}'

            _stack[4] += f'{BLUE_COLOR} (retOffset) {RESET_COLOR}'
            _stack[5] += f'{BLUE_COLOR} (retSize) {RESET_COLOR}'

            return title + '\n'.join(_stack) + '\n' + '\n'.join(_more_stack)

        elif self.curr_opcode.mnemonic == "STATICCALL":
            _more_stack = _stack.split("\n")[7:]
            _stack = _stack.split("\n")[0:7]

            gas = int(_stack[0].split(" ")[1],16)
            argOffset =  int(_stack[2].split(" ")[1],16)
            argSize   =  int(_stack[3].split(" ")[1],16)

            argSizeHuge = False

            if argSize > 50:
                argSize = 50
                argSizeHuge = True

            _stack[0] += f' ({gas}) {BLUE_COLOR} (gas) {RESET_COLOR}'
            _stack[1] += f'{BLUE_COLOR} (target) {RESET_COLOR}'
            _stack[2] += f'{BLUE_COLOR} (argOffset) {RESET_COLOR}'
            _stack[3] += f'{BLUE_COLOR} (argSize) {RESET_COLOR}'

            memory_at_offset = self.comp._memory.read(argOffset,argSize).hex()

            if argSizeHuge:
                _stack[2] += f'{ORANGE_COLOR}→ {GREEN_COLOR}{BOLD_TEXT}[0x{memory_at_offset[0:8]}]{RESET_COLOR}{ORANGE_COLOR}{memory_at_offset[8:]}...{RESET_COLOR}'
            else:
                _stack[2] += f'{ORANGE_COLOR}→ {GREEN_COLOR}{BOLD_TEXT}[0x{memory_at_offset[0:8]}]{RESET_COLOR}{ORANGE_COLOR}{memory_at_offset[8:]}{RESET_COLOR}'

            _stack[4] += f'{BLUE_COLOR} (retOffset) {RESET_COLOR}'
            _stack[5] += f'{BLUE_COLOR} (retSize) {RESET_COLOR}'

            return title + '\n'.join(_stack) + '\n' + '\n'.join(_more_stack)
        else:
            return title + _stack


    def _get_storage_history_view(self):
        ref_account = normalize_contract_address(self.comp.msg.storage_address)
        message = f"{GREEN_COLOR}Last Active Storage Slots [{ref_account}]{RESET_COLOR}"

        fill = HORIZONTAL_LINE
        align = '<'
        width = max(self.tty_columns,0)

        title = f'{message:{fill}{align}{width}}'+'\n'
        legend = f'[ Legend: Slot Address -> Value ]\n'

        # Iterate over sloads for this account
        _sload_log = ''
        if not self.hide_sloads:
            if ref_account in self.sloads:
                ref_account_sloads = self.sloads[ref_account]
                for slot, val in ref_account_sloads.items():
                    _sload_log += f'{CYAN_COLOR}[r]{RESET_COLOR} {slot} -> {hex(val)}\n'

        _sstore_log = ''
        # Iterate over sstore for this account
        if not self.hide_sstores:
            ref_account = normalize_contract_address(self.comp.msg.storage_address)
            if ref_account in self.sstores:
                ref_account_sstores = self.sstores[ref_account]
                for slot, val in ref_account_sstores.items():
                    _sstore_log += f'{YELLOW_COLOR}[w]{RESET_COLOR} {slot} -> {val}\n'

        return title + legend + _sload_log + _sstore_log

    def _get_quick_view(self, arg):
        message = f"{GREEN_COLOR}Quick View{RESET_COLOR}"
        fill = HORIZONTAL_LINE
        align = '<'
        width = max(self.tty_columns,0)

        title = f'{message:{fill}{align}{width}}'

        if arg != 'init':
            print(title)

        print(f'Account: {YELLOW_COLOR}{self.debug_target.source_address}{RESET_COLOR} | Target Contract: {YELLOW_COLOR}{self.debug_target.target_address}{RESET_COLOR}')
        print(f'Chain: {self.debug_target.chain} | Node: {self.w3.provider.endpoint_uri} | Block Number: {self.debug_target.block_number!r}')
        print(f'Value: {self.debug_target.value} | Gas: {self.debug_target.gas}')

    def _get_source_view(self, cutoff=None):
        message = f"{GREEN_COLOR}Source View{RESET_COLOR}"
        fill = HORIZONTAL_LINE
        align = '<'
        width = max(self.tty_columns,0)

        title = f'{message:{fill}{align}{width}}'

        if not self.started:
            return None

        try:
            source = get_source_code_view_for_pc(self.debug_target, self.comp.msg.code_address, self.comp.code.program_counter - 1)
        except Exception as e:
            source = None

        # If we have a huge source view, this is probably imprecise
        # or it means we are in the dispatcher (which is fake), hide this.
        if source:
            lines = source.splitlines()
            if cutoff is None or len(lines) <= self.source_view_cutoff:
                return title + '\n' + source
            else:
                return title + '\n' + '\n'.join(lines[:cutoff]) + '\n' + f'{ORANGE_COLOR}... [source too big, use "source" command to see it all or change the "source_view_cutoff"] ...{RESET_COLOR}'

    def _get_storage_layout_view(self):
        message = f"{GREEN_COLOR}Storage Layout{RESET_COLOR}"
        fill = HORIZONTAL_LINE
        align = '<'
        width = max(self.tty_columns,0)

        title = f'{message:{fill}{align}{width}}'

        storage_layout = get_storage_layout_table(
            lambda slot: self.comp.state.get_storage(self.comp.msg.storage_address, slot).to_bytes(32, byteorder='big'),
            self.comp.msg.code_address,
            self.comp.msg.storage_address
            )

        if storage_layout is not None:
            with rich.get_console().capture() as capture:
                rich.print(storage_layout)
            storage_layout = capture.get()
            return title + storage_layout + '\n'
        else:
            return None

    def _display_context(self, cmdloop=True, with_message=''):
        for val in self.context_layout.split(","):
            if val == 'status':
                if with_message:
                    print(f'Status: {with_message}')

            elif val == 'source':
                source_view = self._get_source_view(cutoff=self.source_view_cutoff)
                if source_view is not None:
                    print(source_view)

            elif val == 'storage_layout':
                storage_layout_view = self._get_storage_layout_view()
                if storage_layout_view is not None:
                    print(storage_layout_view)

            elif val == 'storage_history':
                storage_history_view = self._get_storage_history_view()
                print(storage_history_view)

            elif val == 'metadata':
                metadata_view = self._get_metadata()
                print(metadata_view)

            elif val == 'disass':
                disass_view = self._get_disass()
                print(disass_view)

            elif val == 'stack':
                stack_view = self._get_stack()
                print(stack_view)

            elif val == 'callstack':
                callstack_view = self._get_callstack()
                print(callstack_view)

        if cmdloop:
            try:
                self.cmdloop(intro='')
            except ExitCmdException:
                pass
            except RestartDbgException:
                raise RestartDbgException()

    def _myhook(self, opcode: Opcode, computation: ComputationAPI):
        # Store a reference to the computation to make it
        # accessible to the comamnds

        # Overwriting the origin
        computation.transaction_context._origin = to_canonical_address(self.debug_target.source_address)

        self.comp = computation
        self.curr_opcode = opcode

        # the computation.code.__iter__() has already incremented the program counter by 1, account for this
        pc = computation.code.program_counter - 1
        self.curr_pc = pc

        with computation.code.seek(pc):
            opcode_bytes = computation.code.read(64) # max 32 byte immediate + 32 bytes should be enough, right???

        assert self.debug_target.fork is not None
        if opcode_bytes:
            insn: Instruction = disassemble_one(opcode_bytes, pc=pc, fork=self.debug_target.fork)
            assert insn is not None, "64 bytes was not enough to disassemble?? or this is somehow an invalid opcode??"
            if insn.mnemonic != opcode.mnemonic:
                print(f"disassembled opcode does not match the opcode we're currently executing??")
            hex_bytes = ' '.join(f'{b:02x}' for b in insn.bytes[:5])
            if insn.size > 5: hex_bytes += ' ...'
            if self.show_opcodes_desc:
                _opcode_str = f'{pc:#06x}  {hex_bytes:18} {str(insn):20}    // {insn.description}'
            else:
                _opcode_str = f'{pc:#06x}  {hex_bytes:18} {str(insn):20}'
        else:
            _opcode_str = f'{pc:#06x}  {"":18} {opcode.mnemonic:15} [WARNING: no code]'

        if self.log_op:
            gas_used = self.debug_target.gas - self.comp.get_gas_remaining() - self.comp.get_gas_refund()
            print(f'{_opcode_str}  ⛽️ gas_used: {gas_used}')

        self.history.append(_opcode_str)

        if self.temp_break:
            self.temp_break = False
            self._display_context(with_message=f'🎯 {YELLOW_COLOR}Breakpoint [temp] reached {RESET_COLOR}')
        else:
            # BREAKPOINT MANAGEMENT
            for sbpid, sbp in enumerate(self.breakpoints):
                if sbp.eval_bp(self.comp, pc, opcode, self.callstack):
                    if sbp.temp:
                        self.breakpoints.remove(sbp)
                    self._display_context(with_message=f'🎯 {YELLOW_COLOR}Breakpoint [{sbpid}] reached {RESET_COLOR}')

        if self.temp_break_finish and len(self.callstack) < self.finish_curr_stack_depth:
            # Reset finish break condition
            self.temp_break_finish = False
            self.finish_curr_stack_depth = None
            self._display_context(with_message=f'🎯 {YELLOW_COLOR}Breakpoint [finish] reached {RESET_COLOR}')

        elif self.stop_on_returns and (opcode.mnemonic == "STOP" or opcode.mnemonic == "RETURN"):
            self._display_context(with_message=f'🎯 {YELLOW_COLOR}Breakpoint [stop/return] reached {RESET_COLOR}')

        elif self.stop_on_reverts and opcode.mnemonic == "REVERT":
            self._display_context(with_message=f'🎯 {YELLOW_COLOR}Breakpoint [revert] reached {RESET_COLOR}')

        if opcode.mnemonic == "SSTORE":
            ref_account = normalize_contract_address(computation.msg.storage_address)

            slot_id = hex(read_stack_int(computation, 1))
            slot_val = hex(read_stack_int(computation, 2))

            if ref_account not in self.sstores.keys():
                self.sstores[ref_account] = {}
                self.sstores[ref_account][slot_id] = slot_val
            else:
                self.sstores[ref_account][slot_id] = slot_val

        if opcode.mnemonic == "SLOAD":
            ref_account = normalize_contract_address(computation.msg.storage_address)
            slot_id = hex(read_stack_int(computation, 1))

            # CHECK THIS
            slot_val = computation.state.get_storage(computation.msg.storage_address, int(slot_id,16))
            if ref_account not in self.sloads.keys():
                self.sloads[ref_account] = {}
                self.sloads[ref_account][slot_id] = slot_val
            else:
                self.sloads[ref_account][slot_id] = slot_val

        if "LOG" in opcode.mnemonic:
            n_topics = int(opcode.mnemonic[-1])
            offset = hex(read_stack_int(computation, 1))
            size = hex(read_stack_int(computation, 2))
            emitted_topics = []
            if n_topics > 0:
                for i in range(n_topics):
                    emitted_topics.append(hex(read_stack_int(computation, 3 + i)))
            self.logs.append((normalize_contract_address(computation.msg.code_address), opcode.mnemonic , emitted_topics))

        if opcode.mnemonic in CALL_OPCODES:

            if opcode.mnemonic == "CALL":
                contract_target = hex(read_stack_int(computation, 2))
                contract_target = normalize_contract_address(contract_target)
                value_sent = read_stack_int(computation, 3)

                # We gotta parse the callstack according to the *CALL opcode
                new_callframe = CallFrame(
                                        contract_target,
                                        normalize_contract_address(computation.msg.code_address),
                                        normalize_contract_address(computation.transaction_context.origin),
                                        value_sent,
                                        "CALL",
                                        hex(pc)
                                        )

                self.callstack.append(new_callframe)
                new_tree_node = self.curr_tree_node.add(f"{PURPLE_COLOR}CALL{RESET_COLOR} {contract_target}")
                self.curr_tree_node = new_tree_node
                self.list_tree_nodes.append(new_tree_node)

            elif opcode.mnemonic == "DELEGATECALL":
                contract_target = hex(read_stack_int(computation, 2))
                contract_target = normalize_contract_address(contract_target)
                value_sent = 0
                # We gotta parse the callstack according to the *CALL opcode
                new_callframe = CallFrame(
                                        contract_target,
                                        self.callstack[-1].msg_sender,
                                        normalize_contract_address(computation.transaction_context.origin),
                                        value_sent,
                                        "DELEGATECALL",
                                        hex(pc)
                                        )
                self.callstack.append(new_callframe)
                new_tree_node = self.curr_tree_node.add(f"{RED_COLOR}DELEGATECALL{RESET_COLOR} {contract_target}")
                self.curr_tree_node = new_tree_node
                self.list_tree_nodes.append(new_tree_node)

            elif opcode.mnemonic == "STATICCALL":
                contract_target = hex(read_stack_int(computation, 2))
                contract_target = normalize_contract_address(contract_target)

                value_sent = 0
                if int(contract_target,16) not in PRECOMPILED_CONTRACTS.values():
                    # We gotta parse the callstack according to the *CALL opcode
                    new_callframe = CallFrame(
                                            contract_target,
                                            normalize_contract_address(computation.msg.code_address),
                                            normalize_contract_address(computation.transaction_context.origin),
                                            value_sent,
                                            "STATICCALL",
                                            hex(pc)
                                            )
                    self.callstack.append(new_callframe)
                    new_tree_node = self.curr_tree_node.add(f"{BLUE_COLOR}STATICCALL{RESET_COLOR} {contract_target}")
                    self.curr_tree_node = new_tree_node
                    self.list_tree_nodes.append(new_tree_node)
                else:
                    self.curr_tree_node.add(f"{BLUE_COLOR}STATICCALL{RESET_COLOR} {contract_target}")

            elif opcode.mnemonic == "CREATE":
                contract_value = read_stack_int(computation, 1)
                code_offset = hex(read_stack_int(computation, 2))
                code_size = hex(read_stack_int(computation, 3))

                # calculate the target address as per specification
                contract_address = calculate_create_contract_address(self.w3, computation.msg.storage_address, computation.state.get_nonce(computation.msg.storage_address))

                # this means there was a nested CREATE/CREATE2
                if not computation.msg.code_address:
                    msg_sender = computation.msg.storage_address
                else:
                    msg_sender = computation.msg.code_address
                new_callframe = CallFrame(
                    normalize_contract_address(contract_address),
                    normalize_contract_address(msg_sender),
                    normalize_contract_address(computation.transaction_context.origin),
                    contract_value,
                    "CREATE",
                    hex(pc)
                )
                self.callstack.append(new_callframe)
                new_tree_node = self.curr_tree_node.add(f"{GREEN_COLOR}CREATE{RESET_COLOR} {contract_address}")
                self.curr_tree_node = new_tree_node
                self.list_tree_nodes.append(new_tree_node)

            elif opcode.mnemonic == "CREATE2":
                contract_value = hex(read_stack_int(computation, 1))
                code_offset = hex(read_stack_int(computation, 2))
                code_size = hex(read_stack_int(computation, 3))
                salt = read_stack_bytes(computation, 4)

                contract_address = calculate_create2_contract_address(self.w3, computation.msg.storage_address, salt,
                                                                    self.comp._memory.read(int(code_offset,16),
                                                                                           int(code_size,16)).tobytes())

                # this means there was a nested CREATE/CREATE2
                if not computation.msg.code_address:
                    msg_sender = computation.msg.storage_address
                else:
                    msg_sender = computation.msg.code_address

                new_callframe = CallFrame(
                    normalize_contract_address(contract_address),
                    normalize_contract_address(msg_sender),
                    normalize_contract_address(computation.transaction_context.origin),
                    contract_value,
                    "CREATE2",
                    hex(pc)
                )
                self.callstack.append(new_callframe)
                new_tree_node = self.curr_tree_node.add(f"{GREEN_COLOR}CREATE2{RESET_COLOR} {contract_address}")
                self.curr_tree_node = new_tree_node
                self.list_tree_nodes.append(new_tree_node)
            else:
                print(f"Plz add support for {opcode.mnemonic}")

        if opcode.mnemonic in RETURN_OPCODES:
            self.callstack.pop()
            if len(self.list_tree_nodes) > 1:
                old_root = self.list_tree_nodes.pop()
                self.curr_tree_node = self.list_tree_nodes[-1]
        if opcode.mnemonic == "REVERT":
            self._handle_revert()

        # Execute the opcode finally!
        try:
            opcode(computation=computation)
        except eth.exceptions.OutOfGas:
            self._handle_out_of_gas()


    def print_license(self):
        print(f"{YELLOW_COLOR}⧫ {BOLD_TEXT}ethdbg 0.1 ⧫ - The CLI EVM Debugger{RESET_COLOR}")
        print("License: MIT License")
        print("For a copy, see <https://opensource.org/licenses/MIT>")


def main():
    parser = argparse.ArgumentParser()

    # parse optional argument
    parser.add_argument("--txid", help="address of the smart contract we are debugging", default=None)
    parser.add_argument("--full-context", help="whether we should replay the previous txs before the target one", action='store_true')
    parser.add_argument("--sender", help="address of the sender", default=None)
    parser.add_argument("--gas", help="initial gas you want to send", type=int, default=None)
    parser.add_argument("--balance", help="set a custom balance for the sender", default=None)
    parser.add_argument("--value",  help="amount of ETH to send", default=None)
    parser.add_argument("--node-url", help="url to connect to geth node (infura, alchemy, or private)", default=None)
    parser.add_argument("--target", help="address of the smart contract we are debugging", default=None)
    parser.add_argument("--block", help="reference block", default=None)
    parser.add_argument("--calldata", help="calldata to use for the transaction", default=None)
    parser.add_argument("--wallet", help="wallet id (as specified in ~/.config/ethpwn/pwn/wallets.json )", default=None)

    parser.add_argument("--shellcode", help="test on-the-fly shellcode", default=None)

    args = parser.parse_args()

    # CHECK 0: do we have a config file?
    config_file_path = get_default_global_config_path()
    if not os.path.exists(config_file_path):
        print(f"{YELLOW_COLOR} No config file found at {config_file_path} {RESET_COLOR}")
        print(f"{YELLOW_COLOR} Please use `ethpwn config create` to configure your `ethpwn` installation. {RESET_COLOR}")
        sys.exit(0)

    # CHECK 1: do we have a valid chain RPC?
    if args.node_url is not None:
        # user specified a different node, let's use it first.
        try:
            context.connect_http(args.node_url)
        except Exception:
            print(f"{RED_COLOR} ❌ Could not connect to node: {args.node_url}{RESET_COLOR}")
            sys.exit()
    elif get_default_node_url() is None:
        network = get_default_network()
        print(f"""{RED_COLOR} ❌ No RPC node url specified and no default one available in config.
It appears you did not specify a default node url for the {network} network in your configuration.
Please do so by running `ethpwn config set_default_node_url --network {network} <url>`{RESET_COLOR}""")
        sys.exit()
    else:
        try:
            context.try_auto_connect()
        except Exception as e:
            print(f"{RED_COLOR} ❌ Invalid node url in ethpwn config: {get_default_node_url()}{RESET_COLOR}")
            sys.exit()

    # Get the wallet
    wallet_conf = get_wallet(args.wallet, network=get_chain_name(context.w3.eth.chain_id))

    # Check if we support the chain
    if context.w3.eth.chain_id not in SUPPORTED_CHAINS:
        print(f'{RED_COLOR}Unsupported chain: [{context.w3.eth.chain_id}] {RESET_COLOR}')
        sys.exit(0)

    # Check if wallet and node are referring to the same chain
    if wallet_conf.network != get_chain_name(context.w3.eth.chain_id):
        print(f'Wallet {wallet_conf.name} is on chain {wallet_conf.network}, but node is on chain {get_chain_name(context.w3.eth.chain_id)}')
        sys.exit(0)

    # CHECK 2: do we have a valid sender?
    if args.sender:
        # Validate ETH address using regexp
        if not re.match(ETH_ADDRESS, args.sender):
            print(f"{RED_COLOR}Invalid ETH address provided as sender: {args.sender}{RESET_COLOR}")
            sys.exit()

    # CHECK 3: Are we re-tracing or starting a new transaction?
    if args.txid:
        # replay transaction mode
        debug_target = TransactionCondom(context.w3)
        debug_target.replay_transaction(args.txid,
                                        sender=args.sender,
                                        to=args.target,
                                        block_number=args.block,
                                        calldata=args.calldata,
                                        full_context=args.full_context,
                                        custom_balance=args.balance,
                                        custom_gas=args.gas)

    elif args.shellcode:
        # shellcode mode

        # Add a STOP at the end of the shellcode if there is none
        if args.shellcode[-2:] != "00":
            args.shellcode += "00"

        if args.value is None:
            value = 0
        else:
            value = int(args.value)

        debug_target = TransactionCondom(context.w3)
        debug_target.new_shellcode(to=None,
                                     sender=args.sender,
                                     value=value,
                                     calldata=bytes.fromhex(create_shellcode_deployer_bin(args.shellcode).hex()[2:]),
                                     block_number=args.block,
                                     wallet_conf=wallet_conf,
                                     full_context=False,
                                     custom_balance=args.balance,
                                     custom_gas=args.gas
                                    )

    else:
        # interactive mode
        # is the target an address?
        if args.target and not re.match(ETH_ADDRESS, args.target):
            print(f"{RED_COLOR}Invalid ETH address provided as target: {args.target}{RESET_COLOR}")
            sys.exit()

        if args.value is None:
            value = 0
        else:
            value = int(args.value)

        debug_target = TransactionCondom(context.w3)
        debug_target.new_transaction(to=args.target,
                                     sender=args.sender,
                                     value=value,
                                     calldata=args.calldata,
                                     block_number=args.block,
                                     wallet_conf=wallet_conf,
                                     full_context=False,
                                     custom_balance=args.balance,
                                     custom_gas=args.gas)

    # Load previous sessions history.
    load_cmds_history()

    ethdbgshell = EthDbgShell(wallet_conf, debug_target=debug_target)
    ethdbgshell.print_license()

    while True:
        import ipdb
        with ipdb.launch_ipdb_on_exception():
            try:
                ethdbgshell.cmdloop()
            except KeyboardInterrupt:
                print("")
                continue
            except ExitCmdException:
                print("Program terminated.")
                continue
            except RestartDbgException:
                old_breaks = ethdbgshell.breakpoints

                ethdbgshell = EthDbgShell(wallet_conf, debug_target=debug_target, breaks=old_breaks)
                ethdbgshell.cmdqueue.append("start\n")

if __name__ == '__main__':
    main()
