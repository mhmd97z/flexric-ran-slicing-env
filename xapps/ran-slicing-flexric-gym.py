import json, time
from configs import slice_stats_path
import pandas as pd 

class RanSlicingFlexricGym:
    def __init__(self) -> None:
        # rm imsi_tmsi.txt, tunnel_rnti.txt
        # make sure the exposer and exporter scripts are running
        # make sure the slices are up
        # make sure the ue-slice association script is running
        # make sure the traffic generation script is running
        pass


    def get_observation(self):
        df = pd.read_csv(slice_stats_path)
        print(df)
        

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


if __name__ == '__main__':
    env = RanSlicingFlexricGym()
    env.get_observation()