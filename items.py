import os
import random

def load_items(num_items, iter):
    print(f"Loading items_{num_items}_{iter}.txt")
    try:
        with open(f"items/items{num_items}/items_{num_items}_{iter}.txt", 'r') as f:
            items = []
            for line in f.readlines():
                line = line.strip()
                if line == "":
                    continue
                w, h = line.split()
                items.append((int(w), int(h)))
            if len(items) != num_items:
                raise ValueError(f"items_{num_items}_{iter}.txt does not contain {num_items} items")
            return items
    except FileNotFoundError:
        print(f"items_{num_items}_{iter}.txt not found. Creating...")
        create_items(num_items, iter)
        return load_items(num_items, iter)

def create_items(num_items, iter): # TODO: Create items.txt
    # small(bin 면적의 5%), medium(bin 면적의 15%), large(bin 면적의 25%) = 6:3:1
    # small item
    create_category(num_items, 0, 0.10, 0.6)
    # medium item
    create_category(num_items, 0.10, 0.20, 0.3)
    # large item
    create_category(num_items, 0.20, 0.30, 0.1)
    
    # 모든 item을 섞어서 저장
    with open('items/items.txt', 'r') as f:
        lines = f.readlines()
    random.shuffle(lines)

    # version에 대한 items 저장
    with open(f'items/items{num_items}/items_{num_items}_{iter}.txt', 'w') as f:
        f.writelines(lines)
    
    # 기존 items.txt 삭제
    os.remove('items/items.txt')
    print(f"{iter}번째 items_{num_items}.txt 생성 완료")
        

def create_category(all_num, pre_category_area_ratio, category_area_ratio, category_num_ratio):
    # 모든 Bin의 너비는 100, 높이는 200으로 고정
    W = 100
    H = 200
    file = open(f"items/items.txt", 'a')
    category_num = 0
    # w: item의 너비, h: item의 높이
    while True:
        if category_num == all_num*category_num_ratio:
            return
        else:
            w = random.randint(1, 100)
            h = random.randint(1, 200)
            if w*h <= 100*200*category_area_ratio and w*h >= 100*200*pre_category_area_ratio:
                file.write(f"{w} {h}\n")
                category_num += 1
            else:
                continue
            
if __name__ == "__main__":
    create_items(20)
    create_items(50)
    create_items(100)
    create_items(200)
    