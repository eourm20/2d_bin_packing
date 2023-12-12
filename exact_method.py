from items import load_items
import time
from pulp import *
import pickle
import argparse
import matplotlib.pyplot as plt
import matplotlib.patches as patches

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
        
def load_prob(num_items, num_bins, item, category_color, bin_width, bin_height):
    with open(f'prob_LP_{num_items}.pkl', 'rb') as f:
        prob = pickle.load(f)
    print(f"사용된 최적의 bins 개수: {prob.objective.value()}")
    print(f"최잭해를 찾는데 걸린 시간: {prob.solutionTime}")
    # 만족되지 않은 제약조건 확인
    check_constraints(prob)

    # 시각화
    visualize_bins(prob, num_items, num_bins, item, category_color, bin_width, bin_height)
    
        
def check_constraints(prob):
    constraints_list = ["제약조건1", "제약조건2", "제약조건3", "제약조건4"]
    for constraint_name in constraints_list:
        for name, constraint in prob.constraints.items():
            if str(name).startswith(constraint_name):
                if constraint.value() < 0:
                    print(f"{name} 제약 조건이 만족되지 않습니다. 값: {constraint.value()}")
    print("제약 조건 확인 완료")
            
def visualize_bins(prob, num_items, num_bins, item, category_color, W, H):
    w = [item[0] for item in item]
    h = [item[1] for item in item]
    
    used_bins = [k for k in range(num_bins) if any([prob.variablesDict()[f"z_({i},_{k})"].varValue == 1 for i in range(num_items)])]
    fig, axs = plt.subplots(1, len(used_bins), figsize=(5*len(used_bins), 5))

    if len(used_bins) == 1:
        axs = [axs]

    for bin_index, k in enumerate(used_bins):
        ax = axs[bin_index]
        ax.set_xlim([0, W])
        ax.set_ylim([0, H])
        ax.set_aspect('equal')
        ax.set_title(f"Bin {bin_index}")  # Here, bin_index starts from 0, so we add 1 to start from 1
        ax.set_xticks([])
        ax.set_yticks([])

        items_in_bin = [i for i in range(num_items) if prob.variablesDict()[f"z_({i},_{k})"].varValue == 1]

        for i in items_in_bin:
            x = prob.variablesDict()[f"x_{i}"].varValue
            y = prob.variablesDict()[f"y_{i}"].varValue
            rect = patches.Rectangle((x, y), w[i], h[i], fill=True, color=category_color[i], alpha=0.6)
            ax.add_patch(rect)
            ax.text(x + w[i]/2, y + h[i]/2, str(i+1), ha='center', va='center')

    plt.tight_layout()
    if not os.path.exists(f'exact_result/render'):
        os.makedirs(f'exact_result/render')
    plt.savefig(f'exact_result/render/items{num_items}.png')
            
if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--num_items',dest="num_items", type=int, default=20)
    args = parser.parse_args()
    bin_width = 100
    bin_height = 200
    num_items = args.num_items
    num_bins = num_items # bin의 개수는 item의 개수보다 작거나 같음
    item, category_color = load_items(num_items, 0)
    # binsolve(item, num_items, num_bins, bin_width, bin_height)
    # print(f"{num_items}개 item 실험 완료")
    
    load_prob(num_items, num_bins, item, category_color, bin_width, bin_height)
    
    