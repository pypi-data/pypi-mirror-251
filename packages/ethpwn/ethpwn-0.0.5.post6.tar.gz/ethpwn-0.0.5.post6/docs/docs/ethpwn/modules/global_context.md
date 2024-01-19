<a id="ethpwn.ethlib.global_context"></a>

# ethpwn.ethlib.global\_context

Global context accessible from anywhere in the ethpwn package.

<a id="ethpwn.ethlib.global_context.Web3Context"></a>

## Web3Context Objects

```python
class Web3Context()
```

A context holding global state used by ethpwn.

<a id="ethpwn.ethlib.global_context.Web3Context.try_auto_connect"></a>

#### try\_auto\_connect

```python
def try_auto_connect()
```

Try to auto connect to a node if the default network is set and autoconnect is not disabled.

<a id="ethpwn.ethlib.global_context.Web3Context.terminal"></a>

#### terminal

```python
@property
def terminal()
```

Get the terminal

<a id="ethpwn.ethlib.global_context.Web3Context.terminal"></a>

#### terminal

```python
@terminal.setter
def terminal(value)
```

Set the terminal

<a id="ethpwn.ethlib.global_context.Web3Context.network"></a>

#### network

```python
@property
def network()
```

Get the default network

<a id="ethpwn.ethlib.global_context.Web3Context.network"></a>

#### network

```python
@network.setter
def network(value)
```

Set the default network

<a id="ethpwn.ethlib.global_context.Web3Context.debug_transaction_errors"></a>

#### debug\_transaction\_errors

```python
@property
def debug_transaction_errors()
```

Get whether to debug on revert

<a id="ethpwn.ethlib.global_context.Web3Context.debug_transaction_errors"></a>

#### debug\_transaction\_errors

```python
@debug_transaction_errors.setter
def debug_transaction_errors(value)
```

Set whether to debug on revert

<a id="ethpwn.ethlib.global_context.Web3Context.default_from_addr"></a>

#### default\_from\_addr

```python
@property
def default_from_addr()
```

Get the default from address as set or via the default wallet

<a id="ethpwn.ethlib.global_context.Web3Context.default_signing_key"></a>

#### default\_signing\_key

```python
@property
def default_signing_key()
```

Get the default signing key

<a id="ethpwn.ethlib.global_context.Web3Context.etherscan_api_key"></a>

#### etherscan\_api\_key

```python
@property
def etherscan_api_key()
```

Get the etherscan API key

<a id="ethpwn.ethlib.global_context.Web3Context.log_level"></a>

#### log\_level

```python
@property
def log_level()
```

Get the log level of the logger

<a id="ethpwn.ethlib.global_context.Web3Context.connect"></a>

#### connect

```python
def connect(url, can_fail=False, **kwargs)
```

Connect to the Ethereum node at `url` via HTTP/HTTPS, Websocket, or IPC depending on the URL scheme.
If `can_fail` is True, then the function will return False if it fails to connect instead of raising an exception.

<a id="ethpwn.ethlib.global_context.Web3Context.connect_http"></a>

#### connect\_http

```python
def connect_http(url, can_fail=False, **kwargs)
```

Connect to a remote Ethereum node via HTTP/HTTPS

<a id="ethpwn.ethlib.global_context.Web3Context.connect_ipc"></a>

#### connect\_ipc

```python
def connect_ipc(path='/home/eth/.ethereum/geth.ipc', can_fail=False)
```

Connect to a local Ethereum node via IPC

<a id="ethpwn.ethlib.global_context.Web3Context.connect_websocket"></a>

#### connect\_websocket

```python
def connect_websocket(url, can_fail=False, **kwargs)
```

Connect to an Ethereum node via WebSockets

<a id="ethpwn.ethlib.global_context.Web3Context.pessimistic_gas_price_estimate"></a>

#### pessimistic\_gas\_price\_estimate

```python
def pessimistic_gas_price_estimate()
```

Estimate the gas price for a transaction. This is a pessimistic estimate that will
overestimate the gas price by a factor of 2. This should be good enough to mostly
ensure that the transaction will be mined in a reasonable amount of time.

<a id="ethpwn.ethlib.global_context.Web3Context.pessimistic_transaction_cost"></a>

#### pessimistic\_transaction\_cost

```python
def pessimistic_transaction_cost(gas_used_estimate)
```

Estimate the cost of a transaction. This is a pessimistic estimate that will
overestimate the gas price by a factor of 2. This should be good enough to mostly
ensure that the transaction will be mined in a reasonable amount of time.

<a id="ethpwn.ethlib.global_context.with_local_context"></a>

#### with\_local\_context

```python
@contextlib.contextmanager
def with_local_context(**kwargs)
```

Temporarily set the global context to a new context. Will restore the old context when the
context manager exits.

