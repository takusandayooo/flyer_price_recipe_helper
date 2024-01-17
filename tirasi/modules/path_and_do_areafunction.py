import os


# NOTE: この関数は、dir_pathの中にあるフォルダーをfor文で回して、その中にあるファイルのパスをリストにして返す関数
def get_folder_path_do_area_function(dir_path):
    dir_list = []
    main_files = os.listdir(dir_path)
    for x in main_files:
        if x == "<!DOCTYPE html><html>":
            main_files.remove(x)
            continue
        shop_path = dir_path + "/" + x
        main_files = os.listdir(shop_path)
        for y in main_files:
            file_path = shop_path + "/" + y
            dir_list.append((x, file_path))
    return dir_list


# NOTE: この関数は、dir_pathの中にあるファイルのパスをリストにして返す関数
def get_file_path_do_area_function(dir_path):
    dir_list = []
    main_files = os.listdir(dir_path)
    for x in main_files:
        if x == "<!DOCTYPE html><html>":
            main_files.remove(x)
            continue
        file_path = dir_path + "/" + x
        dir_list.append(file_path)
    return dir_list


if __name__ == "__main__":
    get_file_path_do_area_function("./cutimages")
    print(get_folder_path_do_area_function("./dir_out"))
