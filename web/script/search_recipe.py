import csv
import time

import requests
from bs4 import BeautifulSoup


def scraping_cookpad(ingredients_list):
    id = 0
    ingredients_list = ingredients_list.split(",")

    def format_ingredients(ingredients_dict):
        return "#".join([f"{key}: {value}" for key, value in ingredients_dict.items()])

    csv_file = "./static/csv/recipes.csv"
    recipe_lists = []
    with open(csv_file, "w", newline="", encoding="utf-8-sig") as file:
        writer = csv.writer(file, escapechar=",")
        writer.writerow(
            ["id", "Recipe Title", "Description", "Material Ingredients", "URL"]
        )

        for page_num in range(1, 2):
            search_url = f'https://cookpad.com/search/{"+".join(ingredients_list)}?order=date&page={page_num}'
            res = requests.get(search_url)

            try:
                res.raise_for_status()
            except requests.exceptions.RequestException as e:
                print(f"リクエスト中にエラーが発生しました: {e}")
                break

            res.encoding = "utf-8"
            soup = BeautifulSoup(res.text, "html.parser")

            recipe_links = [a["href"] for a in soup.select("a.recipe-title")]

            if not recipe_links:
                break

            for link in recipe_links:
                id += 1
                full_url = f"https://cookpad.com{link}"
                res = requests.get(full_url)

                try:
                    res.raise_for_status()
                except requests.exceptions.RequestException as e:
                    print(f"リクエスト中にエラーが発生しました: {e}")
                    continue

                res.encoding = "utf-8"
                soup = BeautifulSoup(res.text, "html.parser")

                try:
                    recipe_title = soup.find("h1", class_="recipe-title").text
                except AttributeError:
                    recipe_title = "N/A"

                try:
                    recipe_description = soup.find(
                        "div", class_="description_text"
                    ).text
                except AttributeError:
                    recipe_description = "N/A"

                material_ingredients_list = [
                    x.text for x in soup.find_all("div", class_="ingredient_name")
                ]
                ingredients_used_list = [
                    x.text
                    for x in soup.find_all("div", class_="ingredient_quantity amount")
                ]

                ingredients_dict = {}
                for i in range(len(material_ingredients_list)):
                    ingredients_dict[
                        material_ingredients_list[i]
                    ] = ingredients_used_list[i]

                material_ingredients = format_ingredients(ingredients_dict)

                url = full_url

                writer.writerow(
                    [id, recipe_title, recipe_description, material_ingredients, url]
                )
                recipe_lists.append(
                    {
                        "id": id,
                        "recipe_title": recipe_title,
                        "recipe_description": recipe_description,
                        "material_ingredients": material_ingredients,
                        "url": url,
                    }
                )
            page_num += 1
            time.sleep(1)

    print("csvファイルを確認してください")
    return recipe_lists


if __name__ == "__main__":
    ingredients_list = []
    ingredients_list = input(",で区切って材料を入力してください: ")
    print(scraping_cookpad(ingredients_list))
