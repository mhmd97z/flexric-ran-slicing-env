import json, time, gym
import pandas as pd
from configs import slice_stats_path
from utils import get_prb_count, set_slice, get_slicing_scheme
from metrics import metrics_exporter_slice_mapping as slice_metrics
import xapp_sdk as ric


class RanSlicingFlexricGym(gym.Env):
    def __init__(self):
        # get system configs
        self.prb_count = int(get_prb_count() / 2) # based on flexric api, the action resolution is 2 prbs
        self.metrics_count = len(slice_metrics)
        self.initial_slicing_scheme = get_slicing_scheme()
        self.slice_count = int(self.initial_slicing_scheme['num_slices'])
        self.slice_ids = [item["id"] for item in self.initial_slicing_scheme["slices"]]
        assert(len(self.slice_ids) == self.slice_count)

        # set action and spaces environments
        self.action_space = gym.spaces.Box(low=0, high = self.prb_count,
                                        shape=(self.slice_count,), dtype=int)
        self.observation_space = gym.spaces.Box(low=0, high=+float('inf'),
                                            shape=(self.metrics_count * self.slice_count,), dtype=float)
        
        # setup ric
        ric.init()
        self.ric = ric
        self.conn = self.ric.conn_e2_nodes()
        
        self.reset()

        # make sure the exposer and exporter scripts are running
        # make sure the slices are up
        # make sure the ue-slice association script is running
        # make sure the traffic generation script is running


    def reset(self):
        set_slice()


    def calculate_reward(self):
        pass


    def calculate_state(self):
        # reading state by reading from the json files
        df = pd.read_csv(slice_stats_path)
        state = []
        for slice_id in self.slice_ids:
            row = df.loc[df['slice_id'] == slice_id]
            state += list(row[list(slice_metrics.keys())].values[0])
        
        return state


    def sanitize_action(self, action):
        sum_a = 0
        for iter, a in enumerate(action):
            if a == 0: # at least one unit of resource needs to be allocated to each slice
                action[iter] = 1
                sum_a += 1
            else:
                sum_a += a

        if sum_a > self.prb_count:
            coef = self.prb_count / sum_a
            for iter, a in enumerate(action):
                action[iter] = int(action[iter] * coef)

        return action


    def apply_action(self, action):
        action = self.sanitize_action(action)
        action_dict = {}
        for iter, slice_id in enumerate(self.slice_ids):
            action_dict[slice_id] = action[iter]
            
        set_slice(decision=action_dict, ric_=self.ric, conn=self.conn)


    def step(self, action):
        state = self.calculate_state()
        self.apply_action(action)

        return state


if __name__ == '__main__':
    env = RanSlicingFlexricGym()
    for action in [[3, 3], [4, 5], [5, 2]]:
        print("applying aciton: ", action)
        env.apply_action(action)
        print("waiting ----- ")
        time.sleep(10)