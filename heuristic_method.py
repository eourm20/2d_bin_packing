from rectpack import newPacker
from items import load_items
import time
import os
import random

import matplotlib
import matplotlib.pyplot as plt
import matplotlib.patches as patches
matplotlib.use('TKAgg')
import pandas as pd

def packbins(items, category_color, num_items, W, H, iter):
    time_start = time.time()
    packer = newPacker(rotation=False)

    # Pair items and category_color, then shuffle them together
    paired_list = list(zip(items, category_color))
    random.shuffle(paired_list)
    items, category_color = zip(*paired_list)
    
    # Add the rectangles to packing queue
    for r in range(len(items)):
        packer.add_rect(*items[r], rid=r)
    # Add the bins where the rectangles will be placed
    packer.add_bin(W, H, count=num_items)
    
    # Pack
    packer.pack()
    time_end = time.time()
    all_rects = packer.rect_list()
    
    print(f"{num_items}개 item {iter}번째 실험 완료")
    print(f"사용된 bins 개수: {len(packer)}")
    if not os.path.exists(f'heuristic_result/items{num_items}'):
        os.makedirs(f'heuristic_result/items{num_items}')
    with open(f'heuristic_result/items{num_items}/H_{num_items}_{iter}.txt', 'w') as f:
        f.write(f"binID x y w h color\n")
        for rect in all_rects:
            color = category_color[rect[5]]  # rect[5] is the rid, use it as index to get color
            f.write(f"{rect[0]} {rect[1]} {rect[2]} {rect[3]} {rect[4]} {color}\n")
        f.write(f"\nNumber of bins used: {len(packer)}\n")
        f.write(f"Time: {time_end - time_start}")
    
def bin_render(path):
    file_name = path.split('/')[-1].split('.')[0]
    with open(path, 'r') as f:
        lines = f.readlines()
    lines = lines[1:]
    lines = lines[:-3]
    lines = [line.split() for line in lines]
    data = pd.DataFrame(lines, columns=['binID', 'x', 'y', 'w', 'h', 'color'])
    data = data.astype({'binID': int, 'x': int, 'y': int, 'w': int, 'h': int, 'color': str})
    used_bins = data['binID'].unique()
    num_items = len(data)
    fig, axs = plt.subplots(1, len(used_bins), figsize=(5*len(used_bins), 5))
    
    if len(used_bins) == 1:
        axs = [axs]
        
    for bin_id, ax in enumerate(axs):
        ax.set_xlim(0, 100)
        ax.set_ylim(0, 200)
        ax.set_aspect('equal')
        ax.set_title(f"Bin {bin_id}")
        ax.set_xticks([])
        ax.set_yticks([])
        
        bin_data = data[data['binID'] == bin_id]
        for _, row in bin_data.iterrows():
            global_index = data[(data['x'] == row['x']) & (data['y'] == row['y']) & (data['w'] == row['w']) & (data['h'] == row['h'])].index[0]
            ax.add_patch(patches.Rectangle((row['x'], row['y']), row['w'], row['h'], fill=True, color=row['color'], alpha=0.6))
            ax.text(row['x'] + row['w']/2, row['y'] + row['h']/2, str(global_index+1), ha='center', va='center')
    
    plt.tight_layout()
    save_path = f'heuristic_result/render/items{num_items}'
    if not os.path.exists(save_path):
        os.makedirs(save_path)
    plt.savefig(f'heuristic_result/render/items{num_items}/{file_name}.png')
    plt.close()
        
        
        
if __name__ == '__main__':
    bin_width = 100
    bin_height = 200
    num_items_list = [20, 50, 100, 200]
    
    for num_items in num_items_list:
        # 100번 test 실행
        for i in range(100):
            items, category_color = load_items(num_items, i)
            bins_used = packbins(items, category_color, num_items, bin_width, bin_height, i)
    
        bin_render(f'heuristic_result/items{num_items}/H_{num_items}_5.txt')

    
