####################
####  SLICE CONTROL PARAMETER EXAMPLE - ADD SLICE
####################
add_static_slices = {
    "num_slices" : 2,
    "slice_sched_algo" : "STATIC",
    "slices" : [
        {
            "id" : 1,
            "label" : "s1",
            "ue_sched_algo" : "PF",
            "slice_algo_params" : {"pos_low" : 1, "pos_high" : 3},
        },
        {
            "id" : 2,
            "label" : "s2",
            "ue_sched_algo" : "PF",
            "slice_algo_params" : {"pos_low" : 4, "pos_high" : 10},
        }
    ]
}

assoc_ue_slice = {
    "num_ues" : 2,
    "ues" : [
        {
            "rnti" : 0, # TODO: get rnti from slice_ind_to_dict_json()
            "assoc_dl_slice_id" : 2
        }
    ]
}

####################
####  SLICE CONTROL PARAMETER EXAMPLE - ADD SLICE
####################

add_nvs_slices_rate = {
    "num_slices" : 2,
    "slice_sched_algo" : "NVS",
    "slices" : [
        {
            "id" : 0,
            "label" : "s1",
            "ue_sched_algo" : "PF",
            "type" : "SLICE_SM_NVS_V0_RATE",
            "slice_algo_params" : {"mbps_rsvd" : 60, "mbps_ref" : 120},
        },
        {
            "id" : 2,
            "label" : "s2",
            "ue_sched_algo" : "PF",
            "type" : "SLICE_SM_NVS_V0_RATE",
            "slice_algo_params" : {"mbps_rsvd" : 60, "mbps_ref" : 120},
        }
    ]
}

add_nvs_slices_cap = {
    "num_slices" : 3,
    "slice_sched_algo" : "NVS",
    "slices" : [
        {
            "id" : 0,
            "label" : "s1",
            "ue_sched_algo" : "PF",
            "type" : "SLICE_SM_NVS_V0_CAPACITY",
            "slice_algo_params" : {"pct_rsvd" : 0.5},
        },
        {
            "id" : 2,
            "label" : "s2",
            "ue_sched_algo" : "PF",
            "type" : "SLICE_SM_NVS_V0_CAPACITY",
            "slice_algo_params" : {"pct_rsvd" : 0.3},
        },
        {
            "id" : 5,
            "label" : "s3",
            "ue_sched_algo" : "PF",
            "type" : "SLICE_SM_NVS_V0_CAPACITY",
            "slice_algo_params" : {"pct_rsvd" : 0.2},
        }
    ]
}

add_nvs_slices = {
    "num_slices" : 3,
    "slice_sched_algo" : "NVS",
    "slices" : [
        {
            "id" : 0,
            "label" : "s1",
            "ue_sched_algo" : "PF",
            "type" : "SLICE_SM_NVS_V0_CAPACITY",
            "slice_algo_params" : {"pct_rsvd" : 0.5},
        },
        {
            "id" : 2,
            "label" : "s2",
            "ue_sched_algo" : "PF",
            "type" : "SLICE_SM_NVS_V0_RATE",
            "slice_algo_params" : {"mbps_rsvd" : 50, "mbps_ref" : 120},
        },
        {
            "id" : 5,
            "label" : "s3",
            "ue_sched_algo" : "PF",
            "type" : "SLICE_SM_NVS_V0_RATE",
            "slice_algo_params" : {"mbps_rsvd" : 5, "mbps_ref" : 120},
        }
    ]
}

add_edf_slices = {
    "num_slices" : 3,
    "slice_sched_algo" : "EDF",
    "slices" : [
        {
            "id" : 0,
            "label" : "s1",
            "ue_sched_algo" : "PF",
            "slice_algo_params" : {"deadline" : 10, "guaranteed_prbs" : 20, "max_replenish" : 0},
        },
        {
            "id" : 2,
            "label" : "s2",
            "ue_sched_algo" : "RR",
            "slice_algo_params" : {"deadline" : 20, "guaranteed_prbs" : 20, "max_replenish" : 0},
        },
        {
            "id" : 5,
            "label" : "s3",
            "ue_sched_algo" : "MT",
            "slice_algo_params" : {"deadline" : 40, "guaranteed_prbs" : 10, "max_replenish" : 0},
        }
    ]
}

reset_slices = {
    "num_slices" : 0
}

assoc_ue_slice = {
    "num_ues" : 0,
    "ues" : [
    ]
}


