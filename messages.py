import os
import time
import json
import re
import asyncio
import aiohttp
API_KEY = "AIzaSyD3j8VSwnpGlRdFpXiU4uFCyVbiag0RMIE"

# in flooding, make sure to update timestamp

class ServerMessage:
    history = dict()

    def __init__(self, server_name="whatever_server"):
        self.server_name = server_name
        self.known_command = ["WHATSAT", "IAMAT", "AT"]

    async def __call__(self, message):
        return await self.parse_message(message) if len(message) else "? "

    async def parse_message(self, message):
        command_table = {
            "IAMAT": self.handle_i_am_at,
            "WHATSAT": self.handle_whats_at,
            "AT": self.handle_at
        }
        message_list = [msg for msg in message.strip().split() if len(msg)]
        if not self.is_valid_message(message):
            return f"? {message}"
        cmd = command_table.get(message_list[0], None)
        return await cmd(*message_list[1:])

    async def handle_i_am_at(self, client_id, coordinates, timestamp):
        msg = f"AT {self.server_name} +{time.time() - float(timestamp)} {client_id} {coordinates} {timestamp}"
        ServerMessage.history[client_id] = msg
        return msg

    async def handle_whats_at(self, client_id, radius, max_results):
        location = ServerMessage.history[client_id].split()[4]
        match = re.match(r'([+-]\d+\.\d+)([+-]\d+\.\d+)', location)
        lat, lon = match.groups()
        formatted_location = f"{lat}%2C{lon}"
        radius = int(radius)
        print("Attempting to retrieve places at location {}".format(formatted_location))
        url = f"https://maps.googleapis.com/maps/api/place/nearbysearch/json?key={API_KEY}&location={formatted_location}&radius={radius * 1000}"
        print(url)
        async with aiohttp.ClientSession() as session:
            async with session.get(url) as resp:
                response = await resp.json()
                if int(max_results) < len(response["results"]):
                    print("Limiting results to {} places".format(max_results))
                    response["results"] = response["results"][:int(max_results)]
                google_api_feedback = json.dumps(response, indent=4)
                # client_record = ServerMessage.history[client_id].split()
                # client_record[1] = f"{time.time() - float(client_record[5])}"
                # client_record = " ".join(client_record)
                return ServerMessage.history[client_id] + "\n" + google_api_feedback + "\n" + "\n"
    
    async def handle_at(self, server_name, time_difference, client_id, coordinates, timestamp):
        msg = f"AT {self.server_name} {time_difference} {client_id} {coordinates} {timestamp}"
        if client_id in ServerMessage.history:
            print("Comparing timestamps: {} and {}".format(ServerMessage.history[client_id].split()[5], timestamp))
            if float(ServerMessage.history[client_id].split()[5]) >= float(timestamp):
                print("Received old propagation")
                return "old"
        ServerMessage.history[client_id] = msg
        # check if old propagation or repeat
        return "" # is this correct

    def is_valid_message(self, message):
        print("Checking if message is valid: {}".format(message))
        split_message = message.split()
        if len(split_message) != 4:
            print("Length of message is not 4")
            if len(split_message) != 6 or split_message[0] != "AT":
                print("Received invalid message.")
                return False
        if split_message[0] == "IAMAT":
            # ensure split_message[2] are valid coordinates
            if not re.match(r'^[+-]\d{2}(?:\.\d+)?[+-]\d{3}(?:\.\d+)?$', split_message[2]):
                return False
            elif not re.match(r'^[0-9]{10}(?:\.[0-9]{1,9})?$', split_message[3]):
                return False
        elif split_message[0] == "WHATSAT":
            if not split_message[1] in self.history and split_message[2].isdigit() and split_message[3].isdigit(): # is this correct
                return False
            if int(split_message[2]) > 50 or int(split_message[3]) > 20:
                return False
        elif split_message[0] == "AT":
            print("Valid AT message")
            return True
        else:
            return False
        print("Received valid message.")
        return True

async def main():
    server_message = ServerMessage()
    answer1 = await server_message("IAMAT kiwi.cs.ucla.edu +34.068930-118.445127 1621464827.959498503")
    print(answer1)
    answer2 = await server_message("WHATSAT kiwi.cs.ucla.edu 10 1")
    print(answer2)

if __name__ == '__main__':
    # client_message = ClientMessage(client_id="whatever_name")
    # print(client_message.text("IAMAT"))
    # print(client_message.text("WHATSAT", another_client="kiwi.cs.ucla.edu", radius=10, max_results=5))
    asyncio.run(main())

    # print(server_message(client_message.text("IAMAT")))
    # print(server_message(client_message.text("WHATSAT")))
    # print(server_message.is_valid_message("WHATSAT kiwi.cs.ucla.edu 10 5"))
    # print(server_message.is_valid_message("WHATSAT kiwi.cs.ucla.edu 10 5 6"))
    # print(server_message.parse_message("IAMAT kiwi.cs.ucla.edu +34.068930-118.445127 1520023934.918963997"))