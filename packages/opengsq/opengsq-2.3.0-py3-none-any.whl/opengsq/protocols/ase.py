from opengsq.binary_reader import BinaryReader
from opengsq.exceptions import InvalidPacketException
from opengsq.protocol_base import ProtocolBase
from opengsq.protocol_socket import UdpClient


class ASE(ProtocolBase):
    """All-Seeing Eye Protocol"""
    full_name = 'All-Seeing Eye Protocol'

    _request = b's'
    _response = b'EYE1'

    async def get_status(self) -> dict:
        response = await UdpClient.communicate(self, self._request)
        header = response[:4]

        if header != self._response:
            raise InvalidPacketException(
                'Packet header mismatch. Received: {}. Expected: {}.'
                .format(chr(header), chr(self._response))
            )

        br = BinaryReader(response[4:])

        result = {}
        result['gamename'] = self.__read_string(br)
        result['gameport'] = self.__read_string(br)
        result['hostname'] = self.__read_string(br)
        result['gametype'] = self.__read_string(br)
        result['map'] = self.__read_string(br)
        result['version'] = self.__read_string(br)
        result['password'] = self.__read_string(br)
        result['numplayers'] = self.__read_string(br)
        result['maxplayers'] = self.__read_string(br)
        result['rules'] = self.__parse_rules(br)
        result['players'] = self.__parse_players(br)

        return result

    def __parse_rules(self, br: BinaryReader):
        rules = {}

        while not br.is_end():
            key = self.__read_string(br)

            if not key:
                break

            rules[key] = self.__read_string(br)

        return rules

    def __parse_players(self, br: BinaryReader):
        players = []
        keys = {1: 'name', 2: 'team', 4: 'skin', 8: 'score', 16: 'ping', 32: 'time'}

        while not br.is_end():
            flags = br.read_byte()
            player = {}

            for key, value in keys.items():
                if flags & key == key:
                    player[value] = self.__read_string(br)

            players.append(player)

        return players

    def __read_string(self, br: BinaryReader):
        length = br.read_byte()
        return str(br.read_bytes(length - 1), encoding='utf-8', errors='ignore')


if __name__ == '__main__':
    import asyncio
    import json

    async def main_async():
        # mtasa
        ase = ASE(host='79.137.97.3', port=22126, timeout=10.0)
        status = await ase.get_status()
        print(json.dumps(status, indent=None) + '\n')

    asyncio.run(main_async())
