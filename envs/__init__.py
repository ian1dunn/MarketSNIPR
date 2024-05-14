from gymnasium.envs.registration import register

register(
     id="envs/MarketEnv-v0",
     entry_point="envs.market_env:MarketEnv",
     max_episode_steps=300,
)