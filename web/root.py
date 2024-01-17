import time

from flask import Flask, render_template, request
from script import kcal, radar_chart, ranking, search_recipe

app = Flask(__name__)


# NOTE:ここで材料のリストを作成している。
@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "GET":
        return render_template("index.html")
    if request.method == "POST":
        # 必ず必要な材料取得
        mast_item = request.form["item1"]
        # スクレイピング
        global recipe_lists
        recipe_lists = search_recipe.scraping_cookpad(mast_item)
        split_item = mast_item.split(",")
        [itemName, ranking_list] = ranking.read_file()
        rankingList = []
        # TODO: ランキングの1,2,3位ranking_listに入れる,なかった場合Noneを入れる。そしてHTMLにif文なのでNoneの場合はありませんなどを表示する。

        for x in split_item:
            priceList = [None, None, None]
            shopList = [None, None, None]
            if x in itemName:
                index = itemName.index(x)
                for count, y in enumerate(ranking_list[index]):
                    if count < 3:
                        priceList[count] = y["itemPrice"]
                        shopList[count] = y["shopName"]
            rankingList.append(
                {"itemName": x, "shopList": shopList, "priceList": priceList}
            )
        print(rankingList)
        # recipe_lists=[{"recipe_title":"recipe_title","recipe_description":"recipe_description","material_ingredients":"material_ingredients","url":"url"},{"recipe_title":"recipe_title","recipe_description":"recipe_description","material_ingredients":"material_ingredients","url":"url"}]
        return render_template(
            "recipe.html", recipe_lists=recipe_lists, rankingList=rankingList
        )


# NOTE:indexにより選ばれたレシピを判定し、それによって材料の質量の入力画面を表示している。
@app.route("/calorieItem/<int:index>", methods=["GET", "POST"])
def calorie_item(index):
    global item_dict
    global search_index
    search_index = index - 1
    # print(recipe_lists)
    item_dict = recipe_lists[search_index]["material_ingredients"].split("#")
    item_dict = [{"index": str(count), "name": x} for count, x in enumerate(item_dict)]
    return render_template("calorieItem.html", item_dict=item_dict)


# NOTE:材料の質量を入力すると、カロリー計算の関数を呼び出し、カロリーのグラフを表示している。
@app.route("/calorieGraph", methods=["GET", "POST"])
def calorie_graph():
    item = []
    print(item_dict)
    for count, x in enumerate(item_dict):
        gram = request.form.get("zairyou" + str(count))
        item.append(
            {"index": x["index"], "name": x["name"].split(":")[0], "gram": gram}
        )
    sex = request.form.get("sex")
    age = int(request.form.get("age"))
    # TODO:ここにカロリー計算結果の値を入れる↓
    itemList = []
    for x in item:
        if x["gram"] == "" or x["gram"] == 0:
            continue
        else:
            itemList.append(x["name"])
    kcalList = kcal.kcal(itemList)
    data = [0, 0, 0, 0, 0]
    for x, y in zip(kcalList, item):
        if x["energy"] != 0:
            data[0] += x["energy"] / 100 * int(y["gram"])
            data[1] += x["protein"] / 100 * int(y["gram"])
            data[2] += x["fat"] / 100 * int(y["gram"])
            data[3] += x["carb"] / 100 * int(y["gram"])
            data[4] += x["salt"] / 100 * int(y["gram"])
    radar_chart.main_radarChart(age, sex, data)
    # ここにカロリー計算の関数を入れる↓パスも渡す。
    calorie_dict = {
        "name": recipe_lists[search_index]["recipe_title"],
        "calorie": data[0],
    }
    time.sleep(1)
    return render_template("calorieGraph.html", calorie_dict=calorie_dict)


if __name__ == "__main__":
    app.run()
