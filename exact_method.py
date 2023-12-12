from items import load_items
import time
from pulp import *
import pickle
import argparse

def binsolve(item, num_items, num_bins, W, H):
    # item = [(w, h), ...]
    w = [item[0] for item in item]
    h = [item[1] for item in item]
    

    # 문제를 정의합니다.
    prob = LpProblem("2D_Bin_Packing", LpMinimize)

    # 변수 정의
    # v_k: k번째 bin에 item이 할당되었는지 여부를 나타내는 이진 변수
    v = LpVariable.dicts("v", [k for k in range(num_bins)], 0, 1, LpInteger)

    # z_ik: i번째 item이 k번째 bin에 할당되었는지 여부를 나타내는 이진 변수
    z = LpVariable.dicts("z", [(i,k) for i in range(num_items) for k in range(num_bins)], 0, 1, LpInteger)

    # a_(ij,c): i번째 item과 j번째 item이 서로 overlap되는지 확인하는 조건식의 참 여부를 나타내는 이진 변수
    a = LpVariable.dicts("a", [(i,j,c) for i in range(num_items) for j in range(num_items) for c in range(1, 5)], 0, 1, LpInteger)

    # x_i, y_i: coordinates of the item i in the bin (x_i, y_i ∈ N), the option can be relaxed (x_i, y_i ∈ R+)
    x = LpVariable.dicts("x", [i for i in range(num_items)], 0, W, LpInteger)
    y = LpVariable.dicts("y", [i for i in range(num_items)], 0, H, LpInteger)
    
    # 목표 함수를 정의
    prob += lpSum([v[k] for k in range(num_bins)])
    
    # 제약 조건을 추가
    # (1) 각 item은 오직 하나의 bin에만 담길 수 있다.
    for i in range(num_items):
        prob += lpSum([z[(i,k)] for k in range(num_bins)]) == 1
    
    # (2) 사용하지 않는 bin에는 item을 담을 수 없다.
    for k in range(num_bins):
        prob += lpSum([z[(i,k)] for i in range(num_items)]) <= num_items * v[k]

    # (3) bin k에 담긴 item은 bin의 dimension을 초과할 수 없다.
    for i in range(num_items):
        prob += x[i] + w[i] <= W
        prob += y[i] + h[i] <= H
    
    # (4) 동일한 bin에 담긴 item들은 서로 overlap 할 수 없다.
    M = max(W, H) + 1  # big-M method
    for i in range(num_items):
        for j in range(i+1, num_items):
            for k in range(num_bins):
                prob += x[i] + w[i] <= x[j] + M * (3 - z[(i,k)] - z[(j,k)] - a[(i,j,1)])
                prob += x[j] + w[j] <= x[i] + M * (3 - z[(i,k)] - z[(j,k)] - a[(i,j,2)])
                prob += y[i] + h[i] <= y[j] + M * (3 - z[(i,k)] - z[(j,k)] - a[(i,j,3)])
                prob += y[j] + h[j] <= y[i] + M * (3 - z[(i,k)] - z[(j,k)] - a[(i,j,4)])
                prob += lpSum([a[(i,j,c)] for c in range(1, 5)]) >= 1
                
    # (5) item의 edge는 bin의 edge와 평행해야 한다.
    # 이미 정의 됨=> 정수로만 표현하면 됨
    
    # 문제 풀기
    # prob.solve(PULP_CBC_CMD(msg=False, timeLimit=1800))
    prob.solve()

    print("solve 완료!!")
    # 결과를 출력
    if LpStatus[prob.status] == 'Optimal':
        bins_used = sum([v[k].varValue for k in range(num_bins)])
        print("사용된 bins 개수: {}".format(bins_used))
        # 'prob' 객체를 'prob.pkl' 파일에 저장합니다.
        with open(f'prob_LP_{num_items}.pkl', 'wb') as f:
            pickle.dump(prob, f)
        print(f"prob_LP_{num_items}.pkl 저장 완료")
    else:
        print("최적해 찾지 못함..")
        


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--num_items',dest="num_items", type=int, default=20)
    args = parser.parse_args()
    bin_width = 100
    bin_height = 200
    num_items = args.num_items
    num_bins = num_items # bin의 개수는 item의 개수보다 작거나 같음
    item = load_items(num_items)
    time_start = time()
    binsolve(item, num_items, num_bins, bin_width, bin_height)
    time_end = time()
    print(f"{num_items}개 item 실험 완료")
    print("걸린 시간: {}".format(time_end - time_start))
    
    