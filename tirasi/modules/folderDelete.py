import os
import shutil


def folderDelete(folderName):
    try:
        shutil.rmtree(folderName)
    except:
        pass
    # os.mkdir(folderName)


if __name__ == "__main__":
    folderDelete("cutimages")
