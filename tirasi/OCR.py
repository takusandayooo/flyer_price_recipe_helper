import argparse
import sys

import cv2
from ppocr_onnx.ppocr_onnx import PaddleOcrONNX


def get_args():
    parser = argparse.ArgumentParser()

    parser.add_argument("--image", type=str, default="test2.png")

    parser.add_argument(
        "--det_model",
        type=str,
        default="./ppocr_onnx/model/det_model/en_PP-OCRv3_det_infer.onnx",
    )
    parser.add_argument(
        "--rec_model",
        type=str,
        default="./ppocr_onnx/model/rec_model/en_PP-OCRv3_rec_infer.onnx",
    )
    parser.add_argument(
        "--rec_char_dict",
        type=str,
        default="./ppocr_onnx/ppocr/utils/dict/en_dict.txt",
    )
    parser.add_argument(
        "--cls_model",
        type=str,
        default="./ppocr_onnx/model/cls_model/ch_ppocr_mobile_v2.0_cls_infer.onnx",
    )

    parser.add_argument(
        "--use_gpu",
        action="store_true",
    )

    args = parser.parse_args()

    return args


class DictDotNotation(dict):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.__dict__ = self


def get_paddleocr_parameter():
    paddleocr_parameter = DictDotNotation()

    # params for prediction engine
    paddleocr_parameter.use_gpu = False

    # params for text detector
    paddleocr_parameter.det_algorithm = "DB"
    paddleocr_parameter.det_model_dir = (
        "./ppocr_onnx/model/det_model/ch_PP-OCRv3_det_infer.onnx"
    )
    paddleocr_parameter.det_limit_side_len = 960
    paddleocr_parameter.det_limit_type = "max"
    paddleocr_parameter.det_box_type = "quad"

    # DB parmas
    paddleocr_parameter.det_db_thresh = 0.3
    paddleocr_parameter.det_db_box_thresh = 0.6
    paddleocr_parameter.det_db_unclip_ratio = 1.5
    paddleocr_parameter.max_batch_size = 10
    paddleocr_parameter.use_dilation = False
    paddleocr_parameter.det_db_score_mode = "fast"

    # params for text recognizer
    paddleocr_parameter.rec_algorithm = "SVTR_LCNet"
    paddleocr_parameter.rec_model_dir = (
        "./ppocr_onnx/model/rec_model/japan_PP-OCRv3_rec_infer.onnx"
    )
    paddleocr_parameter.rec_image_shape = "3, 48, 320"
    paddleocr_parameter.rec_batch_num = 6
    paddleocr_parameter.rec_char_dict_path = (
        "./ppocr_onnx/ppocr/utils/dict/japan_dict.txt"
    )
    paddleocr_parameter.use_space_char = True
    paddleocr_parameter.drop_score = 0.5

    # params for text classifier
    paddleocr_parameter.use_angle_cls = False
    paddleocr_parameter.cls_model_dir = (
        "./ppocr_onnx/model/cls_model/ch_ppocr_mobile_v2.0_cls_infer.onnx"
    )
    paddleocr_parameter.cls_image_shape = "3, 48, 192"
    paddleocr_parameter.label_list = ["0", "180"]
    paddleocr_parameter.cls_batch_num = 6
    paddleocr_parameter.cls_thresh = 0.9

    paddleocr_parameter.save_crop_res = False

    return paddleocr_parameter


# 日本語のOCRをしその返り値はOCR結果と確率、座標の入った配列.midは重心を表している。
def jp_OCR(image_path):
    # PaddleOCR準備
    paddleocr_parameter = get_paddleocr_parameter()

    paddle_ocr_onnx = PaddleOcrONNX(paddleocr_parameter)
    text_str = ""
    if image_path is not None:
        image = cv2.imread(image_path)

        # OCR実施
        dt_boxes, rec_res, time_dict = paddle_ocr_onnx(image)
        # print(rec_res)
        jp_list = []
        for coordinate, text in zip(dt_boxes, rec_res):
            i, t = text
            # print(i,end=" ")
            # print(t)
            # "coordinate":[x1,y1,x2,y2]という形.midは重心の場所を示している。
            tmp = {
                "text": i,
                "probability": t,
                "coordinate": [
                    coordinate[0][0],
                    coordinate[0][1],
                    coordinate[2][0],
                    coordinate[2][1],
                ],
                "mid": [
                    (coordinate[0][0] + coordinate[2][0]) / 2,
                    (coordinate[0][1] + coordinate[2][1]) / 2,
                ],
            }
            jp_list.append(tmp)
            text_str += i
        # print(jp_list)
        # print(text_str)
        return jp_list

    else:
        print("ファイルが設定されていないです")
        sys.exit(1)


# 英語のOCRをかける日本語と同じような返り値の仕様
def en_OCR(image_path):
    args = get_args()

    # PaddleOCR準備
    paddleocr_parameter = get_paddleocr_parameter()

    paddleocr_parameter.det_model_dir = args.det_model
    paddleocr_parameter.rec_model_dir = args.rec_model
    paddleocr_parameter.rec_char_dict_path = args.rec_char_dict
    paddleocr_parameter.cls_model_dir = args.cls_model

    paddleocr_parameter.use_gpu = args.use_gpu

    paddle_ocr_onnx = PaddleOcrONNX(paddleocr_parameter)

    # 画像読み込み
    image = cv2.imread(image_path)

    # OCR実施
    dt_boxes, rec_res, time_dict = paddle_ocr_onnx(image)

    # print(time_dict)
    # for dt_box, rec in zip(dt_boxes, rec_res):
    #     print(dt_box, rec)
    en_list = []
    for coordinate, text in zip(dt_boxes, rec_res):
        i, t = text
        # print(i,end=" ")
        # print(t)
        # "coordinate":[x1,y1,x2,y2]という形.midは重心を表している。
        tmp = {
            "text": i,
            "probability": t,
            "coordinate": [
                coordinate[0][0],
                coordinate[0][1],
                coordinate[2][0],
                coordinate[2][1],
            ],
            "mid": [
                (coordinate[0][0] + coordinate[2][0]) / 2,
                (coordinate[0][1] + coordinate[2][1]) / 2,
            ],
        }
        en_list.append(tmp)
    return en_list


# 日本語と英語のOCRをかけ確率が高いほうを採用する関数。返り値は比較した後の採用されたほうの要素が入った配列。
def OCR_compare(jp_list, en_list):
    compare_list = jp_list.copy()
    for x in en_list:
        for count, y in enumerate(jp_list):
            x1, y1, x2, y2 = y["coordinate"]
            x_mid, y_mid = x["mid"]
            # 重心の中に日本語の判定での座標が含まれているのか判定
            if x1 < x_mid < x2 and y1 < y_mid < y2:
                # print(x["text"],y["text"])
                # 確率が高いほうを採用する
                if x["probability"] > y["probability"]:
                    compare_list[count] = x
                    break
    return compare_list


# 座標で1行を選定した後にそれを一つの文字列にするコード返り値は辞書型で上の辞書型と同じ。
def str_molding(lists):
    top_x = sorted(lists, key=lambda x: x["coordinate"][0])[0]["coordinate"][0]
    top_y = sorted(lists, key=lambda x: x["coordinate"][1])[0]["coordinate"][1]
    bottom_x = sorted(lists, key=lambda x: x["coordinate"][2], reverse=True)[0][
        "coordinate"
    ][2]
    bottom_y = sorted(lists, key=lambda x: x["coordinate"][3], reverse=True)[0][
        "coordinate"
    ][3]
    string = ""
    probability = 0
    # 確率を足して平均を計算する
    for item in lists:
        string += item["text"]
        probability += item["probability"]
    probability = probability / len(lists)
    dicts = {
        "text": string,
        "probability": probability,
        "coordinate": [top_x, top_y, bottom_x, bottom_y],
        "mid": [(top_x + bottom_x) / 2, (top_y + bottom_y) / 2],
    }
    return dicts


# 座標を確認して1行を確認するコード。
def OCR_line(compare_list):
    lists = []
    line_result = []
    for count, item in enumerate(compare_list):
        # print(count,item)
        for compare_index in range(count + 1, len(compare_list)):
            # print(compare_index,compare_list[compare_index]["text"])
            mid_x, mid_y = item["mid"]
            x1, y1, x2, y2 = compare_list[compare_index]["coordinate"]
            # print(item["text"],y1,y2,mid_y)
            value = 0
            # 中心が比較対象に含まれているのかか確認する。↓作成者以下解読不可能
            # 動きは例えば、[{本体},{228}][{228},{円}]と繋がっているため2番目と次の要素の１番目が一致する場合は追加する。違かったら新しいブロックになる。
            if y1 < mid_y < y2:
                value = 1
                # print(item,compare_list[compare_index])
                # listsが空っぽだったら初回のブロックのためlistsに2つの要素を追加する
                if len(lists) == 0:
                    lists.append(item)
                    lists.append(compare_list[compare_index])
                else:
                    if item in lists:
                        lists.append(compare_list[compare_index])
                    # 多分下のところは実行されない例外が起こってもいいため↓
                    elif compare_list[compare_index] in lists:
                        lists.append(item)
                    else:
                        # HACK:10月19日以下のfor文解読不可
                        for x in lists:
                            if x in line_result:
                                line_result.remove(x)

                        result_list = str_molding(lists)
                        line_result.append(result_list)
                        lists.clear()
                        lists.append(item)
                        lists.append(compare_list[compare_index])
        if value == 0:
            line_result.append(item)
        # print(line_result, lists)
    if len(lists) != 0:
        result_list = str_molding(lists)
        line_result.append(result_list)
    # HACK:10月19日以下のfor文解読不可
    for x in lists:
        if x in line_result:
            line_result.remove(x)
    # y座標によりソートをして上から並べ替えている。※ブロックになった要素が最後にappendされるため
    line_result = sorted(line_result, key=lambda x: x["coordinate"][1])
    # print(line_result)
    str_result = str()
    for x in line_result:
        str_result += x["text"]
    return str_result


# NOTE: 精度が悪いため使用しない:x座標によりある程度ブロックを作成するコード
def x_line_block(line_result):
    tmp_list1 = []
    tmp_list2 = []

    line_result = sorted(line_result, key=lambda x: x["coordinate"][0])

    for x in line_result:
        print(x)
    for count, item in enumerate(line_result):
        if count == 0:
            tmp_list1.append(item)
            continue
        if (
            line_result[count - 1]["coordinate"][0]
            < line_result[count]["mid"][0]
            < line_result[count - 1]["coordinate"][2]
        ):
            tmp_list1.append(item)
        elif (
            line_result[count - 1]["coordinate"][2]
            - line_result[count]["coordinate"][0]
            < 30
            or (
                line_result[count]["coordinate"][0]
                - line_result[count - 1]["coordinate"][0]
            )
            < 70
        ):
            tmp_list1.append(item)
        else:
            tmp_list2.append(tmp_list1)
            tmp_list1 = []
    tmp_list2.append(tmp_list1)
    # print(tmp_list2)
    for x in tmp_list2:
        print("########")
        print(x)
    # print(tmp_list2)
    tmp_list3 = y_line_block(tmp_list2)
    # for item in tmp_list3:
    #     print(item)
    # OCR_line(item)


# NOTE: 精度が悪いため使用しないy座標よりある程度ブロックを作成するコード
def y_line_block(list_item):
    item_list = []
    block_list = []
    for count, item in enumerate(list_item):
        if count == 0:
            item_list.append(item)
        else:
            if (
                list_item[count]["coordinate"][3]
                - list_item[count - 1]["coordinate"][1]
                < 200
            ):
                # print(item)
                item_list.append(item)
            else:
                # print(item_list)
                # appendは値渡しではなくアドレス渡し(知見)
                block_list.append(item_list)
                # clearを使ってしまとアドレスの先の値が消えてしまうからitem_listを再定義
                item_list = []
                item_list.append(item)
    block_list.append(item_list)
    # print(block_list)
    return block_list


def ocr_main(photo_path):
    jp_list = jp_OCR(photo_path)
    en_list = en_OCR(photo_path)
    # print(jp_list)
    # print(en_list)
    compare_list = OCR_compare(jp_list, en_list)
    # print(y_result)
    # y_result = y_line_block(compare_list)
    # x_line_block(compare_list)
    try:
        line_result = OCR_line(compare_list)
        return line_result
    except:
        str_result = str()
        for x in compare_list:
            str_result += x["text"]
        return str_result


if __name__ == "__main__":
    print(ocr_main("./cutimages/test6.png"))
