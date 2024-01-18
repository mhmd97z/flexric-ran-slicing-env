import logging
import sys
import paramiko
import subprocess
import threading
import time
from paramiko_expect import SSHClientInteraction
import jsonpickle
import numpy as np
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



def setup_iperf_server_on_phone(phone: Phone):
    logging.info("setting iperf server on phone %s ", phone.control_plane_ip)
    client = paramiko.SSHClient()
    client.load_system_host_keys()
    client.connect(
        phone.control_plane_ip, 
        username=phone.username, 
        password=phone.password, 
        port=phone.port
    )

    PROMPT = r":/ #\s+"
    try:
        with SSHClientInteraction(client, timeout=5, display=True) as interact:
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
    for phone, traffic_pattern in zip(phones, traffics):
        TrafficPatternExecutor().run(phone, traffic_pattern)


def load_phones():
    f = open(phones_json_path, "r")
    phones_json_str = '\n'.join(f.readlines())
    phones = jsonpickle.decode(phones_json_str)
    return phones


def genZ(total_time: float, length: float, inter_arrival: float):
    print("\n\n\n\n\n")
    t = 0
    points = []
    while t < total_time:
        ia = int(np.random.exponential(inter_arrival))
        l = int(np.random.exponential(length))
        if ia <= 0 or l <= 0:
            continue
        t += ia

        if t + l >= total_time:
            l = total_time - t

        points.append((t, "start"))
        points.append((t + l, "end"))
        print(t, t + l)


    # merge overlapping segements
    points = sorted(points)
    tp = TrafficPattern()
    bitrate = 0
    for i in range(len(points)):
        if bitrate >= 1 and points[i][0] != points[i - 1][0]:
            tp.add_interval(
                    start=points[i - 1][0], 
                    traffic_interval=IperfTrafficInterval(length=points[i][0] - points[i - 1][0], bitrate=bitrate)
            )
        if points[i][1] == "start":
            bitrate += 1000000
        else:
            bitrate -= 1000000

    for interval in tp.intervals:
        print(interval[0], interval[1].length + interval[0], interval[1].bitrate)

    return tp


def run():
    # np.random.seed()
    phones = load_phones()
    tps = [genZ(50, 5, 15) for phone in phones]
    generate_traffic(phones, tps)


if __name__ == "__main__":
    phones = load_phones()
    setup_iperf_servers(phones)

