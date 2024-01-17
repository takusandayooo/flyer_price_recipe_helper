import os
import time

import modules.folderDelete as folderDelete
import modules.getItemName as getItemName
import modules.getPrice as getPrice
import modules.main_get_infomations as get_tirasi
import modules.tirasicut as tirasicut
from modules.path_and_do_areafunction import (get_file_path_do_area_function,
                                              get_folder_path_do_area_function)

import OCR as OCR

try:
    file = open(r"../web/static/csv/item.csv", "x")
except FileExistsError:
    os.remove(r"../web/static/csv/item.csv")
    file = open(r"../web/static/csv/item.csv", "x")
file.write("#店舗,商品,分類,価格\n")
print("チラシをダウンロード")
get_tirasi.get_resipe()
print("チラシのパスを取得")
pathList = get_folder_path_do_area_function("./dir_out")
for shopName, path in pathList:
    print("チラシの切り抜き")
    folderDelete.folderDelete("./cutimages")
    tirasicut.tirasitm(path)
    cutPathList = get_file_path_do_area_function("./cutimages")
    print(cutPathList)
    for cutPath in cutPathList:
        print(cutPath)
        ocrText = OCR.ocr_main(cutPath)
        print(ocrText)
        findPrice = getPrice.getGeminiAPIResponse(ocrText)
        print(findPrice)
        time.sleep(1)
        itemName = getItemName.getGeminiAPIResponse(ocrText)
        print(shopName, itemName)
        file.write(
            shopName.replace(" ", "")
            + ","
            + itemName
            + ","
            + "None"
            + ","
            + str(findPrice)
            + "\n"
        )
file.close()
