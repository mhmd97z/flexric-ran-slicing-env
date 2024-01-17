from rnti_imsi import run_rnti_imsi_mapper
from raw_exposer import run_exposer
from monitoring_exporter import run_kpi_monitoring_exporter
from slice_exporter import run_slice_exporter
from utils import set_slice
from ue_slice_associator import run_ue_slice_associator





def main():
    run_rnti_imsi_mapper()
    run_exposer()
    run_kpi_monitoring_exporter()
    set_slice()
    run_slice_exporter()
    run_ue_slice_associator()



if __name__ == "__main__":
    main()

