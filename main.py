import numpy as np
import torch
import gymnasium as gym
import os

import config
from model import td3, utils


# Runs policy for X episodes and returns average reward
# A fixed seed is used for the eval environment
def eval_policy(policy, env_name, seed, eval_episodes=10):
    eval_env = gym.make(env_name)
    eval_env.seed(seed + 100)

    avg_reward = 0.
    for _ in range(eval_episodes):
        state, done = eval_env.reset(), False
        while not done:
            action = policy.select_action(np.array(state))
            state, reward, done, _ = eval_env.step(action)
            avg_reward += reward

    avg_reward /= eval_episodes

    print("---------------------------------------")
    print(f"Evaluation over {eval_episodes} episodes: {avg_reward:.3f}")
    print("---------------------------------------")
    return avg_reward


if __name__ == "__main__":
    file_name = f"TD3_{config.ENV}_{config.SEED}"
    print("---------------------------------------")
    print(f"Policy: TD3, Env: {config.ENV}, Seed: {config.SEED}")
    print("---------------------------------------")

    if not os.path.exists("./results"):
        os.makedirs("./results")

    if config.SAVE_MODEL and not os.path.exists("./models"):
        os.makedirs("./models")

    env = gym.make(config.ENV)

    # Set seeds
    env.seed(config.SEED)
    env.action_space.seed(config.SEED)
    torch.manual_seed(config.SEED)
    np.random.seed(config.SEED)

    state_dim = env.observation_space.shape[0]
    action_dim = env.action_space.shape[0]
    max_action = float(env.action_space.high[0])

    kwargs = {"state_dim": state_dim, "action_dim": action_dim, "max_action": max_action, "discount": config.DISCOUNT,
              "tau": config.TAU, "policy_noise": config.POLICY_NOISE * max_action,
              "noise_clip": config.NOISE_CLIP * max_action, "policy_freq": config.POLICY_FREQ}

    # Target policy smoothing is scaled wrt the action scale
    policy = td3.TD3(**kwargs)

    if config.LOAD_MODEL != "":
        policy_file = file_name if config.LOAD_MODEL == "default" else config.LOAD_MODEL
        policy.load(f"./models/{policy_file}")

    replay_buffer = utils.ReplayBuffer(state_dim, action_dim)

    # Evaluate untrained policy
    evaluations = [eval_policy(policy, config.ENV, config.SEED)]

    state, done = env.reset(), False
    episode_reward = 0
    episode_timesteps = 0
    episode_num = 0

    for t in range(int(config.MAX_TIMESTEPS)):  # TODO remove config, use based on market data length

        episode_timesteps += 1

        # Select action randomly or according to policy
        if t < config.START_TIMESTEPS:  # TODO adjust this to accurately reflect market data length
            action = env.action_space.sample()
        else:
            action = (
                    policy.select_action(np.array(state))
                    + np.random.normal(0, max_action * config.EXPL_NOISE, size=action_dim)
            ).clip(-max_action, max_action)

        # Perform action
        next_state, reward, done, _ = env.step(action)
        done_bool = float(done) if episode_timesteps < env._max_episode_steps else 0

        # Store data in replay buffer
        replay_buffer.add(state, action, next_state, reward, done_bool)

        state = next_state
        episode_reward += reward

        # Train agent after collecting sufficient data
        if t >= config.START_TIMESTEPS:
            policy.train(replay_buffer, config.BATCH_SIZE)

        if done:
            # +1 to account for 0 indexing. +0 on ep_timesteps since it will increment +1 even if done=True
            print(
                f"Total T: {t + 1} Episode Num: {episode_num + 1} Episode T: {episode_timesteps} Reward: {episode_reward:.3f}")
            # Reset environment
            state, done = env.reset(), False
            episode_reward = 0
            episode_timesteps = 0
            episode_num += 1

        # Evaluate episode
        if (t + 1) % config.EVAL_FREQ == 0:
            evaluations.append(eval_policy(policy, config.ENV, config.SEED))
            np.save(f"./results/{file_name}", evaluations)
            if config.SAVE_MODEL:
                policy.save(f"./models/{file_name}")
