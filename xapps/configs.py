import configparser

def get_rnti_teid_path():
    parser = configparser.RawConfigParser()
    parser.read(srsran_config_path+"/enb.conf")
    return str(parser.get("log", "rnti_teid_path"))

def get_imsi_teid_path():
    parser = configparser.RawConfigParser()
    parser.read(srsran_config_path+"/epc.conf")
    return str(parser.get("log", "imsi_teid_path"))


# prometheus exporter
EXPORTER_PORT = 9000
SLICE_EXPORTER_PORT = 10001
EXPORTER_UPDATE_PERIOD = 1
PROMETHEUS_URL = "http://129.97.168.51:30090"


# ue-slice association
ASSOCIATOR_UPDATE_PERIOD = 0.5


# RNTI-IMSI Mapping
TEID_IMSI_UPDATE_PERIOD = 0.1
RNTI_TEID_UPDATE_PERIOD = 0.3


# srsran
srsran_config_path = "/root/.config/srsran"
rnti_teid_path = get_rnti_teid_path()   # /tmp/tunnel_rnti.txt
imsi_teid_path = get_imsi_teid_path()   # /tmp/imsi_teid.txt


# metrics
metrics_path = {"mac": "/home/mzi/ran-slicing-flexric-gym/flexric/build/examples/xApp/python3/stats/exporter_stats_mac.json",
                "rlc": "/home/mzi/ran-slicing-flexric-gym/flexric/build/examples/xApp/python3/stats/exporter_stats_rlc.json",
                "pdcp": "/home/mzi/ran-slicing-flexric-gym/flexric/build/examples/xApp/python3/stats/exporter_stats_pdcp.json"}

# slicing config
imsi_slice_path = "/home/mzi/ran-slicing-flexric-gym/flexric/build/examples/xApp/python3/imsi_slice_mapping_dict.json"
slicing_scheme_path = "/home/mzi/ran-slicing-flexric-gym/flexric/build/examples/xApp/python3/slicing_scheme.json"


# slicing indication
slice_indication_path = "/home/mzi/ran-slicing-flexric-gym/flexric/build/examples/xApp/python3/stats/exporter_indication_slice.json"
slice_stats_path = "/home/mzi/ran-slicing-flexric-gym/flexric/build/examples/xApp/python3/stats/exporter_stats_slice.csv"


# rnti-imsi
rnti_imsi_path = "/home/mzi/ran-slicing-flexric-gym/flexric/build/examples/xApp/python3/stats/rnti_imsi.json"
