import asyncio
import time

# Examples, delete later
sample_message = "IAMAT kiwi.cs.ucla.edu +34.068930-118.445127 1621464827.959498503"
sample_query = "WHATSAT kiwi.cs.ucla.edu 10 5"

async def tcp_echo_client(message):
    reader, writer = await asyncio.open_connection('127.0.0.1', 10001)

    print(f'Send: {message!r}')
    writer.write(message.encode())
    await writer.drain()

    data = bytearray()
    while True:
        chunk = await reader.read(100)
        if not chunk:
            break
        data += chunk

    print(f'Received: {data.decode()}')

    print('Close the connection')
    writer.close()
    await writer.wait_closed()

asyncio.run(tcp_echo_client(f'IAMAT kiwi.cs.ucla.edu +34.068930-118.445127 {time.time()}'))
asyncio.run(tcp_echo_client('WHATSAT kiwi.cs.ucla.edu 10 1'))