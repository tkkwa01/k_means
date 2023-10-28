import math
import random

# 2つの特徴点間の直線距離を計算する関数
def calcDistance(v1, v2):
    sum2 = 0
    dim = len(v1)
    for i in range(dim):
        sum2 += ((v1[i] - v2[i]) * (v1[i] - v2[i]))
    return math.sqrt(sum2)


# 初期の代表点を設定する関数
def initCenters(data, k):
    centers = []
    num_points = len(data)
    selected_points = []
    while len(selected_points) < k:
        point_idx = random.randint(0, num_points - 1)
        if point_idx not in selected_points:
            selected_points.append(point_idx)
    for point_idx in selected_points:
        centers.append(data[point_idx])
    return centers

# 各点を最も近い代表点に割り当てる関数
def assignDocs(data, centers):
    clusters = []
    for i in range(len(centers)):
        clusters.append([])
    for i, point in enumerate(data):
        closest_center_idx = -1
        closest_distance = float('inf')
        for j, center in enumerate(centers):
            distance = calcDistance(point, center)
            if distance < closest_distance:
                closest_distance = distance
                closest_center_idx = j
        clusters[closest_center_idx].append(i)
    return clusters

# 代表点を更新する関数
def updateCenters(data, clusters):
    new_centers = []
    for cluster in clusters:
        if len(cluster) == 0:
            continue
        new_center = [0] * len(data[0])
        for point_idx in cluster:
            point = data[point_idx]
            for i in range(len(point)):
                new_center[i] += point[i]
        for i in range(len(new_center)):
            new_center[i] /= len(cluster)
        new_centers.append(new_center)
    return new_centers

def printFormattedCenters(centers):
    for i, center in enumerate(centers):
        print(f'クラスタ{i+1}の代表点: [', end='')
        for j, val in enumerate(center):
            print(f'{val:.2f}', end='')
            if j < len(center) - 1:
                print(', ', end='')
        print(']')

# クラスタ内分散（クラスタの代表点と所属文書の点までの距離の平均）を計算
def calcIntraDist(data, centers, clusters):
    totalAveDist = 0
    sum = 0
    for i, center in enumerate(centers):
        for point_idx in clusters[i]:
            sum += calcDistance2(center, data[point_idx])
    return sum / len(data)

# クラスタ間分散（代表点間の距離の平均）を計算
def calcInterDist(centers):
    sum = 0
    for i in range(len(centers)):
        for j in range(i + 1, len(centers)):
            sum += calcDistance2(centers[i], centers[j])
    return sum / (len(centers) * (len(centers) - 1) // 2)

# データの読み込み
with open('data1.txt', 'r') as f:
    lines = f.readlines()

prefecture_data = []
prefecture_names = []
for line in lines:
    parts = line.strip().split('\t')
    if len(parts) == 3:
        prefecture_names.append(parts[0])
        latitude = float(parts[1])
        longitude = float(parts[2])
        prefecture_data.append([latitude, longitude])

# k-means法でクラスタリング
k = 8
print('step 1. 代表点の初期化')
centers = initCenters(prefecture_data, k)
printFormattedCenters(centers)

while True:
    print('step 2. クラスタ割り当て')
    clusters = assignDocs(prefecture_data, centers)
    for i, cluster in enumerate(clusters):
        print(f"Cluster {i+1}: ", end="")
        for point_idx in cluster:
            print(prefecture_names[point_idx], end=", ")
        print()

    print('step 3. 代表点の更新')
    new_centers = updateCenters(prefecture_data, clusters)
    printFormattedCenters(new_centers)

    if new_centers == centers:
        print('代表点が変化しなかったので処理を終了')
        break

    centers = new_centers

# クラスタリング結果の評価
print('クラスタリング結果評価')
Sintra = calcIntraDist(prefecture_data, centers, clusters)
print('クラスタ内分散:' + str(Sintra))
Sinter = calcInterDist(centers)
print('クラスタ間分散:' + str(Sinter))
print('クラスタリング結果の評価値:' + str(Sinter / Sintra))
