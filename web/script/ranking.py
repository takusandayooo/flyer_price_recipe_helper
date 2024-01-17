from itertools import groupby


def read_file():
    item_file = open("./static/csv/item.csv", "r")
    file_list = []
    for line in item_file:
        if line.startswith("#"):
            continue
        line = line.strip().split(",")
        file_list.append(
            {
                "shopName": line[0],
                "itemName": line[1],
                "category": line[2],
                "itemPrice": int(line[3]),
            }
        )
    item_file.close()
    itemName = sorted(
        list(
            {
                next(group)["itemName"]
                for key, group in groupby(file_list, lambda x: x["itemName"])
            }
        )
    )
    file_list = sorted(file_list, key=lambda x: x["itemName"])
    lists = []
    for key, group in groupby(file_list, key=lambda x: x["itemName"]):
        group = list(group)
        group = sorted(group, key=lambda x: x["itemPrice"])
        lists.append(group)
    return [itemName, lists]


if __name__ == "__main__":
    lists = read_file()
    print(lists)
