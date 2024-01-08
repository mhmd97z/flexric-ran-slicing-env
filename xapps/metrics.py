metrics = {
    'mac': [
        'dl_aggr_tbs',      # downlink aggregated transfer block size
        'ul_aggr_tbs',      # uplink aggregated transfer block size
        'dl_aggr_sdus',     # downlink aggregated sdus
        'ul_aggr_sdus',     # uplink aggregated sdus
        'bsr',              # buffer state report
        'pusch_snr',        # channel quality
        'ul_mcs1',          # coding scheme
        'phr',              # power head room
        'wb_cqi'            # channel quality
    ],
    'rlc': [
        'rxpdu_bytes',      # aggregated bytes of rx packets
        'rxpdu_pkts',       # aggregated number of rx packets
        'txpdu_bytes',      # aggregated number of tx packets
        'txpdu_pkts',       # aggregated bytes of tx packets
    ],
    'pdcp': [
        'rxbuf_occ_bytes',  # current rx buffer occupancy in terms of amount of bytes
        'txbuf_occ_bytes',  # current rx buffer occupancy in terms of amount of packets
        'rxbuf_occ_pkts',  # current tx bufer occupancy in terms of number of bytes
        'txbuf_occ_pkts',  # current tx bufer occupancy in terms of number of packets
    ]
}
