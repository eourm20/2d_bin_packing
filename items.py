import os
import random

def load_items(num_items, iter):
    print(f"Loading items_{num_items}_{iter}.txt")
    if not os.path.exists('items'):
        os.makedirs('items')
    try:
        with open(f"items/items{num_items}/items_{num_items}_{iter}.txt", 'r') as f:
            items = []
            category_color = []
            for line in f.readlines():
                line = line.strip()
                if line == "":
                    continue
                w, h, color = line.split()
                items.append((int(w), int(h)))
                category_color.append(color)
            if len(items) != num_items:
                raise ValueError(f"items_{num_items}_{iter}.txt does not contain {num_items} items")
            return items, category_color
    except FileNotFoundError:
        print(f"items_{num_items}_{iter}.txt not found. Creating...")
        create_items(num_items, iter)
        return load_items(num_items, iter)

def create_items(num_items, iter): # TODO: Create items.txt
    # small(bin 너비/높이 길이의 0~20%), medium(bin 너비/높이 길이의 20~40%), large(bin 너비/높이 길이의 40~70%) = 7:2:1
    # small item
    create_category(num_items, 0, 0.20, 0.7, "skyblue")
    # medium item
    create_category(num_items, 0.20, 0.40, 0.2, "blue")
    # large item
    create_category(num_items, 0.40, 0.70, 0.1, "navy")
    
    # 모든 item을 섞어서 저장
    with open('items/items.txt', 'r') as f:
        lines = f.readlines()
    random.shuffle(lines)

    # version에 대한 items 저장
    if not os.path.exists(f'items/items{num_items}'):
        os.makedirs(f'items/items{num_items}')
    with open(f'items/items{num_items}/items_{num_items}_{iter}.txt', 'w') as f:
        f.writelines(lines)
    
    # 기존 items.txt 삭제
    os.remove('items/items.txt')
    print(f"{iter}번째 items_{num_items}.txt 생성 완료")
        

def create_category(all_num, pre_category_area_ratio, category_area_ratio, category_num_ratio, category_color):
    # 모든 Bin의 너비는 100, 높이는 200으로 고정
    W = 100
    H = 200
    file = open(f"items/items.txt", 'a')
    # w: item의 너비, h: item의 높이
    for i in range(int(all_num*category_num_ratio)):
        w = random.randint(int(1+(W*pre_category_area_ratio)), int(W*category_area_ratio))
        h = random.randint(int(1+(W*pre_category_area_ratio)), int(H*category_area_ratio))
        file.write(f"{w} {h} {category_color}\n")
            
if __name__ == "__main__":
    create_items(20)
    create_items(50)
    create_items(100)
    create_items(200)
    