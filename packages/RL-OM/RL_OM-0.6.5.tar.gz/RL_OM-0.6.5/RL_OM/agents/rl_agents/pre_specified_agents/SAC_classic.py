# AUTOGENERATED! DO NOT EDIT! File to edit: ../../../../nbs/agents/rl_agents/pre_specified_agents/11_SAC_classic.ipynb.

# %% auto 0
__all__ = ['SACClassic']

# %% ../../../../nbs/agents/rl_agents/pre_specified_agents/11_SAC_classic.ipynb 4
# General libraries
import numpy as np

# Torch
import torch
import torch.nn as nn
import torch.nn.functional as F
import torch.optim as optim

# Networks
from ...networks.critics import CriticNetworkStateAction
from ...networks.actors import ActorNetwork

# Algorithms
from mushroom_rl.algorithms.actor_critic.deep_actor_critic import SAC

# Processors
from ...processors.processors import HybridToContinuous


# %% ../../../../nbs/agents/rl_agents/pre_specified_agents/11_SAC_classic.ipynb 5
class SACClassic():

    """
    Soft Actor Critic (SAC) agent with hybrid action, both based on Gaussian. The binary action is 
    0 if the output of the network is less or equal than 0, and 1 otherwise.

    Args:
        mdp_info (MDPInfo): Contains relevant information about the environment.
        learning_rate_actor (float): Learning rate for the actor.
        learning_rate_critic (float): Learning rate for the critic.
        learning_rate_alpha (float): Learning rate for the temperature parameter.
        initial_replay_size (int): Number of transitions to save in the replay buffer during startup.
        max_replay_size (int): Maximum number of transitions to save in the replay buffer.
        batch_size (int): Number of transitions to sample each time experience is replayed.
        n_features (int): Number of features for the hidden layers of the networks.
        warmup_transitions (int): Number of transitions to replay before starting to update the networks.
        lr_alpha (float): Learning rate for the temperature parameter.
        tau (float): Parameter for the soft update of the target networks.
        optimizer (torch.optim): Optimizer to use for the networks.
        squeeze_output (bool): Whether to squeeze the output of the actor network or not.
        use_cuda (bool): Whether to use CUDA or not. If True and not available, it will use CPU.
        agent_name (str): Name of the agent. If set to None will use some default name.

    """

    def __init__(
            self,
            mdp_info,
            learning_rate_actor = 3e-4,
            learning_rate_critic = None,
            initial_replay_size = 64,
            max_replay_size = 50000,
            batch_size = 64,
            n_features = 64,
            warmup_transitions = 100,
            lr_alpha = 3e-4,
            tau = 0.005,
            log_std_min = -20,
            log_std_max = 2,
            target_entropy = None,
            optimizer = optim.Adam,
            squeeze_output = True,
            use_cuda = True,
            agent_name = None): 
        
        use_cuda = use_cuda and torch.cuda.is_available()

        input_shape = mdp_info.observation_space.shape
        actor_output_shape = (mdp_info.action_space.shape[0],) 

        if learning_rate_critic is None:
            learning_rate_critic = learning_rate_actor

        actor_mu_params = dict(network=ActorNetwork,
                                n_features=n_features,
                                input_shape=input_shape,
                                output_shape=actor_output_shape,
                                use_cuda=use_cuda)

        actor_sigma_params = dict(network=ActorNetwork,
                                    n_features=n_features,
                                    input_shape= input_shape,
                                    output_shape=actor_output_shape,
                                    use_cuda=use_cuda)
        
        actor_optimizer = {'class': optimizer,
                    'params': {'lr': learning_rate_actor}} 
        
        critic_input_shape = (input_shape[0] + actor_output_shape[0],)
        critic_params = dict(network=CriticNetworkStateAction,
                        optimizer={'class': optim.Adam,
                                'params': {'lr': learning_rate_critic}}, 
                        loss=F.mse_loss,
                        n_features=n_features,
                        input_shape=critic_input_shape,
                        output_shape=(1,),
                        squeeze_output=squeeze_output,
                        use_cuda=use_cuda)
        
        self.agent = SAC(mdp_info, actor_mu_params, actor_sigma_params,
                    actor_optimizer, critic_params, batch_size, initial_replay_size,
                    max_replay_size, warmup_transitions, tau, lr_alpha, log_std_min, log_std_max, target_entropy,
                    critic_fit_params=None)
        
        if agent_name is None:
            self.agent.name = 'SAC_classic'
        else:
            self.agent.name = agent_name

    def __getattr__(self, attr):
        return getattr(self.agent, attr)
