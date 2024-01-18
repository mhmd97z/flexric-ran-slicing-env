import paramiko
import subprocess
import threading
import time
from paramiko_expect import SSHClientInteraction
import jsonpickle
from configs import phones_json_path




class Phone():
    def __init__(self, *, data_plane_ip: str, control_plane_ip: str,
                 port: int, username: str, password: str, iperf_binary: str) -> None:
        self.data_plane_ip = data_plane_ip
        self.control_plane_ip = control_plane_ip
        self.port = port
        self.username = username
        self.password = password
        self.iperf_binary = iperf_binary


class IperfTrafficInterval:
    def __init__(self, *, length: int, bitrate) -> None:
        self.length = length
        self.bitrate = bitrate


class TrafficPattern:
    def __init__(self) -> None:
        self.intervals = []

    def add_interval(self, *, start, traffic_interval):
        self.intervals.append((start, traffic_interval))
        return self


class TrafficPatternExecutor:
    def run(self, phone: Phone, traffic_pattern: TrafficPattern):
        t = 0
        PERIOD = 0.05
        ind = 0
        while True:
            if ind < len(traffic_pattern.intervals):
                start, tp = traffic_pattern.intervals[ind]
                if start < t:
                    print("starting at ", ind, t)
                    threading.Thread(target=run_iperf_from_client, args=(phone, tp)).start()
                    ind += 1
            else:
                return
                
            time.sleep(PERIOD)
            t += PERIOD



def run_iperf_from_client(phone: Phone, iti: IperfTrafficInterval):
    bitrate_cmd_str = ""
    if iti.bitrate is not None:
        bitrate_cmd_str = f"-b {iti.bitrate}"
    subprocess.run(["iperf3", "-c", phone.data_plane_ip, "-t", str(iti.length), bitrate_cmd_str])


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



def generate_traffic(phones, traffics):
    setup_iperf_servers(phones)
    time.sleep(20)
    for phone, traffic_pattern in zip(phones, traffics):
        TrafficPatternExecutor().run(phone, traffic_pattern)


def load_phones():
    f = open(phones_json_path, "r")
    phones_json_str = '\n'.join(f.readlines())
    phones = jsonpickle.decode(phones_json_str)
    return phones


phones = load_phones()

tp0 = TrafficPattern()\
        .add_interval(start=3, traffic_interval=IperfTrafficInterval(length=3, bitrate=None))\
        .add_interval(start=10, traffic_interval=IperfTrafficInterval(length=3, bitrate=None))\
        .add_interval(start=15, traffic_interval=IperfTrafficInterval(length=3, bitrate=None))

a = [tp0]
generate_traffic(phones, a)

