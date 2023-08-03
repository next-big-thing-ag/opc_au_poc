import asyncio
import logging

from asyncua import Client, Node

logging.basicConfig(level=logging.INFO)
_logger = logging.getLogger('asyncua')


class SubscriptionHandler:
    def datachange_notification(self, node: Node, val, data):
        if node.nodeid.Identifier == "freeopcua.Tags.measurements":
            _logger.info(f'freeopcua.Tags.measurements changed to {val}')


async def main():
    """
    Entry point method for the program.

    Connects to an OPC server, creates a subscription, and waits for data change events.

    :return: None
    """
    client = Client(url='opc.tcp://opc_server:4840/freeopcua/server/')
    async with client:
        idx = await client.get_namespace_index(uri="http://examples.freeopcua.github.io")
        device = await client.nodes.root.get_child(["0:Objects", f"{idx}:Device"])
        variables = await device.get_variables()

        handler = SubscriptionHandler()
        subscription = await client.create_subscription(500, handler)

        await subscription.subscribe_data_change(variables)

        while True:
            await asyncio.sleep(1)


if __name__ == "__main__":
    asyncio.run(main())
