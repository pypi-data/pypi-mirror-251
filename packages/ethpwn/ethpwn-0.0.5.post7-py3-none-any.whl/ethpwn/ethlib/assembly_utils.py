'''
Module containing utility functions for assembling and disassembling EVM bytecode manually
and automatically.
'''
import subprocess

from hexbytes import HexBytes
from pyevmasm import assemble, disassemble_all, assemble_all

from .utils import run_in_new_terminal

def value_to_smallest_hexbytes(value):
    """Convert an integer to the smallest possible hexbytes"""

    # pylint: disable=unidiomatic-typecheck
    if type(value) is int:
        bit_length = value.bit_length()
        byte_length = (bit_length + 7) // 8
        if byte_length == 0:
            return HexBytes(b'\x00')
        return HexBytes(value.to_bytes(byte_length, 'big'))

    if isinstance(value, HexBytes):
        return value

    raise ValueError('value must be int or HexBytes')

def asm_push_value(value):
    """Push value to the stack"""
    value = value_to_smallest_hexbytes(value)
    return assemble('PUSH' + str(len(value)) + ' ' + value.hex())

def asm_codecopy(dst, src, size):
    """Copy code from src to dst"""
    code = asm_push_value(size)
    code += asm_push_value(src)
    code += asm_push_value(dst)
    code += assemble('CODECOPY')
    return code

def asm_return(mem_offset, length):
    """Return a value from memory"""
    code = asm_push_value(length)
    code += asm_push_value(mem_offset)
    code += assemble('RETURN')
    return code

def asm_mstore(mem_offset, value):
    """Store value at key"""
    code = asm_push_value(value)
    code += asm_push_value(mem_offset)
    code += assemble('MSTORE')
    return code

def asm_mload(mem_offset):
    """Load value at key"""
    code = asm_push_value(mem_offset)
    code += assemble('MLOAD')
    return code

def asm_sstore(key, value):
    """Store value at key"""
    code = asm_push_value(value)
    code += asm_push_value(key)
    code += assemble('SSTORE')
    return code

def asm_sload(key):
    """Load value at key"""
    code = asm_push_value(key)
    code += assemble('SLOAD')
    return code


def create_shellcode_deployer_bin(shellcode):
    """
        Create a contract that deploys shellcode at a specific address

        The deployer code is as follows:
        ```
        PUSH <len(shellcode)>   # len
        PUSH <offsetof label>   # src (offset of shellcode in the deployer)
        PUSH 0                  # dst-offset
        CODECOPY                # copy shellcode to offset 0 from <code> + <offsetof label>

        PUSH <len(shellcode)>   # length to return
        PUSH 0                  # offset to return
        RETURN                  # return shellcode
        label:
            <shellcode goes here>
        ```

    """
    shellcode = bytes(HexBytes(shellcode))

    return_code = asm_return(0, len(shellcode))

    prev_offset = 0

    # find a length of the codecopy instruction that allows us to consistently place the shellcode after
    while True:
        cur_offset = len(asm_codecopy(0, prev_offset, len(shellcode))) + len(return_code)
        if cur_offset > prev_offset:
            prev_offset = cur_offset
        else:
            break

    code = asm_codecopy(0, prev_offset, len(shellcode)) + return_code
    assert len(code) == prev_offset
    return HexBytes(code + shellcode)

def disassemble_pro(code, start_pc=0, fork='paris'):
    """
    Disassemble code and return a string containing the disassembly. This disassembly includes the
    pc, bytes, instruction, gas cost, and description of each instruction in addition to the
    standard disassembly.
    """
    code = HexBytes(code)

    insns = disassemble_all(code, pc=start_pc, fork=fork)

    disassembly = ''
    for insn in insns:
        bytes_insn = bytes(code[insn.pc - start_pc : insn.pc + - start_pc + len(insn.bytes)])
        bytes_repr = ' '.join([f'{b:02x}' for b in bytes_insn])
        disassembly += f'{insn.pc:04x}: {bytes_repr:12} {str(insn):20}'
        disassembly += f'[gas={insn.fee}, description="{insn.description}"]\n'

    return disassembly



def assemble_pro(code, start_pc=0, fork='paris'):
    """
    Assemble code and return a string containing the bytecode.
    code is a string such as:
        '''PUSH1 0x60\n \
            PUSH1 0x40\n \
            MSTORE\n \
        '''
    """
    aaa = assemble_all(code, pc=start_pc, fork=fork)

    bytecode = None
    for a in aaa:
        if bytecode is None:
            bytecode = HexBytes(a.bytes)
        else:
            bytecode += HexBytes(a.bytes)
    return bytecode.hex()

def debug_shellcode(code, ethdbg=True):
    """
    Run on-the-fly EVM bytecode inside ethdbg.
    code is the bytecode as a string such (the deploying bytecode does not need to be included)
    """
    if ethdbg:
        # create a new terminal and run ethdbg with arg --shelcode
        # TODO: spawn this in a new terminal in a multi-platform way
        # FIXME: this fails with rich
        # subprocess.run(f'ethdbg --shellcode {code}', shell=True, check=True)
        run_in_new_terminal(['ethdbg', '--shellcode', HexBytes(code).hex()])
        input('Debugger launched, press enter to continue...')

def debug_contract(code, abi, ethdbg=True):
    """
    Run the bytecode of a smart contract inside ethdbg.
    code is the run-time bytecode, abi is the abi of the contract
    """
    # TODO
    assert(False)
    if ethdbg:
        subprocess.run(f'ethdbg --new-contract-bytecode {code} --new-contract-abi {abi}', shell=True, check=True)