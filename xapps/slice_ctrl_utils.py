import xapp_sdk as ric

def fill_ue_slice_association_ctrl_msg(items):
    msg = ric.slice_ctrl_msg_t()
    msg.type = ric.SLICE_CTRL_SM_V0_UE_SLICE_ASSOC
    msg.u.ue_slice.len_ue_slice = len(items)
    assoc = ric.ue_slice_assoc_array(len(items))
    for i in range(len(items)):
        a = ric.ue_slice_assoc_t()
        a.rnti = int(items[i][0])
        a.dl_id = int(items[i][2])
        assoc[i] = a
    msg.u.ue_slice.ues = assoc
    return msg

def create_slice(slice_params, slice_sched_algo):
    s = ric.fr_slice_t()
    s.id = slice_params["id"]
    s.label = slice_params["label"]
    s.len_label = len(slice_params["label"])
    s.sched = slice_params["ue_sched_algo"]
    s.len_sched = len(slice_params["ue_sched_algo"])
    if slice_sched_algo == "STATIC":
        s.params.type = ric.SLICE_ALG_SM_V0_STATIC
        s.params.u.sta.pos_low = slice_params["slice_algo_params"]["pos_low"]
        s.params.u.sta.pos_high = slice_params["slice_algo_params"]["pos_high"]
    elif slice_sched_algo == "NVS":
        s.params.type = ric.SLICE_ALG_SM_V0_NVS
        if slice_params["type"] == "SLICE_SM_NVS_V0_RATE":
            s.params.u.nvs.conf = ric.SLICE_SM_NVS_V0_RATE
            s.params.u.nvs.u.rate.u1.mbps_required = slice_params["slice_algo_params"]["mbps_rsvd"]
            s.params.u.nvs.u.rate.u2.mbps_reference = slice_params["slice_algo_params"]["mbps_ref"]
            # print("ADD NVS DL SLCIE: id", s.id,
            # ", conf", s.params.u.nvs.conf,
            # ", mbps_rsrv", s.params.u.nvs.u.rate.u1.mbps_required,
            # ", mbps_ref", s.params.u.nvs.u.rate.u2.mbps_reference)
        elif slice_params["type"] == "SLICE_SM_NVS_V0_CAPACITY":
            s.params.u.nvs.conf = ric.SLICE_SM_NVS_V0_CAPACITY
            s.params.u.nvs.u.capacity.u.pct_reserved = slice_params["slice_algo_params"]["pct_rsvd"]
            # print("ADD NVS DL SLCIE: id", s.id,
            # ", conf", s.params.u.nvs.conf,
            # ", pct_rsvd", s.params.u.nvs.u.capacity.u.pct_reserved)
        else:
            print("Unkown NVS conf")
    elif slice_sched_algo == "EDF":
        s.params.type = ric.SLICE_ALG_SM_V0_EDF
        s.params.u.edf.deadline = slice_params["slice_algo_params"]["deadline"]
        s.params.u.edf.guaranteed_prbs = slice_params["slice_algo_params"]["guaranteed_prbs"]
        s.params.u.edf.max_replenish = slice_params["slice_algo_params"]["max_replenish"]
    else:
        print("Unkown slice algo type")

    return s


def fill_slice_scheme_ctrl_msg(ctrl_msg):
    msg = ric.slice_ctrl_msg_t()
    msg.type = ric.SLICE_CTRL_SM_V0_ADD
    dl = ric.ul_dl_slice_conf_t()
    # TODO: UL SLICE CTRL ADD
    # ul = ric.ul_dl_slice_conf_t()

    # ue_sched_algo can be "RR"(round-robin), "PF"(proportional fair) or "MT"(maximum throughput) and it has to be set in any len_slices
    ue_sched_algo = "PF"
    dl.sched_name = ue_sched_algo
    dl.len_sched_name = len(ue_sched_algo)

    dl.len_slices = ctrl_msg["num_slices"]
    slices = ric.slice_array(ctrl_msg["num_slices"])
    for i in range(0, ctrl_msg["num_slices"]):
        slices[i] = create_slice(ctrl_msg["slices"][i], ctrl_msg["slice_sched_algo"])

    dl.slices = slices
    msg.u.add_mod_slice.dl = dl
    # TODO: UL SLICE CTRL ADD
        # msg.u.add_mod_slice.ul = ul;

    return msg

