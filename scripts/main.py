from starter import Starter
from os import listdir
from os.path import isfile, join

path = "./data"

if __name__ == "__main__":
    print("Available starters : ")
    fileNames = [f for f in listdir(path) if f[-5:] == ".json"]

    for (index, name) in enumerate(fileNames):
        print("    {} : {}".format(index, name[:-5]))
    chosen_index = int(input("Choose your starter : \n"))
    starter = Starter.load("./data/" + fileNames[chosen_index])
    print(starter)

    target = int(input("target amount of levain (in grams): \n"))

    stages = int(input("number of stages: \n"))

    starter.build_schedule(target, stages)