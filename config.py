LOOK_BACK_WINDOW = 14  # 14 or 9, how many days to look back to determine past asset prices

#
# Enviroment & Model Config
#
ENV = "envs/MarketEnv"  # OpenAI gym environment name
SEED = 0  # Sets Gym, PyTorch and Numpy seeds
START_TIMESTEPS = 25e3  # Time steps initial random policy is used
EVAL_FREQ = 5e3  # How often (time steps) we evaluate
MAX_TIMESTEPS = 1e6  # Max time steps to run environment

EXPL_NOISE = 0.1  # Std of Gaussian exploration noise
BATCH_SIZE = 256  # Batch size for both actor and critic
DISCOUNT = 0.99  # Discount factor
TAU = 0.005  # Target network update rate
POLICY_NOISE = 0.2  # Noise added to target policy during critic update
NOISE_CLIP = 0.5  # Range to clip target policy noise
POLICY_FREQ = 2  # Frequency of delayed policy updates

SAVE_MODEL = True  # Save model and optimizer parameters  (action=store_true)
LOAD_MODEL = "./model..."  # Model load file name, "" doesn't load, "default" uses file_name