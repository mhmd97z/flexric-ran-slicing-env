from rnti_imsi import run_rnti_imsi_mapper
from raw_exposer import run_exposer
from monitoring_exporter import run_kpi_monitoring_exporter
from slice_exporter import run_slice_exporter


class Object(object):
    pass


def main():
    run_rnti_imsi_mapper()

    args = Object()
    setattr(args, "all", True)
    setattr(args, "kpi", False)
    setattr(args, "slice", False)
    run_exposer(args)

    run_kpi_monitoring_exporter()
    run_slice_exporter()


if __name__ == "__main__":
    main()

