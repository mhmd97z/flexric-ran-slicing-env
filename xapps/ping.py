import logging
import sys
import paramiko
import threading
from paramiko_expect import SSHClientInteraction
import jsonpickle
from configs import phones_json_path



logging.basicConfig(level=logging.INFO, stream=sys.stdout)


class Phone():
    def __init__(self, *, data_plane_ip: str, control_plane_ip: str,
                 port: int, username: str, password: str, iperf_binary: str) -> None:
        self.data_plane_ip = data_plane_ip
        self.control_plane_ip = control_plane_ip
        self.port = port
        self.username = username
        self.password = password
        self.iperf_binary = iperf_binary


def setup_ping_in_ue(phone: Phone):
    logging.info("setting iperf server on phone %s ", phone.control_plane_ip)
    client = paramiko.SSHClient()
    client.load_system_host_keys()
    client.connect(
        phone.control_plane_ip, 
        username=phone.username, 
        password=phone.password, 
        port=phone.port
    )

    try:
        with SSHClientInteraction(client, timeout=5, display=True) as interact:
            # get root access
            interact.send("su")

            interact.send("whoami")
            interact.expect(".*root.*")

            interact.send("ping -i 30 8.8.8.8")
            interact.tail()

            interact.send('exit')
            interact.expect()

    except Exception as e:
        print(e)
    finally:
        try:
            client.close()
        except Exception:
            pass


def setup_ping_in_ues(phones):
    for phone in phones:
        threading.Thread(target=setup_ping_in_ue, args=(phone, )).start()


def load_phones():
    f = open(phones_json_path, "r")
    phones_json_str = '\n'.join(f.readlines())
    phones = jsonpickle.decode(phones_json_str)
    return phones


if __name__ == "__main__":
    setup_ping_in_ues(load_phones())
