import os
from pathlib import Path

import cv2
import matplotlib.pyplot as plt
import numpy as np
from PIL import Image

# チラシのサイズの取得


def tirasitm(path):
    def white(img):
        # print(type(img))
        h, w, _ = img.shape
        # print("width: ", w)
        # print("height:", h)

        # チラシのサイズの白紙の線を引く紙
        img_white = np.ones((h, w), np.uint8) * 255
        return img_white
        # print(img_white)
        # plt.plot(), plt.imshow(img_white, cmap='gray', vmin=0, vmax=255)
        # plt.show()

    # ラインのリストを初期化
    def hahu(img, img_white):
        yokoline_list = []
        tateline_list = []

        h, w, _ = img.shape
        if h < 1000:
            h = 400
        else:
            h = h / 2
        # ループ処理　横ラインの情報を格納
        for i in range(5, 10):
            # エッジ処理
            img_gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
            img_after = cv2.Canny(img_gray, 100, 200)
            cv2.imwrite("./draft/sample_after2.png", img_after)
            img2 = img[:, :, ::-1]
            gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
            cv2.imwrite("./draft/gray.jpg", gray)
            img_p = cv2.imread("./draft/gray.jpg")
            img_p2 = img[:, :, ::-1]
            edges = cv2.Canny(gray, 50, 150, apertureSize=3)
            cv2.imwrite("./draft/edges.jpg", edges)
            img_p = cv2.imread("./draft/edges.jpg")
            img_p2 = img[:, :, ::-1]

            # ハフ変換で横ラインを検出

            yokolines = cv2.HoughLinesP(
                edges,
                rho=1,
                theta=np.pi / 180,
                threshold=90,
                minLineLength=i * 20,
                maxLineGap=4,
            )
            # print(yokolines)
            if yokolines is not None:
                yokoline_list.append(yokolines)
            # 縦ラインの情報を格納
        for i in (1, 10):
            img_gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
            img_after = cv2.Canny(img_gray, 100, 200)
            cv2.imwrite("./draft/sample_after2.png", img_after)
            img2 = img[:, :, ::-1]
            gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
            cv2.imwrite("./draft/gray.jpg", gray)
            img_p = cv2.imread("./draft/gray.jpg")
            img_p2 = img[:, :, ::-1]
            edges = cv2.Canny(gray, 50, 150, apertureSize=3)
            cv2.imwrite("./draft/edges.jpg", edges)
            img_p = cv2.imread("./draft/edges.jpg")
            img_p2 = img[:, :, ::-1]

            # ハフ変換縦のライン
            tatelines = cv2.HoughLinesP(
                edges,
                rho=1,
                theta=np.pi / 360,
                threshold=90,
                minLineLength=h / 10,
                maxLineGap=i * h / 200,
            )
            tateline_list.append(tatelines)

        # ラインを格納するリストを初期化
        var_line_list = []
        hoz_line_list = []

        # 検出された垂直ライン（tatelines）をループ処理
        for k in range(len(tateline_list)):
            for line in tateline_list[k]:
                x1, y1, x2, y2 = line[0]
                threshold_slope = 3

                # ラインがほぼ垂直であるかどうかをチェック
                if abs(x1 - x2) < threshold_slope:
                    whiteline = 3
                    img_white = cv2.line(
                        img_white, (x1, y1), (x2, y2), (0, 0, 255), whiteline
                    )
                    var_line_list.append((x1, y1, x2, y2))

            # 垂直ラインをフィルタリングして並び替える
            var_line_list.sort(key=lambda x: (x[1], x[0], x[2], x[3]))
            x1 = 0
            var_line = 0

            for line in var_line_list:
                judge_x1 = line[0]

                # 近くの縦のラインを排除　x
                if abs(judge_x1 - x1) < 2 and var_line_list != []:
                    x1 = judge_x1
                else:
                    x1 = judge_x1
                    var_line += 1
                    # var_line_list.append(line)
        # 検出された水平ライン（yokolines）をループ処理
        for k in range(len(yokoline_list)):
            for line in yokoline_list[k]:
                x1, y1, x2, y2 = line[0]
                threshold_slope = 3

                #  ラインがほぼ水平であるかどうかをチェック
                if abs(y1 - y2) < threshold_slope:
                    whiteline = 3
                    img_white = cv2.line(
                        img_white, (x1, y1), (x2, y2), (0, 0, 255), whiteline
                    )
                    hoz_line_list.append((x1, y1, x2, y2))

            # 水平ラインをフィルタリングして並び替える
            hoz_line_list.sort(key=lambda x: (x[1], x[0], x[2], x[3]))
            y1 = 0
            hoz_line = 0

            for line in hoz_line_list:
                judge_y1 = line[0]

                # ほぼ同じ水平ラインを除外する
                if abs(judge_y1 - y1) < 2 and hoz_line_list != []:
                    y1 = judge_y1
                else:
                    y1 = judge_y1
                    hoz_line += 1
                    # hoz_line_list.append(line)
        # 表示
        # plt.figure(figsize=(5, 5))
        # plt.xticks([]), plt.yticks([])
        # plt.imshow(img[:, :, ::-1])
        # plt.show('')
        cv2.imwrite("./draft/LinePapper.jpg", img_white)
        imgline = cv2.imread("./draft/LinePapper.jpg")
        return imgline

    def hahu2(lineimg, img_white):
        # 画像を読み込む
        image = lineimg

        # 画像をグレースケールに変換
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

        # エッジを検出（Canny法を使用）
        edges = cv2.Canny(gray, 50, 150, apertureSize=3)

        # Hough変換を使用して直線を検出
        lines = cv2.HoughLines(edges, 1, np.pi / 180, threshold=100)

        # 検出した直線を描画するためのコピーを作成
        line_imag = np.copy(img_white)

        # 近接している直線をグループ化する
        grouped_lines = []
        for i in range(len(lines)):
            if i in grouped_lines:
                continue
            group = [i]
            rho1, theta1 = lines[i][0]
            for j in range(i + 1, len(lines)):
                if j in grouped_lines:
                    continue
                rho2, theta2 = lines[j][0]
                # 二つの直線の距離が一定以下であれば、同一グループとみなす
                if np.abs(rho1 - rho2) < 50 and np.abs(theta1 - theta2) < 3.14 / 18:
                    group.append(j)
                    grouped_lines.append(j)
            grouped_lines.append(i)

            # 同一グループの直線の平均を計算
            mean_rho = np.mean([lines[k][0][0] for k in group])
            mean_theta = np.mean([lines[k][0][1] for k in group])

            # 平均直線が斜めの場合、グループ内の適当な直線を代わりに描画
            if np.abs(np.sin(mean_theta)) < 1:
                mean_rho = lines[group[0]][0][0]
                mean_theta = lines[group[0]][0][1]

            # 平均直線を描画
            a = np.cos(mean_theta)
            b = np.sin(mean_theta)
            x0 = a * mean_rho
            y0 = b * mean_rho
            x1 = int(x0 + 1000 * (-b))
            y1 = int(y0 + 1000 * (a))
            x2 = int(x0 - 1000 * (-b))
            y2 = int(y0 - 1000 * (a))
            cv2.line(line_imag, (x1, y1), (x2, y2), (0, 255, 0), 2)

        # 結果を表示
        # plt.imshow(cv2.cvtColor(line_imag, cv2.COLOR_BGR2RGB))
        # cv2.imwrite("hahu.jpg", line_imag)
        # plt.axis('off')
        # plt.show()
        return line_imag

    def crop_and_save(
        image, coordinates, output_folder, output_filename, image_quality=95
    ):
        # 画像をトリミング
        x, y, w, h = coordinates
        cropped = image[y : y + h, x : x + w]

        # 画像保存時のパラメータ
        jpeg_params = [int(cv2.IMWRITE_JPEG_QUALITY), image_quality]

        # トリミングされた画像を保存
        output_path = os.path.join(output_folder, output_filename)
        cv2.imwrite(output_path, cropped, jpeg_params)

    def toriming(line_img, img):
        # 画像を読み込む
        image = line_img

        # 画像をグレースケールに変換
        gray = image

        # エッジを検出（Canny法を使用）
        edges = cv2.Canny(gray, 50, 150, apertureSize=3)

        # 輪郭を検出
        contours, _ = cv2.findContours(
            edges, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE
        )

        # 各輪郭に対して処理を行う
        for i, contour in enumerate(contours):
            # 輪郭を近似
            epsilon = 0.02 * cv2.arcLength(contour, True)
            approx = cv2.approxPolyDP(contour, epsilon, True)

            # 輪郭が四角形であるか確認
            if len(approx) == 4:
                # 四角形の座標を取得
                x, y, w, h = cv2.boundingRect(approx)

                # 画像をトリミング
                cropped = image[y : y + h, x : x + w]

                # トリミングされた画像を保存などの処理を行う
                h, w = cropped.shape[:2]

        # 座標情報を保存
        coordinates_path = "./draft/coordinates.txt"
        with open(coordinates_path, "w") as f:
            for coordinate in contours:
                x, y, w, h = cv2.boundingRect(coordinate)
                f.write(f"{x} {y} {w} {h}\n")

        # 別の画像に同じ座標情報を適用してトリミング
        new_image = img

        # 座標情報を読み込む
        with open(coordinates_path, "r") as f:
            lines = f.readlines()
            for i, line in enumerate(lines):
                x, y, w, h = map(int, line.split())
                crop_and_save(
                    new_image,
                    (x, y, w, h),
                    "cutimages",
                    f"cropped_other_{i}.jpg",
                    95,
                )

        # 結果を表示
        # plt.imshow(new_image)
        # plt.show()

    print(f"パスから画像を読み込みます：{path}")
    img = cv2.imread(path)
    a, b = img.shape[:2]

    if a > 3000 and b > 3000:
        img = cv2.resize(img, (2000, int(2000 * a / b)))
        cv2.imwrite("./draft/test.jpg", img)

    if img is None:
        print(f"エラー：{path} から画像を読み込むことができませんでした")
    # 適切なエラーハンドリングを追加するか、関数からリターンする
    """ if img is None:
        print("Error: Could not read the image.")
    else:
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY) """

    new_folder = "cutimages"
    os.makedirs(new_folder)

    white_img = white(img)
    lineimg = hahu(img, white_img)
    line_img = hahu2(lineimg, white_img)
    toriming(line_img, img)

    file_list = os.listdir("cutimages")
    for i in file_list:
        img_path = os.path.join("./cutimages", i)
        img1 = cv2.imread(img_path)
        w, h = img1.shape[:2]
        if (w < a / 15) or (h < b / 15):
            os.remove(img_path)
        elif w > a / 2 or h > b / 2:
            os.remove(img_path)


if __name__ == "__main__":
    tirasitm("./dir_out/ミリオンショップ江戸や 多摩店/6583727.jpg")
