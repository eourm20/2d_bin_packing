from rectpack import newPacker
from items import load_items
import time
import os

import matplotlib.pyplot as plt
import matplotlib.patches as patches
import pandas as pd

def packbins(items, num_items, W, H, iter):
    time_start = time.time()
    packer = newPacker(rotation=False)

    # Add the rectangles to packing queue
    for r in items:
        packer.add_rect(*r)
    # Add the bins where the rectangles will be placed
    packer.add_bin(W, H, count=num_items)
    
    # Pack
    packer.pack()
    time_end = time.time()
    all_rects = packer.rect_list()
    
    print(f"{num_items}개 item {iter}번째 실험 완료")
    print(f"사용된 bins 개수: {len(packer)}")
    with open(f'heuristic_result/items{num_items}/H_{num_items}_{iter}.txt', 'w') as f:
        f.write(f"binID x y w h\n")
        for rect in all_rects:
            f.write(f"{rect[0]} {rect[1]} {rect[2]} {rect[3]} {rect[4]}\n")
        f.write(f"\nNumber of bins used: {len(packer)}\n")
        f.write(f"Time: {time_end - time_start}")
    
def bin_render(path):
    file_name = path.split('/')[-1].split('.')[0]
    with open(path, 'r') as f:
        lines = f.readlines()
    lines = lines[1:]
    lines = lines[:-3]
    lines = [line.split() for line in lines]
    data = pd.DataFrame(lines, columns=['binID', 'x', 'y', 'w', 'h'])
    data = data.astype({'binID': int, 'x': int, 'y': int, 'w': int, 'h': int})
    used_bins = data['binID'].unique()
    num_items = len(data)
    fig, axs = plt.subplots(1, len(used_bins), figsize=(5*len(used_bins), 5))
    
    for bin_id, ax in enumerate(axs):
        ax.set_xlim(0, 100)
        ax.set_ylim(0, 200)
        ax.set_aspect('equal')
        ax.set_title(f"Bin {bin_id}")
        ax.set_xticks([])
        ax.set_yticks([])
        
        bin_data = data[data['binID'] == bin_id]
        for _, row in bin_data.iterrows():
            global_index = data[(data['x'] == row['x']) & (data['y'] == row['y']) & (data['w'] == row['w']) & (data['h'] == row['h'])].index[0]  # 추가된 부분
            ax.add_patch(patches.Rectangle((row['x'], row['y']), row['w'], row['h'], fill=True, color='skyblue', alpha=0.6))
            ax.text(row['x'] + row['w']/2, row['y'] + row['h']/2, str(global_index+1), ha='center', va='center')  # 수정된 부분
    
    plt.tight_layout()
    save_path = f'heuristic_result/render/items{num_items}'
    if not os.path.exists(save_path):
        os.makedirs(save_path)
    plt.savefig(f'heuristic_result/render/items{num_items}/{file_name}.png')
    plt.close()
        
        
        
if __name__ == '__main__':
    bin_width = 100
    bin_height = 200
    # num_items = 20
    # num_items = 50
    # num_items = 100
    # num_items = 200
    '''
    # 100번 test 실행
    for i in range(100):
        items = load_items(num_items, i)
        bins_used = packbins(items, num_items, bin_width, bin_height, i)
    '''
    # bin_render('heuristic_result/items20/H_20_5.txt')
    # bin_render('heuristic_result/items50/H_50_5.txt')
    bin_render('heuristic_result/items100/H_100_5.txt')
    
