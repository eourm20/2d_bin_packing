
class bin_packing_2d_env:
    def __init__(self, items, bin_size):
        self.items = items
        self.bin_size = bin_size
        self.state = (0, 0, 0)
        self.action_space = spaces.Discrete(2)
        self.observation_space = spaces.Box(low=0, high=1, shape=(len(items), bin_size[0], bin_size[1]), dtype=np.int8)
        self.reset()

    def step(self, action):
        if action == 0:
            self.state = (self.state[0] + 1, self.state[1], self.state[2])
        elif action == 1:
            self.state = (self.state[0] + 1, self.state[1] + self.items[self.state[0]][0], self.state[2] + self.items[self.state[0]][1])
        else:
            raise ValueError("Invalid action: " + str(action))
        done = self.state[0] == len(self.items)
        reward = 0
        if done:
            reward = self.state[2]
        return self._get_obs(), reward, done, {}

    def reset(self):
        self.state = (0, 0, 0)
        return self._get_obs()

    def _get_obs(self):
        obs = np.zeros((len(self.items), self.bin_size[0], self.bin_size[1]), dtype=np.int8)
        for i in range(self.state[0]):
            obs[i, :, :] = 1
        return obs

    def render(self, mode='human'):
        print(self.state)

    def close(self):
        pass