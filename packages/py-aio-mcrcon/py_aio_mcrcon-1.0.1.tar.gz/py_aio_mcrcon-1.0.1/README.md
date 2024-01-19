# aiomcrcon
![Python Versions](https://img.shields.io/badge/dynamic/toml?url=https%3A%2F%2Fraw.githubusercontent.com%2Farvitus%2Faiomcrcon%2Fmaster%2Fpyproject.toml&query=%24.project%5B%22requires-python%22%5D&style=for-the-badge&label=Python&color=blue)
![CodeFactor Grade](https://img.shields.io/codefactor/grade/github/arvitus/aiomcrcon?style=for-the-badge&color=green)
[![PyPI - Version](https://img.shields.io/pypi/v/py-aio-mcrcon?style=for-the-badge&color=green)](https://pypi.org/project/py-aio-mcrcon)
[![PyPI - Downloads](https://img.shields.io/pypi/dm/py-aio-mcrcon?style=for-the-badge&color=green)](https://pypi.org/project/py-aio-mcrcon)

An async Minecraft RCON client library with support for fragmented responses.

## Installing
```sh
pip install py-aio-mcrcon
```

## Example
```py
import asyncio
import aiomcrcon

async def main():
    # As context manager
    async with aiomcrcon.Client("myserver.com", "password") as client:
        response = await client.command("list")

    # Without context manager
    client = aiomcrcon.Client("myserver.com", "password") # port is optional, default is default RCON port
    await client.connect()
    response = await client.command("list")
    await client.close()

asyncio.run(main())
```

## Documentation
Everything is properly type hinted and documented in the source code. Using the IDE of your choice, you should be able to get all the information you need. Otherwise, just take a look at the [source code](./aiomcrcon/client.py).

## Fragmented responses
The Minecraft server implementation has a limit on the maximum response size of about 4096 bytes. If the response exceeds this limit, it will be split into multiple fragments. The client will automatically reassemble these fragments into a single response.  
*I do currently not know any other similar library that supports this feature.*

## Information regarding `asyncio.gather()`
The client does technically support `asyncio.gather()`, but in practice it will currently cause errors, because of a [bug](https://bugs.mojang.com/browse/MC-87863) in the Minecraft server implementation. As long as this bug is not fixed, using the client with `asyncio.gather()` will execute the first command and return its response, but everything else will be ignored and the connection will be closed by the server. This causes all of the remaining or following commands to time out (raise TimeoutError) or wait indefinitely (based on timeout parameter). The client must be closed and connected to be used again.  
**This is not a bug in this library, but in the Minecraft server implementation!**

## Contributing
If you want to contribute to this project, feel free to open a pull request or issue.