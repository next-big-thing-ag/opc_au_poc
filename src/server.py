import asyncio
import logging
from asyncua import Server

logging.basicConfig(level=logging.INFO)
_logger = logging.getLogger('asyncua')


async def main():
    """
    Method to start and configure the OPC UA server.

    :return: None
    """
    server = Server()
    await server.init()
    server.set_endpoint("opc.tcp://0.0.0.0:4840/freeopcua/server/")

    uri = "http://examples.freeopcua.github.io"
    idx = await server.register_namespace(uri)

    ns = "ns=2;s=freeopcua.Tags.pressure"
    ns2 = "ns=2;s=freeopcua.Tags.temperature"
    ns3 = "ns=2;s=freeopcua.Tags.measurements"

    device = await server.nodes.objects.add_object(idx, "Device")
    pressure = await device.add_variable(ns, "DevicePressure", 10.5)
    temperature = await device.add_variable(ns2, "DeviceTemperature", 26.7)
    measurements = await device.add_variable(ns3, "DeviceMeasurements", b"{}")

    await pressure.set_writable()
    await temperature.set_writable()
    await measurements.set_writable()

    _logger.info("Starting server!")
    async with server:
        while True:
            await asyncio.sleep(1)


if __name__ == "__main__":
    logging.basicConfig(level=logging.DEBUG)
    asyncio.run(main(), debug=True)
