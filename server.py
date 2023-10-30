import sys
import os
import asyncio
import logging
import aiohttp
from messages import *

API_KEY = os.environ.get('GOOGLE_PLACES_API_KEY')
LOCALHOST = '127.0.0.1'

# Hard coded ports
server_ports = {"Bailey": 10000, "Bona": 10001, "Campbell": 10002, "Clark": 10003, "Jaquez": 10004}
server_neighbors = {
    "Clark": ["Jaquez", "Bona"],
    "Campbell": ["Bailey", "Bona", "Jaquez"],
    "Bona": ["Bailey", "Clark", "Campbell"],
    "Bailey": ["Campbell", "Bona"],
    "Jaquez": ["Clark", "Campbell"]
}

server_name = sys.argv[1]

class Server(asyncio.Protocol):
    def __init__(self, name, ip=LOCALHOST, port=8888, message_max_length=1e6):
        self.name = name
        self.ip = ip
        self.port = port
        self.message_max_length = int(message_max_length)

    async def handle_message(self, reader, writer):
        data = await reader.read(self.message_max_length)
        message = data.decode()
        addr = writer.get_extra_info('peername')
        print("{} received {} from {}".format(self.name, message, addr))

        parse_server_message = ServerMessage(self.name)
        sendback_message = await parse_server_message(message) + "\n"
        if sendback_message == "\n":
            await self.flood(message)
        elif sendback_message.startswith("old"):
            print("Old message, do not flood.")

        if sendback_message.startswith("AT"):
            print("{} send: {}".format(self.name, sendback_message[:100]))
            writer.write(sendback_message.encode())
            if (len(sendback_message.split()) == 6):
                await self.flood(sendback_message)
        # writer.write_eof()
        await writer.drain()

        print("close the client socket")
        writer.close()
    
    async def flood(self, message):
        async def send_to_server(server_name, message):
            try:
                reader, writer = await asyncio.open_connection(LOCALHOST, server_ports[neighbor])
                writer.write(message.encode())
                await writer.drain()
                print("Flooded {} with message {}".format(neighbor, message))
                writer.close()
            except ConnectionRefusedError:
                print("Connection refused to {}".format(neighbor))
                pass
        print(server_neighbors[self.name])
        for neighbor in server_neighbors[self.name]:
            print("Attempting to flood {} with message {}".format(neighbor, message))
            await asyncio.gather(send_to_server(neighbor, message))

    async def run_forever(self):
        server = await asyncio.start_server(self.handle_message, self.ip, self.port)

        # Serve requests until Ctrl+C is pressed
        print(f'serving on {server.sockets[0].getsockname()}')
        async with server:
            await server.serve_forever()
        # Close the server
        server.close()


def main():
    print(server_neighbors["Bona"])
    logging.basicConfig(filename="server_{}.log".format(server_name), format='%(levelname)s: %(message)s', filemode='w+', level=logging.INFO)
    print("Hello, welcome to server {}".format(server_name))
    server = Server(server_name, LOCALHOST, server_ports[server_name])
    try:
        asyncio.run(server.run_forever())
    except KeyboardInterrupt:
        pass

if __name__ == '__main__':
    main()