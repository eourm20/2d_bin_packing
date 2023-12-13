import gym
from stable_baselines3 import DQN, PPO
from stable_baselines3.common.envs import BitFlippingEnv
from RL_env import BinPacking2DEnv
from items import load_items
from stable_baselines3.common.callbacks import BaseCallback, CheckpointCallback

num_items = 20
bin_width = 100
bin_height = 200
num_bins = num_items # bin의 개수는 item의 개수보다 작거나 같음
item, category_color = load_items(num_items, 0)
'''
# Create environment
env = BinPacking2DEnv(item, category_color, num_items, bin_width, bin_height)

# Initialize agent
model = DQN('MlpPolicy', env, verbose=1)

# Train agent
model.learn(total_timesteps=10000)

# Test the trained agent
obs = env.reset()
n_steps = num_items
for step in range(n_steps):
  action, _ = model.predict(obs, deterministic=True)
  print(f"Step {step + 1}")
  print(f"Action: {action}")
  obs, reward, done, info = env.step(action)
  print(f"Reward: {reward}")
  if done:
    print("Goal achieved!")
    break
'''

# 환경을 생성합니다.
env = BinPacking2DEnv(item, category_color, num_items, bin_width, bin_height)

checkpoint_callback = CheckpointCallback(
        save_freq=20000,
        save_path='2d_bin_packing/',
        name_prefix="2d_bin_packing_model"
    )
# PPO 모델을 초기화하고 학습합니다.
model = PPO('MlpPolicy', env, verbose=1,  tensorboard_log="2d_bin_packing/ppo_2dbinpacking_tensorboard/")
model.learn(total_timesteps=100000, progress_bar=True, callback=checkpoint_callback)
model.save("ppo_2dbinpacking")
'''
# 학습한 모델을 테스트합니다.
obs = env.reset()
for _ in range(100):
    action, _states = model.predict(obs)
    obs, rewards, done, info = env.step(action)
    env.render(_)
    if done:
        obs = env.reset()

# 모델을 저장합니다.
model.save("ppo_2dbinpacking")
'''