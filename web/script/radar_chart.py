import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np


def normalize_data(data, max_values):
    return [value / max_value for value, max_value in zip(data, max_values)]


def radar_chart(ax, data, labels, title, color):
    # データの数
    num_vars = len(data)
    # 360度をデータの数で等分する
    angles = np.linspace(0, 2 * np.pi, num_vars, endpoint=False).tolist()
    # 最初のデータを再度リストに追加して、ループを閉じる
    data += data[:1]
    angles += angles[:1]
    # レーダーチャートの描画
    ax.fill(angles, data, color=color, alpha=0.25)
    ax.set_yticklabels([])  # ラベルを非表示にする
    ax.set_xticks(angles[:-1])
    ax.set_xticklabels(labels)
    # タイトルの設定
    ax.set_title(title)
    # グリッドの表示
    ax.grid(True)


def main_radarChart(age, sex, data2):
    if 18 <= age <= 29:
        if sex == "男":
            A = [2650, 65, 74, 381, 8]
        else:
            A = [2000, 50, 56, 288, 7]
    elif 30 <= age <= 49:
        if sex == "男":
            A = [2700, 65, 75, 389, 8]
        else:
            A = [2050, 50, 57, 295, 7]
    elif 50 <= age <= 64:
        if sex == "男":
            A = [2600, 65, 73, 374, 8]
        else:
            A = [1950, 50, 54, 281, 7]
    print(A)
    # カロリー等栄養素の最大値
    max_values = [4000, 100, 120, 500, 50]
    # それぞれの項目における最大値を適切に設定
    # 新しいデータとラベル
    data1 = A
    labels = ["energy", "protein", "lipid", "carbohydrate", "salt"]
    # データを最大値で正規化
    normalized_data1 = normalize_data(data1, max_values)
    normalized_data2 = normalize_data(data2, max_values)
    # レーダーチャートの作成
    fig, ax = plt.subplots(subplot_kw=dict(polar=True), figsize=(8, 8))
    # 1つ目のデータセット
    radar_chart(ax, normalized_data1, labels, "nutrition 1", "skyblue")
    # 2つ目のデータセット
    radar_chart(ax, normalized_data2, labels, "nutrition", "lightcoral")
    plt.savefig("./static/img/sin.png")


# if __name__ == "__main__":
#     data2 = [1500, 40, 60, 250, 20]
#     age = int(input())
#     sex = input()
#     main_radarChart(age,sex,data2)
#     plt.show()
