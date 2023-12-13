import gym
import numpy as np
from gym import spaces
import matplotlib.pyplot as plt
import matplotlib.patches as patches
import os

from items import load_items

class BinPacking2DEnv(gym.Env):
    def __init__(self, item, category_color, num_items, bin_width, bin_height):
        super(BinPacking2DEnv, self).__init__()
        self.bin_size = (bin_width, bin_height)
        self.category_color = category_color
        self.num_items = num_items
        self.items = item
        self.item_index = 0
        self.state = np.zeros(self.bin_size)
        self.action_space = spaces.Discrete(self.bin_size[0] * self.bin_size[1])  # x, y position
        self.observation_space = spaces.Box(low=0, high=1, shape=self.bin_size)
    
    def step(self, action):
        x = action // self.bin_size[1]
        y = action % self.bin_size[1]
        item = self.items[self.item_index]
        reward = self.place_item(item, x, y)
        self.item_index += 1
        done = self.item_index == len(self.items)
        return self.state, reward, done, {}

    def reset(self):
        self.state = np.zeros(self.bin_size)
        self.item_index = 0
        return self.state

    def render(self, step, mode='human'):
        fig, ax = plt.subplots(1, 1, figsize=(5, 5))

        ax.set_xlim([0, self.bin_size[0]])
        ax.set_ylim([0, self.bin_size[1]])
        ax.set_aspect('equal')
        ax.set_title("Bin")  
        ax.set_xticks([])
        ax.set_yticks([])

        for i in range(self.num_items):
            x = i // self.bin_size[1]
            y = i % self.bin_size[1]
            item = self.items[i]
            if np.any(self.state[x:x+item[0], y:y+item[1]] == 1):  # if the item is placed
                color = self.category_color[i]
                rect = patches.Rectangle((x, y), item[0], item[1], fill=True, color=color, alpha=0.6)
                ax.add_patch(rect)
                ax.text(x + item[0]/2, y + item[1]/2, str(i+1), ha='center', va='center')

        plt.tight_layout()
        if not os.path.exists('DRL_result/render'):
            os.makedirs('DRL_result/render')
        plt.savefig(f'DRL_result/render/bin{step}.png')
        plt.close(fig)

    def place_item(self, item, x, y):
        # Check if the item fits within the bin dimensions
        if x + item[0] > self.bin_size[0] or y + item[1] > self.bin_size[1]:
            return -1  # item cannot be placed

        # Check if the space is already occupied
        if np.any(self.state[x:x+item[0], y:y+item[1]] == 1):
            return -1  # space is already occupied

        # Check for overlap with existing items
        for other_x in range(x, x + item[0]):
            for other_y in range(y, y + item[1]):
                if self.state[other_x, other_y] == 1:
                    return -1  # overlap

        # If all checks pass, place the item
        self.state[x:x+item[0], y:y+item[1]] = 1
        return item[0] * item[1]  # reward is the area of the item


if __name__ == '__main__':
    num_items = 20
    bin_width = 100
    bin_height = 200
    num_bins = num_items # bin의 개수는 item의 개수보다 작거나 같음
    item, category_color = load_items(num_items, 0)

    # Create environment
    env = BinPacking2DEnv(item, category_color, num_items, bin_width, bin_height)

    