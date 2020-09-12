import glob, os
import random
import shutil

ROOT = "D:/gobot/train/map/"
TRAIN_DEST = "D:/gobot/train/map_od/train/"
TEST_DEST = "D:/gobot/train/map_od/test/"

os.chdir("D:/gobot/train/map")
xmls = glob.glob("*.xml")
random.shuffle(xmls)

train_len = int(0.9*len(xmls))

for file in xmls[:train_len]:
    shutil.move(ROOT+file, TRAIN_DEST)
    imageFile = file.split(".")[0] + ".png"
    shutil.move(ROOT+imageFile, TRAIN_DEST)

for file in xmls[train_len:]:
    shutil.move(ROOT+file, TEST_DEST)
    imageFile = file.split(".")[0] + ".png"
    shutil.move(ROOT+imageFile, TEST_DEST)