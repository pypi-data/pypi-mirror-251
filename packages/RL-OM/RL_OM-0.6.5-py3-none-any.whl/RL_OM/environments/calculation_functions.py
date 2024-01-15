# AUTOGENERATED! DO NOT EDIT! File to edit: ../../nbs/environments/10_calculation_functions.ipynb.

# %% auto 0
__all__ = ['normalize_reward', 'eoq_qr_calculations_single_action', 'eoq_qr_calculations_qr_action',
           'mpfc_calculations_ss_action', 'nv_calculations', 'get_fixed_ordering_cost']

# %% ../../nbs/environments/10_calculation_functions.ipynb 4
# General libraries:
import numpy as np
import time

# %% ../../nbs/environments/10_calculation_functions.ipynb 7
# helper functions:
def normalize_reward(self, reward):
    if self.normalize_reward:
        # print(np.sum(self.holding_cost*self.inventory_cap))
        # print(np.sum(self.fixed_ordering_cost))
        reward_norm = reward / np.maximum(np.sum(self.holding_cost*self.inventory_cap), np.sum(self.fixed_ordering_cost))
        reward_norm = np.clip(reward_norm, -5, 0)
    else:
        reward_norm = reward
    return reward_norm

# %% ../../nbs/environments/10_calculation_functions.ipynb 8
def eoq_qr_calculations_single_action(self, action):

    # TODO Think about naming of the function

    fixed_ordering_cost_step = get_fixed_ordering_cost(self, action, positive_only = True)

    # todo: add variable ordering cost:
        # variable cost positive order ...
        # variable cost negative order would build on overage cost

    if self.use_order_pipeline:
        orders_arriving = self.order_pipeline[:,-1]
            # Move elements one slot to the right in order_pipeline
        self.order_pipeline[:, 1:] = self.order_pipeline[:, :-1]
        self.order_pipeline[:, 0] = action
    else:
        orders_arriving = action

    self.inventory += orders_arriving # first, the order will be added to inventory (meaning lead-time is 0)

    self.inventory = np.maximum(self.inventory, 0) # inventory cannot be negative

    self.inventory = np.minimum(self.inventory, self.inventory_cap) # inventory cannot be higher than inventory_cap

    self.inventory -= self.demand[self.period, :] # Then demand is subtracted from inventory

    outages = np.where(self.inventory < 0, np.abs(self.inventory), 0)
    penalty_cost_step = self.underage_cost * outages.sum()

    self.inventory = np.maximum(self.inventory, 0) # inventory cannot be negative
    holding_cost_step = self.holding_cost * self.inventory

    total_cost_step = fixed_ordering_cost_step + penalty_cost_step + holding_cost_step
    reward = - total_cost_step.sum() # maximize negative cost (sum over all products)


    # print(f"fixed_ordering_cost_step: {fixed_ordering_cost_step}")
    # print(f"penalty_cost_step: {penalty_cost_step}")
    # print(f"holding_cost_step: {holding_cost_step}")
    # print(f"total_cost_step: {total_cost_step}")

    reward_norm = normalize_reward(self, reward)

    # # print(f"reward_norm: {reward_norm}")
    # if self.normalize_reward:
    #     time.sleep(2)

    info = dict(
            inventory = self.inventory,
            demand = self.demand[self.period, :],
            action = action,
            order = action,
            penalty = penalty_cost_step,
            holding = holding_cost_step,
            fixed_ordering = fixed_ordering_cost_step,
    )

    self.period += 1

    return reward_norm, info

# %% ../../nbs/environments/10_calculation_functions.ipynb 9
def eoq_qr_calculations_qr_action(self, action):

    # TODO Think about naming of the function
    
    # print("inventory: ", self.inventory)
    # print("pipeline: ", self.order_pipeline)
    # print("action: ", action)
    # print("demand: ", self.demand[self.period, :])

    if len(action.shape) == 1:
        r = action[0]
        q = action[1]
    else:
        r = action[0][0]
        q = action[0][1]

    order = np.where(self.inventory <= r, q, 0)

    fixed_ordering_cost_step = get_fixed_ordering_cost(self, order, positive_only = True)

    if self.use_order_pipeline:
        orders_arriving = self.order_pipeline[:,-1].copy()
            # Move elements one slot to the right in order_pipeline
        self.order_pipeline[:, 1:] = self.order_pipeline[:, :-1]
        self.order_pipeline[:, 0] = order
    else:
        orders_arriving = order

    # todo: add variable ordering cost:
        # variable cost positive order ...
        # variable cost negative order would build on overage cost

    inventory_start = self.inventory.copy()

    self.inventory += orders_arriving # first, the order will be added to inventory (meaning lead-time is 0)

    self.inventory = np.maximum(self.inventory, 0) # inventory cannot be negative

    self.inventory = np.minimum(self.inventory, self.inventory_cap) # inventory cannot be higher than inventory_cap

    self.inventory -= self.demand[self.period, :] # Then demand is subtracted from inventory

    outages = np.where(self.inventory < 0, np.abs(self.inventory), 0)
    penalty_cost_step = self.underage_cost * outages.sum()

    self.inventory = np.maximum(self.inventory, 0) # inventory cannot be negative
    holding_cost_step = self.holding_cost * self.inventory

    total_cost_step = fixed_ordering_cost_step + penalty_cost_step + holding_cost_step
    reward = - total_cost_step.sum() # maximize negative cost (sum over all products)

    # print("end inventory: ", self.inventory)
    # print("end pipeline: ", self.order_pipeline)

    # print(f"fixed_ordering_cost_step: {fixed_ordering_cost_step}")
    # print(f"penalty_cost_step: {penalty_cost_step}")
    # print(f"holding_cost_step: {holding_cost_step}")
    # print(f"total_cost_step: {total_cost_step}")


    reward_norm = normalize_reward(self, reward)
    
    # print(f"reward_norm: {reward_norm}")

    # if self.normalize_reward:
    #     time.sleep(2)

    info = dict(
            inventory = inventory_start,
            demand = self.demand[self.period, :],
            action = action,
            order = order,
            penalty = penalty_cost_step,
            holding = holding_cost_step,
            fixed_ordering = fixed_ordering_cost_step,
    )

    self.period += 1

    return reward_norm, info

# %% ../../nbs/environments/10_calculation_functions.ipynb 10
def mpfc_calculations_ss_action(self, action):

    # TODO Think about naming of the function

    if len(action.shape) == 1:
        s = action[0]
        S = action[1]
    else:
        s = action[0][0]
        S = action[0][1]

    total_inventory_position= self.inventory + np.sum(self.order_pipeline, axis = 1)
    q = S - total_inventory_position

    # print("inventory:",  self.inventory)
    # print("order pipeline:", self.order_pipeline)
    # print("total_inventory_position:", total_inventory_position)
    # print("S:", S)
    # print("q:", q)

    order = np.where(self.inventory <= s, q, 0)

    # print("order:", order)

    fixed_ordering_cost_step = get_fixed_ordering_cost(self, order, positive_only = True)

    if self.use_order_pipeline:
        orders_arriving = self.order_pipeline[:,-1].copy()
            # Move elements one slot to the right in order_pipeline
        self.order_pipeline[:, 1:] = self.order_pipeline[:, :-1]
        self.order_pipeline[:, 0] = order
    else:
        orders_arriving = order

    # todo: add variable ordering cost:
        # variable cost positive order ...
        # variable cost negative order would build on overage cost

    inventory_start = self.inventory.copy()

    self.inventory += orders_arriving # first, the order will be added to inventory (meaning lead-time is 0)

    self.inventory = np.maximum(self.inventory, 0) # inventory cannot be negative

    self.inventory = np.minimum(self.inventory, self.inventory_cap) # inventory cannot be higher than inventory_cap

    self.inventory -= self.demand[self.period, :] # Then demand is subtracted from inventory

    outages = np.where(self.inventory < 0, np.abs(self.inventory), 0)
    penalty_cost_step = self.underage_cost * outages.sum()

    self.inventory = np.maximum(self.inventory, 0) # inventory cannot be negative
    holding_cost_step = self.holding_cost * self.inventory

    total_cost_step = fixed_ordering_cost_step + penalty_cost_step + holding_cost_step
    reward = - total_cost_step.sum() # maximize negative cost (sum over all products)

    reward_norm = normalize_reward(self, reward)

    info = dict(
            inventory = inventory_start,
            demand = self.demand[self.period, :],
            action = action,
            order = order,
            penalty = penalty_cost_step,
            holding = holding_cost_step,
            fixed_ordering = fixed_ordering_cost_step,
    )

    self.period += 1

    return reward_norm, info

# %% ../../nbs/environments/10_calculation_functions.ipynb 11
def nv_calculations(self, action):

    demand = self.demand[self.period, :]
    remaining_demand = demand.copy() - action

    cost = np.zeros(self.num_products)

    cost[remaining_demand > 0] = self.underage_cost * remaining_demand[remaining_demand > 0]
    cost[remaining_demand < 0] = self.overage_cost * np.abs(remaining_demand[remaining_demand < 0])

    reward = -cost.sum()

    reward_norm = normalize_reward(self, reward)
    
    info = dict(
        demand = demand,
        cost = cost
    )

    self.period += 1

    return reward_norm, info

# %% ../../nbs/environments/10_calculation_functions.ipynb 13
def get_fixed_ordering_cost(self, action, positive_only = True):
    """ 
    Returns the fixed ordering cost for the period.

    Parameters
    ----------
    action : array
        The action taken in the period.
    positive_only : bool
        If True, only positive orders will be charged the fixed ordering cost. Otherwise, all non-zero orders will be charged the fixed ordering cost.

    Returns
    -------
    fixed_ordering_cost : array
        The fixed ordering cost for the period per product.
    
    """

    if positive_only:
        positive_order = np.where(action > 0, 1, 0)
    else:
        # nonzero = 1, zero = 0
        positive_order = np.where(action != 0, 1, 0)
    return self.fixed_ordering_cost * positive_order
