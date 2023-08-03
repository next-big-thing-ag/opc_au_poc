import asyncio
import logging
import random

from asyncua import Client

logging.basicConfig(level=logging.INFO)
_logger = logging.getLogger('asyncua')


async def main():
    """
    The main method connects to an OPC server using the asyncua library, retrieves a device node from the server, and continuously writes random measurements to a specific variable node.

    :return: None
    """
    client = Client(url='opc.tcp://opc_server:4840/freeopcua/server/')
    async with client:

        idx = await client.get_namespace_index(uri="http://examples.freeopcua.github.io")
        device = await client.nodes.root.get_child(["0:Objects", f"{idx}:Device"])
        variables = [variable for variable in await device.get_variables() if
                 variable.nodeid.Identifier == "freeopcua.Tags.measurements"]

        while True:
            await asyncio.sleep(1)
            values = {"temperature": random.randint(0, 100), "pressure": random.randint(0, 100)}
            _logger.info(f"Setting values to {values}")

            encoded_measurements = str(values).encode('utf-8')
            await variables[0].write_value(encoded_measurements)


if __name__ == "__main__":
    asyncio.run(main())
