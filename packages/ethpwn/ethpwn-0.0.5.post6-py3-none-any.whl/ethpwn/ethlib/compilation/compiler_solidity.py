"""
This module contains the `SolidityCompiler` class, which is a wrapper around `ethcx`.
`SolidityCompiler` provides a convenient interface to compile smart contracts written in Solidity and automatically
handles version selection, input encoding, etc.
It also contains functionality to automatically recover the optimizer settings used to compile
a contract from its bytecode.
"""

from copy import deepcopy
import functools
import os
from pathlib import Path
import random
import struct
from typing import Dict, List, Union
import cbor
from hexbytes import HexBytes
import ethcx
import rich
from rich.table import Table

from ..global_context import context
from ..utils import get_shared_prefix_len


def configure_ethcx_for_solidity_pragma(pragma_line: str):
    if pragma_line is None:
        return
    
    ethcx.install_solc_pragma(pragma_line)
    ethcx.set_solc_version_pragma(pragma_line)


def find_pragma_line(content: str):
    for line in content.splitlines():
        if line.strip().startswith("pragma solidity"):
            return line


def get_pragma_lines(files: List[str]):
    pragma_lines = set()
    for file in files:
        with open(file, "r") as f:
            solidity_pragma_line = find_pragma_line(f.read())
            if solidity_pragma_line is not None:
                pragma_lines.add(solidity_pragma_line)
    return list(pragma_lines)


def merge_pragma_lines(pragma_lines: List[str]):
    if len(pragma_lines) == 0:
        return None
    if len(pragma_lines) == 1:
        return pragma_lines[0]
    pragma_lines = sorted(
        pragma_lines,
        key=lambda x: tuple(
            int(y) for y in x.split()[2].rstrip(";").strip().lstrip("><^=").split(".")
        ),
    )
    return pragma_lines[-1]  # take the highest requested one


class SolidityCompiler:
    def __init__(self) -> None:
        self.import_remappings: Dict[str, str] = {}
        self.allowed_directories: List[str] = []

    def add_import_remappings(self, remappings: Dict[str, str]):
        self.import_remappings.update(remappings)
        self.add_allowed_directories(remappings.values())

    def add_allowed_directories(self, directories: List[str]):
        self.allowed_directories.extend(directories)

    def get_output_values(self):
        output_values = [
            "abi",
            "bin",
            "bin-runtime",
            "asm",
            "hashes",
            "metadata",
            "srcmap",
            "srcmap-runtime",
        ]
        if ethcx.get_solc_version().minor >= 6:
            output_values.append("storage-layout")
        return output_values

    def get_import_remappings(
        self, no_default_import_remappings=False, import_remappings=None, **kwargs
    ):
        result = {} if no_default_import_remappings else self.import_remappings.copy()
        if import_remappings is not None:
            result.update(import_remappings)
        return result

    def get_allow_paths(self):
        return self.allowed_directories

    def get_default_optimizer_settings(self, optimizer_runs=1000):
        return {"enabled": True, "runs": optimizer_runs}

    def get_solc_input_json(
        self, sources_entry, remappings, optimizer_settings=None, libraries=None
    ):
        result = {
            "language": "Solidity",
            "sources": sources_entry,
            "settings": {
                "remappings": [
                    f"{key}={value}" for key, value in sorted(remappings.items())
                ],
                "outputSelection": {"*": {"*": ["*"], "": ["*"]}},
                "optimizer": optimizer_settings
                if optimizer_settings is not None
                else {"enabled": False},
            },
        }
        if libraries:
            libs = {"": libraries}
            for file in sources_entry.keys():
                libs[file] = libraries
            result["settings"]["libraries"] = libs
        return result

    def compile_source(
        self,
        source: str,
        file_name: Union[Path, str],
        optimizer_settings=None,
        libraries=None,
        no_default_import_remappings=False,
        extra_import_remappings=None,
        **kwargs,
    ):
        configure_ethcx_for_solidity_pragma(find_pragma_line(source))

        if optimizer_settings is None:
            optimizer_settings = self.get_default_optimizer_settings()

        input_json = self.get_solc_input_json(
            {str(file_name): {"content": source}},
            remappings=self.get_import_remappings(
                no_default_import_remappings, extra_import_remappings
            ),
            optimizer_settings=optimizer_settings,
            libraries=libraries,
        )

        kwargs = _add_cached_solc_binary_to_kwargs(kwargs)

        output_json = ethcx.compile_solidity_standard(
            input_json, allow_paths=self.get_allow_paths(), **kwargs
        )

        return input_json, output_json

    def compile_sources(
        self,
        sources: Dict[str, str],
        libraries=None,
        optimizer_settings=None,
        no_default_import_remappings=False,
        extra_import_remappings=None,
        **kwargs,
    ):
        pragma_lines = [find_pragma_line(s["content"]) for file, s in sources.items()]

        configure_ethcx_for_solidity_pragma(merge_pragma_lines(pragma_lines))

        if optimizer_settings is None:
            optimizer_settings = self.get_default_optimizer_settings()

        # sources should already be in the right format
        input_json = self.get_solc_input_json(
            sources,
            remappings=self.get_import_remappings(
                no_default_import_remappings, extra_import_remappings
            ),
            optimizer_settings=optimizer_settings,
            libraries=libraries,
        )

        kwargs = _add_cached_solc_binary_to_kwargs(kwargs)

        output_json = ethcx.compile_solidity_standard(
            input_json, allow_paths=self.get_allow_paths(), **kwargs
        )
        return input_json, output_json

    def compile_files(
        self,
        files: List[Union[str, Path]],
        libraries=None,
        optimizer_settings=None,
        no_default_import_remappings=False,
        extra_import_remappings=None,
        **kwargs,
    ):
        pragma_lines = get_pragma_lines(files)
        assert len(pragma_lines) <= 1, "Multiple solidity versions in files"
        configure_ethcx_for_solidity_pragma(pragma_lines[0] if len(pragma_lines) == 1 else None)

        if optimizer_settings is None:
            optimizer_settings = self.get_default_optimizer_settings()

        input_json = self.get_solc_input_json(
            {str(path): {"urls": [str(path)]} for path in files},
            remappings=self.get_import_remappings(
                no_default_import_remappings, extra_import_remappings
            ),
            optimizer_settings=optimizer_settings,
            libraries=libraries,
        )

        kwargs = _add_cached_solc_binary_to_kwargs(kwargs)

        allow_paths = self.get_allow_paths()
        allow_paths += [os.path.dirname(os.path.abspath(file)) for file in files]
        output_json = ethcx.compile_solidity_standard(
            input_json,
            allow_paths=allow_paths,
            **kwargs,
        )
        return input_json, output_json

    def compile_json(
        self,
        input_json: Dict[str, str],
        **kwargs,
    ):
        assert kwargs.get('solc_version', None) is not None, "solc_version must be provided"
        kwargs = _add_cached_solc_binary_to_kwargs(kwargs)

        # override the output selection to include everything
        input_json = deepcopy(input_json)
        input_json["settings"]["outputSelection"] = {"*": {"*": ["*"], "": ["*"]}}

        output_json = ethcx.compile_solidity_standard(
            input_json, allow_paths=self.get_allow_paths(), **kwargs
        )
        return input_json, output_json


solc_binary_cache = {}
vyper_binary_cache = {}


def _add_cached_solc_binary_to_kwargs(kwargs):
    solc_binary_version = kwargs.get("solc_version", None)
    if solc_binary_version is None:
        return kwargs
    if kwargs.get("solc_binary", None) is None:
        if solc_binary_version in solc_binary_cache:
            solc_binary = solc_binary_cache[solc_binary_version]
        else:
            ethcx.install_solc(solc_binary_version)
            solc_binary = ethcx.compilers.solidity.install.get_executable(
                solc_binary_version
            )
            solc_binary_cache[solc_binary_version] = solc_binary
        kwargs["solc_binary"] = solc_binary
    return kwargs


def decode_solidity_metadata_from_bytecode(bytecode):
    """
    Decodes the CBOR encoded solidity compiler metadata appended to the bytecode.
    Should include at least the IPFS hash and the solc version, but may include
    other information as well.
    """
    end_len = struct.unpack(">H", bytecode[-2:])[0]
    start_cbor = len(bytecode) - 2 - end_len
    data = cbor.loads(bytecode[start_cbor:-2])
    if 'solc' not in data:
        assert 'bzzr0' in data, "The metadata should contain either a solc version or a swarm hash"
        return data, bytecode[:start_cbor]
    else:
        assert len(data["solc"]) == 3, "The solc version should have 3 digits"
        # data["ipfs"] = HexBytes(data["ipfs"])
        data["solc"] = ".".join(str(x) for x in data["solc"])
    return data, bytecode[:start_cbor]


# pylint: disable=redefined-builtin,too-many-arguments,too-many-locals
def try_match_optimizer_settings(
    compile,
    contract_name,
    bin=None,
    bin_runtime=None,
    solc_versions=None,
    minimize=False,
):
    """
    Tries to match the optimizer settings of the given contract to the given bytecode by repeatedly
    compiling the contract with different optimizer settings until a match is found.

    ```
    from ethpwn import *

    compiler = SolidityCompiler()
    do_compile = functools.partial(compiler.compile_files, ['contracts/MyContract.sol'])

    code = context.w3.eth.getCode('0x...')

    best_kwargs, meta, result_bytecode = try_match_optimizer_settings(do_compile, 'MyContract', bin_runtime=bytecode)
    print(best_kwargs)
    ```

    :param compile: A function that takes keyword arguments `optimizer_settings` and `solc_version`
                    and returns the `output_json` from the solidity compiler. This is compatible with
                    the `SolidityCompiler.compile_source` and `SolidityCompiler.compile_files` methods.
    :param contract_name: The name of the contract to match
    :param bin: The constructor bytecode of the contract to match or `None`
    :param bin_runtime: The runtime bytecode of the contract to match or `None`
    :param solc_versions: A list of solc versions to try, if the bytecode contains metadata
                          declaring the solc version, this parameter is ignored.
    :param minimize: Whether to try to minimize the number of optimizer runs or not

    """
    try:
        from simanneal import Annealer
        import editdistance
    except ImportError:
        raise ImportError(
            "The optional `simanneal` and `editdistance` packages are required to use try_match_optimizer_settings"
        )

    if bin is None and bin_runtime is None:
        raise ValueError("At least one of bin or bin_runtime must be provided")
    if bin is not None and bin_runtime is not None:
        raise ValueError("Only one of bin or bin_runtime must be provided")
    if bin is not None:
        bin = HexBytes(bin)
    if bin_runtime is not None:
        bin_runtime = HexBytes(bin_runtime)

    if bin is not None:
        (selector, bin_data) = ("bytecode", bin)
    else:
        (selector, bin_data) = ("deployedBytecode", bin_runtime)


    sol_meta = None
    if not solc_versions:
        try:
            sol_meta, bin_data = decode_solidity_metadata_from_bytecode(bin_data)
            if "solc" in sol_meta:
                solc_versions = [sol_meta["solc"]]
        except Exception as e:
            context.logger.exception("Could not decode metadata: %s", e)
            # just continue, we just won't get an exact match

    assert (
        solc_versions is not None and len(solc_versions) > 0
    ), "At least one solc version must be provided, could not extract from bytecode metadata"

    def get_contract_bytecode_by_name(output_json, contract_name):
        for contract in output_json["contracts"].values():
            if contract_name in contract:
                return contract[contract_name]["evm"][selector]["object"]
        raise ValueError(f"Contract {contract_name} not found in output")

    def log_result(optimizer_settings, output_json, fitness):
        compiled = HexBytes(get_contract_bytecode_by_name(output_json, contract_name))
        _, compiled = decode_solidity_metadata_from_bytecode(compiled)
        prefix_len = get_shared_prefix_len(compiled, bin_data)

        table = Table(title="Settings", show_header=False)
        table.add_column("Settings", justify="left", style="cyan")
        table.add_column("Compiled size", justify="right", style="magenta")
        table.add_column("Original size", justify="right", style="magenta")
        table.add_column("Shared prefix length", justify="right", style="magenta")
        table.add_column("Fitness", justify="right", style="magenta")
        table.add_row(
            str(optimizer_settings),
            str(len(compiled)),
            str(len(bin_data)),
            str(prefix_len),
            str(fitness),
        )
        global_table.add_row(
            str(optimizer_settings),
            str(len(compiled)),
            str(len(bin_data)),
            str(prefix_len),
            str(fitness),
        )
        rich.print(table)

    table = Table(title="Settings")
    table.add_column("Settings", justify="left", style="cyan")
    table.add_column("Compiled size", justify="right", style="magenta")
    table.add_column("Original size", justify="right", style="magenta")
    table.add_column("Shared prefix length", justify="right", style="magenta")
    table.add_column("Fitness", justify="right", style="magenta")
    global_table = table

    @functools.lru_cache(maxsize=None)
    def try_compile(optimizer_settings, solc_version=None):
        optimizer_settings = dict(optimizer_settings)
        try:
            input_json, output_json = compile(
                optimizer_settings=optimizer_settings, solc_version=solc_version
            )
        except Exception as exc:
            # context.logger.warning(
            #     "Failed to compile with %s and %s: %s",
            #     optimizer_settings,
            #     solc_version,
            #     exc,
            # )
            return None, None, None
        compiled_bytecode = HexBytes(
            get_contract_bytecode_by_name(output_json, contract_name)
        )

        compiled_meta, compiled_bytecode = decode_solidity_metadata_from_bytecode(
            compiled_bytecode
        )
        if sol_meta is not None and sol_meta.get("solc", None) is not None:
            assert (
                sol_meta["solc"] == compiled_meta["solc"]
            ), "The solc versions should match"
        return output_json, compiled_meta, compiled_bytecode

    def try_settings(optimizer_settings, solc_version=None):

        output_json, output_metadata, compiled_bytecode = try_compile(
            optimizer_settings, solc_version
        )
        if compiled_bytecode is None:
            return 10000000, False

        component_prefix = len(bin_data) - get_shared_prefix_len(
            compiled_bytecode, bin_data
        )
        component_size = abs(len(bin_data) - len(compiled_bytecode))
        edit_distance = editdistance.distance(HexBytes(bin_data), compiled_bytecode)
        fitness = component_prefix + component_size
        fitness += edit_distance // 10  # if you're better by at least 10 bytes

        log_result(
            str(
                {"optimizer_settings": optimizer_settings, "solc_version": solc_version}
            ),
            output_json,
            f"{fitness} \\[{component_prefix=}, {component_size=}, {edit_distance=}\\]",
        )
        return fitness, HexBytes(compiled_bytecode).hex() == HexBytes(bin_data).hex()

    RUNS_TO_TEST = (
        0, 100, 200, 300, 400, 500, 600, 700, 800, 900,
        1000, 2000, 3000, 4000, 5000, 6000, 7000, 8000, 9000
    )
    class AnnealerGuesser(Annealer):
        """
        A simulated annealing implementation to guess the best optimizer settings
        """

        def __init__(self, state):
            super().__init__(state)
            self.lowest_runs_best_seen_state = state["runs"]
            self.highest_runs_best_seen_state = state["runs"]
            self.best_seen_solc_versions = {state["solc_version"]}
            self.best_seen_settings = state
            self.best_seen_energy = len(bin_data)
            self.best_seen_energy = self.energy()
            self.runs_to_test = [
                (runs, solc_version) for runs in RUNS_TO_TEST for solc_version in solc_versions
            ]
            self.tested_runs = set()
            self.queued_states_to_test = []

        def move(self):
            rich.print(
                f"BEST SEEN ENERGY: {self.best_seen_energy} \\[{self.lowest_runs_best_seen_state}, {self.highest_runs_best_seen_state}, {list(sorted(self.best_seen_solc_versions))}], [bold green]BEST SEEN SETTINGS: {self.best_seen_settings}[/bold green]"
            )

            if self.runs_to_test and (val := self.runs_to_test.pop(0)):
                self.state["runs"], self.state["solc_version"] = val
                return

            if self.queued_states_to_test:
                self.state = self.queued_states_to_test.pop(0)
                return

            if len(solc_versions) > 1 and random.randint(0, 1000) == 0:
                # .01% chance to try all solc versions with the current best settings
                states_to_test = [
                    deepcopy(self.state) for _ in range(len(solc_versions))
                ]
                for i, solc_version in enumerate(solc_versions):
                    states_to_test[i]["solc_version"] = solc_version
                self.queued_states_to_test.extend(states_to_test)

            if len(solc_versions) > 1 and random.randint(0, 100) < 20:
                # 50% chance for a known best solc_versions, 50% chance for a random one
                if random.randint(0, 100) < 50:
                    self.state["solc_version"] = random.choice(
                        list(self.best_seen_solc_versions)
                    )
                else:
                    self.state["solc_version"] = random.choice(solc_versions)
                return

            step = max(
                self.highest_runs_best_seen_state - self.lowest_runs_best_seen_state, 10
            )

            # if we are below the lowest best seen state, we should move towards it with a higher chance
            if self.state["runs"] < self.lowest_runs_best_seen_state:
                step_dec = int(step * 0.6)
                step_inc = step

            # if we are above the highest best seen state, we should move towards it with a higher chance
            elif self.state["runs"] > self.highest_runs_best_seen_state:
                step_dec = step
                step_inc = int(step * 0.8)

            # otherwise, we should move either way with equal chance
            else:
                step_dec = step
                step_inc = step

            self.state["runs"] += random.randint(
                max(-step_dec, -self.state["runs"]),
                min(step_inc, 1000000 - self.state["runs"]),
            )

        def energy(self):
            energy, fullmatch = try_settings(
                (("enabled", True), ("runs", self.state["runs"])),
                solc_version=self.state["solc_version"],
            )
            if energy < self.best_seen_energy:
                self.best_seen_settings = deepcopy(self.state)
                self.best_seen_energy = energy
                self.lowest_runs_best_seen_state = self.state["runs"]
                self.highest_runs_best_seen_state = self.state["runs"]
                self.best_seen_solc_versions = {self.state["solc_version"]}

            elif energy == self.best_seen_energy:
                self.lowest_runs_best_seen_state = min(
                    self.lowest_runs_best_seen_state, self.state["runs"]
                )
                self.highest_runs_best_seen_state = max(
                    self.highest_runs_best_seen_state, self.state["runs"]
                )
                self.best_seen_solc_versions.add(self.state["solc_version"])

            if fullmatch:
                self.found_exact_match = deepcopy(self.state)
                self.user_exit = True
                return 0

            return energy

    def minimize_runs_for_best_state(state, expected_result):
        cur_best = state["runs"]
        for i in range(cur_best, 0, -100):
            result = try_settings(
                (("enabled", True), ("runs", i)), solc_version=state["solc_version"]
            )
            if i == state["runs"]:
                assert expected_result == result
            if result == expected_result:
                cur_best = i

        for i in range(cur_best, max(cur_best - 100, 0), -10):
            result = try_settings(
                (("enabled", True), ("runs", i)), solc_version=state["solc_version"]
            )
            if expected_result == result:
                cur_best = i

        for i in range(cur_best, max(cur_best - 10, 0), -1):
            result = try_settings(
                (("enabled", True), ("runs", i)), solc_version=state["solc_version"]
            )
            if result == expected_result:
                cur_best = i

        return cur_best

    annealer = AnnealerGuesser(
        {
            "runs": 10,
            "solc_version": random.choice(solc_versions),
            "evmVersion": "shanghai",
        }
    )
    _, final_energy = annealer.anneal()
    best_state = annealer.best_seen_settings

    # now that we have a good guess, let's try to minimize the runs
    if minimize:
        best_state["runs"] = minimize_runs_for_best_state(best_state, final_energy)
    output_json, solidity_meta, final_bytecode = try_compile(
        (("enabled", True), ("runs", best_state["runs"])),
        solc_version=best_state["solc_version"],
    )
    log_result(best_state, output_json, str(final_energy))
    editdist = editdistance.distance(final_bytecode, bin_data)
    # pylint: disable=line-too-long
    rich.print(
        f"[bold green]FINAL STATE: {best_state}[/bold green] with fitness {final_energy} and edit distance {editdist}"
    )
    best_kwargs = {
        "optimizer_settings": {"enabled": True, "runs": best_state["runs"]},
        "solc_version": best_state["solc_version"],
    }
    return best_kwargs, solidity_meta, final_bytecode
