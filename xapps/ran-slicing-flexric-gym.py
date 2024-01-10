import json, time
from configs import slice_stats_path

class RanSlicingFlexricGym:
    def __init__(self) -> None:
        # make sure the exposer and exporter scripts are running
        # make sure the slices are up
        # make sure the ue-slice association script is running
        # make sure the traffic generation script is running
        pass


    def get_observation(self):
        self.sm_imsi_metrocs = {}
        for sm in ['mac', 'rlc', 'pdcp']:
            self.sm_imsi_metrocs[sm] = get_metrics(sm)


    def calculate_reward(self):
        pass


    def calculate_state(self):
        # reading state by reading from the json files
        self.get_observation()

        # process the per-imsi information 
        # 
        return None

    def apply_action(self, action):
        # editing the json file 
        # calling the slice_ctrl --create to enforce the decision
        pass


    def reward_caculation(self):
        state = self.calculate_state()



    def step(self, action):
        self.calculate_state()

