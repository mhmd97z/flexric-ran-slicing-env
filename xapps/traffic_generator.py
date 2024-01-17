import paramiko
import subprocess
import threading
import time
from paramiko_expect import SSHClientInteraction




class Phone():
    def __init__(self, *, data_plane_ip: str, control_plane_ip: str,
                 port: int, username: str, password: str, iperf_binary: str) -> None:
        self.data_plane_ip = data_plane_ip
        self.control_plane_ip = control_plane_ip
        self.port = port
        self.username = username
        self.password = password
        self.iperf_binary = iperf_binary


a_phone = Phone(
    control_plane_ip="192.168.1.162", port=2222,
    username="ue90", password="ue90", 
    iperf_binary="/data/local/tmp/binaries/libs/arm64-v8a/iperf3.8",
    data_plane_ip="172.16.0.10", 
)
a_phone.data_plane_ip = a_phone.control_plane_ip

PHONES = [
    a_phone,
]


def run_iperf_from_client(phone):
    subprocess.run(["iperf3", "-c", phone.data_plane_ip])


def setup_iperf_server_on_phone(phone):
    client = paramiko.SSHClient()
    client.load_system_host_keys()
    client.connect(
        phone.data_plane_ip, 
        username=phone.username, 
        password=phone.password, 
        port=phone.port
    )

    PROMPT = r":/ #\s+"
    try:
        with SSHClientInteraction(client, timeout=10, display=True) as interact:
            # get root access
            interact.send("su")

            # interact.expect(PROMPT)
            interact.send("whoami")
            interact.expect(".*root.*")

            # start iperf3 server using pre-existing script on device
            interact.send("/data/local/tmp/binaries/libs/arm64-v8a/iperf3.8 -s")

            interact.tail(
                line_prefix="pashmmm!",
            )
            # interact.expect()
            print("done expecting after iperf3 server")

            # interact.send('uname -a')
            # # interact.expect(PROMPT)
            # # cmd_output_uname = interact.current_output_clean
            # cmd_output_uname = interact.current_output

            interact.send('exit')
            interact.expect()

    except Exception as e:
        print(e)
    finally:
        try:
            client.close()
        except Exception:
            pass


def setup_iperf_servers(phones):
    for phone in phones:
        threading.Thread(target=setup_iperf_server_on_phone, args=(phone, )).start()



def generate_traffic(phones):
    setup_iperf_servers(phones)
    threading.Thread(target=generate_intermittent_traffic, args=(phones,)).start()


def generate_intermittent_traffic(phones):
    while True:
        time.sleep(30)
        for phone in phones:
            threading.Thread(target=run_iperf_from_client, args=(phone,)).start()


generate_traffic(PHONES)
