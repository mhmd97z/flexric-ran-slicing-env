# import iperf3
import subprocess
import threading


PHONE_IP = "172.16.0.10"


PHONES = [
    # ("192.168.1.162", "ue90", "ue90"), 
    (PHONE_IP, "ue90", "ue90"), 
]



def setup_iperf_server_on_phone(phone):
    host = phone[0]
    user = phone[1]
    password = phone[2]
    cmd = "su; ls"
    # cmd = "su; iperf3 -s;"
    # cmd = ""
    cmd = ""

    fw = open("tmpout", "wb")
    fr = open("tmpout", "r")
    fi = open("tmpin", "w")
    p = subprocess.Popen(
        # f"ssh {user}@{host} -p 2222 {cmd}", 
        f"ssh hpc1", 
        shell=True,
        # stdin = fi, 
        stdin = subprocess.PIPE,
        stdout = fw, 
        stderr = fw, 
        # bufsize = 1
    )

    while True:
        s = input()
        print("handling ", s)

        p.stdin.write(s.encode("utf-8"))
        out = fr.readline()
        print("read", out)

    fw.close()
    fr.close()


    print("okkkkayyy")
    p = subprocess.Popen(
        f"ssh {user}@{host} -p 2222 {cmd}", 
        shell=True, 
        stdin=subprocess.PIPE,
        stdout=subprocess.PIPE, 
        stderr=subprocess.PIPE,
    )
    print("asdfasdfasdf")

    out = p.stdout.readline().decode("utf-8").strip()
    print("is this ", out)



    # print(type(a))
    # print(type(b))

    # get output from process "Something to print"
    # one_line_output = p.stdout.readline()
    # print(one_line_output)

""" iperf3.8 path on phone
/data/local/tmp/binaries/libs/arm64-v8a/iperf3.8
"""


def setup_iperf_client():
    # client = iperf3.Client()
    # client.server_hostname = PHONE_IP
    # client.bind_address = '10.0.0.1'

    sp = subprocess.run(["iperf3", "-c", PHONE_IP], capture_output=True)
    print(sp.stdout)
    print(sp.stderr)
    # doesn't capture output


def run_paramiko(phone):
    import paramiko
    command = "who"
    # Update the next three lines with your
    # server's information


    host = phone[0]
    username = phone[1]
    password = phone[2]

    client = paramiko.client.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    client.connect(host, username=username, password=password, port="2222")
    _stdin, _stdout,_stderr = client.exec_command(command)
    print(_stdout.read().decode())
    client.close()
    pass


# run_paramiko(PHONES[0])
#
# setup_iperf_server_on_phone(PHONES[0])
# setup_iperf_client()




def generate_traffic(phone):
    host = phone[0]
    subprocess.run(["iperf3", "-c", host])


def generate_traffic_for_all_phones(phones):
    for phone in phones:
        threading.Thread(target=generate_traffic, args=(phone, )).start()


generate_traffic_for_all_phones(PHONES)
