# import iperf3
import subprocess


PHONE_IP = "172.16.0.10"


PHONES = [
    ("172.16.0.10", "ue90", "ue90"), 
]


def generate_traffic():
    pass


def setup_iperf_server_on_phone(phone):
    host = phone[0]
    user = phone[1]
    password = phone[2]
    cmd = "su; ls"
    print("adsfasdf")
    subprocess.Popen(f"ssh {user}@{host} -p 2222 {cmd}", shell=False, stdout=subprocess.PIPE, stderr=subprocess.PIPE).communicate()


def setup_iperf_client():
    # client = iperf3.Client()
    # client.server_hostname = PHONE_IP
    # client.bind_address = '10.0.0.1'

    sp = subprocess.run(["iperf3", "-c", PHONE_IP], capture_output=True)
    print(sp.stdout)
    print(sp.stderr)
    # doesn't capture output

setup_iperf_server_on_phone(PHONES[0])
# setup_iperf_client()

