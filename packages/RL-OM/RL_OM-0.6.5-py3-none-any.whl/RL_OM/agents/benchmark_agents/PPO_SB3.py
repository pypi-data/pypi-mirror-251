# AUTOGENERATED! DO NOT EDIT! File to edit: ../../../nbs/agents/benchmark_agents/99_TEMP_PPO_SB3.ipynb.

# %% auto 0
__all__ = ['PPOAgent', 'PPOPolicy']

# %% ../../../nbs/agents/benchmark_agents/99_TEMP_PPO_SB3.ipynb 3
# General libraries:
import numpy as np
from scipy.stats import norm
from tqdm import tqdm

# Mushroom libraries
from mushroom_rl.core import Agent

# %% ../../../nbs/agents/benchmark_agents/99_TEMP_PPO_SB3.ipynb 5
class PPOAgent(Agent):

    train_directly=True

    """_summary_
    """

    def __init__(self,
                    mdp_info,
                    mdp,

                    ):

        print("initializing PPO agent")

        mdp._mdp_info.horizon = mdp.demand.shape[0]
        mdp.reset(0)

        policy = PPOPolicy(

                        )
        
        if agent_name is None:
            self.name = 'PPO_SB3_Agent'
        else:
            self.name = agent_name
        
        self.train_directly=True
        # self.train_mode="direct" # try without this first

        super().__init__(mdp_info, policy)
    
    def fit(self, features=None, demand=None):
        assert isinstance(demand, np.ndarray)
        assert demand.ndim == 2

        self.policy.set_params(demand, self._preprocessors[0])

class PPOPolicy():
    """
    

    """

    

    def draw_action(self, input):

        """
        Note: only designed for single product case
        """

        for preprocessor in self.preprocessors:
            # input must be a vector containing the inventory and the pipeline vector
            input = preprocessor(input)
        
        # print(input)
        # breakpoint()
        

        return XXX


    def reset(self):
        pass
