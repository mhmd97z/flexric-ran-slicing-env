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

phones = [
    a_phone,
]


class IperfTrafficGenerator():
    def __init__(self, phone: Phone) -> None:
        self.client_done = False
        self.phone = phone

    def setup_iperf_server_on_phone(self):
        client = paramiko.SSHClient()
        client.load_system_host_keys()
        client.connect(
            self.phone.data_plane_ip, 
            username=self.phone.username, 
            password=self.phone.password, 
            port=self.phone.port
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
                    stop_callback=lambda x: self.client_done,
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


    def run_iperf_from_client(self):
        subprocess.run(["iperf3", "-c", self.phone.control_plane_ip])


    def run(self):
        server_thread = threading.Thread(target=self.setup_iperf_server_on_phone)
        client_thread = threading.Thread(target=self.run_iperf_from_client)
        server_thread.start()
        time.sleep(30)
        client_thread.start()
        client_thread.join()
        self.client_done = True
        server_thread.join()


if __name__ == "__main__":
    tg = IperfTrafficGenerator(a_phone);
    tg.run()
