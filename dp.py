from items import load_items
import time

def can_place(bin, item, x, y):
    for i in range(x, x + item[0]):
        for j in range(y, y + item[1]):
            if i >= len(bin) or j >= len(bin[0]) or bin[i][j]:
                return False
    return True

def place(bin, item, x, y):
    for i in range(x, x + item[0]):
        for j in range(y, y + item[1]):
            bin[i][j] = 1

def remove(bin, item, x, y):
    for i in range(x, x + item[0]):
        for j in range(y, y + item[1]):
            bin[i][j] = 0

def pack(bin, items, index=0):
    if index == len(items):
        return 0

    min_bin = float('inf')
    for i in range(len(bin)):
        for j in range(len(bin[0])):
            if can_place(bin, items[index], i, j):
                place(bin, items[index], i, j)
                min_bin = min(min_bin, 1 + pack(bin, items, index + 1))
                remove(bin, items[index], i, j)
    return min_bin

items = load_items(10)  # 아이템의 수를 줄여서 실행 시간을 감소시킵니다.
W = 100  # bin의 너비
H = 200  # bin의 높이
bin = [[0]*H for _ in range(W)]
start = time.time()
print(pack(bin, items))
end = time.time()
print('Execution time:', end-start)
