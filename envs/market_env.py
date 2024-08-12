import gymnasium as gym
import numpy as np
from gymnasium import spaces

from trading.controller import Controller


class MarketEnv(gym.Env):
    def __init__(self, controller: Controller):
        super(MarketEnv, self).__init__()

        self.controller = controller
        self.initial_balance = self.controller.get_buying_power()
        self.cash_balance = self.initial_balance
        self._previous_portfolio_value = self.controller.get_portfolio_value()

        # Observation space: [cash_balance, shares_owned, asset_info]
        self.num_assets = len(self.controller.get_open_positions())
        self.shares_owned = np.zeros(self.num_assets)
        asset_info_length = 11  # TODO Closing price + technical indicators
        low_obs = np.array([0] * (1 + self.num_assets + self.num_assets * asset_info_length), dtype=np.float32)
        high_obs = np.array([np.inf] * (1 + self.num_assets + self.num_assets * asset_info_length), dtype=np.float32)
        self.observation_space = spaces.Box(low=low_obs, high=high_obs, dtype=np.float32)

        # Action space: one integer per asset TODO bound it to avoid selling too many stocks or buying too many shares
        self.action_space = spaces.Box(low=-5, high=5, shape=(self.num_assets,), dtype=np.int32)

        self.reset()

    def reset(self, seed=None, options=None):
        # We need the following line to seed self.np_random
        super().reset(seed=seed)
        self.controller.reset()
        self.cash_balance = self.initial_balance
        self.shares_owned = np.zeros(self.num_assets)
        return self._get_observation()

    def _get_observation(self):
        asset_info = []
        for pos in self.controller.get_open_positions():
            closing_price, indicators = self.controller.get_position_data(pos)
            asset_info.append(closing_price)
            asset_info.extend(indicators)

        observation = [self.cash_balance] + list(self.shares_owned) + asset_info
        return np.array(observation, dtype=np.float32)

    def step(self, action):  # Occurs at end of each day
        # Perform the trades
        for i, act in enumerate(action):
            closing_price = self.controller.get_position_data(self.controller.positions[i])[0]
            # TODO modify this behavior to limit purchasing
            if act > 0:  # Buy shares
                cost = act * closing_price
                if self.cash_balance >= cost:
                    self.cash_balance -= cost
                    self.shares_owned[i] += act
            elif act < 0:  # Sell shares
                if self.shares_owned[i] >= act:
                    self.cash_balance += act * closing_price
                    self.shares_owned[i] -= act

        # Calculate reward
        portfolio_value = self.controller.get_portfolio_value()
        reward = portfolio_value - self._previous_portfolio_value
        self._previous_portfolio_value = portfolio_value

        done = self.controller.is_done()
        info = {}

        obs = self._get_observation()
        print(f'Observation at step {self.controller.step - 1}: {obs}')
        return obs, reward, done, info
