import re

from opengsq.binary_reader import BinaryReader
from opengsq.protocol_base import ProtocolBase
from opengsq.protocol_socket import UdpClient


class Quake1(ProtocolBase):
    """Quake1 Protocol"""
    full_name = 'Quake1 Protocol'

    def __init__(self, host: str, port: int, timeout: float = 5.0):
        """Quake1 Query Protocol"""
        super().__init__(host, port, timeout)
        self._delimiter1 = b'\\'
        self._delimiter2 = b'\n'
        self._request_header = b'status'
        self._response_header = 'n'

    async def get_status(self) -> dict:
        """This returns server information and players."""
        br = await self._get_response_binary_reader()

        return {
            'info': self._parse_info(br),
            'players': self._parse_players(br),
        }

    async def _get_response_binary_reader(self) -> BinaryReader:
        response_data = await self._connect_and_send(self._request_header)

        br = BinaryReader(response_data)
        header = br.read_string(self._delimiter1)

        if header != self._response_header:
            raise Exception(f'Packet header mismatch. Received: {header}. Expected: {self._response_header}.')

        return br

    def _parse_info(self, br: BinaryReader) -> dict:
        info = {}

        # Read all key values until meet \n
        while br.remaining_bytes() > 0:
            key = br.read_string(self._delimiter1)

            if key == '':
                break

            info[key] = br.read_string([self._delimiter1, self._delimiter2])

            br.stream_position -= 1

            if bytes([br.read_byte()]) == self._delimiter2:
                break

        return info

    def _parse_players(self, br: BinaryReader) -> list:
        players = []

        for matches in self._get_player_match_collections(br):
            matches: list[re.Match] = [match.group() for match in matches]

            players.append({
                'id': int(matches[0]),
                'score': int(matches[1]),
                'time': int(matches[2]),
                'ping': int(matches[3]),
                'name': str(matches[4]).strip('"'),
                'skin': str(matches[5]).strip('"'),
                'color1': int(matches[6]),
                'color2': int(matches[7]),
            })

        return players

    def _get_player_match_collections(self, br: BinaryReader):
        match_collections = []

        # Regex to split with whitespace and double quote
        regex = re.compile(r'"(\\"|[^"])*?"|[^\s]+')

        # Read all players
        while not br.is_end():
            match_collections.append(regex.finditer(br.read_string(self._delimiter2)))

        return match_collections

    async def _connect_and_send(self, data):
        header = b'\xFF\xFF\xFF\xFF'
        response_data = await UdpClient.communicate(self, header + data + b'\x00')

        # Remove the last 0x00 if exists (Only if Quake1)
        if response_data[-1] == 0:
            response_data = response_data[:-1]

        # Add \n at the last of responseData if not exists
        if response_data[-1] != self._delimiter2:
            response_data += self._delimiter2

        # Remove the first four 0xFF
        return response_data[len(header):]


if __name__ == '__main__':
    import asyncio
    import json

    async def main_async():
        quake1 = Quake1(host='35.185.44.174', port=27500, timeout=5.0)
        status = await quake1.get_status()
        print(json.dumps(status, indent=None) + '\n')

    asyncio.run(main_async())
