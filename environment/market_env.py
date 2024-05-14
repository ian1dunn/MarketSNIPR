import gymnasium as gym
import numpy as np
import pandas as pd
from gymnasium import spaces


class MarketEnv(gym.Env):
    def __init__(self, dataframes: list[pd.DataFrame], initial_balance=10000):
        super(MarketEnv, self).__init__()

        self.dataframes = dataframes
        self.initial_balance = initial_balance
        self.current_step = 0
        self.cash_balance = initial_balance
        self.shares_owned = np.zeros(len(dataframes))

        # Observation space: [cash_balance, shares_owned, asset_info]
        num_assets = len(dataframes)
        asset_info_length = 1 + len(dataframes[0].columns) - 1  # Closing price + technical indicators
        low_obs = np.array([0] * (1 + num_assets + num_assets * asset_info_length), dtype=np.float32)
        high_obs = np.array([np.inf] * (1 + num_assets + num_assets * asset_info_length), dtype=np.float32)
        self.observation_space = spaces.Box(low=low_obs, high=high_obs, dtype=np.float32)

        # Action space: one integer per asset TODO bound it to avoid selling too many stocks or buying too many shares
        self.action_space = spaces.Box(low=-np.inf, high=np.inf, shape=(num_assets,), dtype=np.int32)

        self.reset()

    def reset(self):
        self.current_step = 0
        self.cash_balance = self.initial_balance
        self.shares_owned = np.zeros(len(self.dataframes))
        return self._get_observation()

    def _get_observation(self):
        asset_info = []
        for df in self.dataframes:
            row = df.iloc[self.current_step]
            closing_price = row['Close']
            indicators = row.drop('Close').values
            asset_info.append(closing_price)
            asset_info.extend(indicators)

        observation = [self.cash_balance] + list(self.shares_owned) + asset_info
        return np.array(observation, dtype=np.float32)

    def _get_portfolio_value(self):
        asset_values = [df.iloc[self.current_step]['Close'] * self.shares_owned[i] for i, df in
                        enumerate(self.dataframes)]
        return self.cash_balance + sum(asset_values)

    def step(self, action):
        # Perform the trades
        for i, act in enumerate(action):
            if act > 0:  # Buy shares
                num_shares_to_buy = act
                cost = num_shares_to_buy * self.dataframes[i].iloc[self.current_step]['Close']
                if self.cash_balance >= cost:
                    self.cash_balance -= cost
                    self.shares_owned[i] += num_shares_to_buy
            elif act < 0:  # Sell shares
                num_shares_to_sell = -act
                if self.shares_owned[i] >= num_shares_to_sell:
                    self.cash_balance += num_shares_to_sell * self.dataframes[i].iloc[self.current_step]['Close']
                    self.shares_owned[i] -= num_shares_to_sell

        # Calculate reward
        portfolio_value = self._get_portfolio_value()
        reward = portfolio_value - self._previous_portfolio_value
        self._previous_portfolio_value = portfolio_value

        self.current_step += 1
        done = self.current_step >= len(self.dataframes[0]) - 1
        info = {}

        return self._get_observation(), reward, done, info
