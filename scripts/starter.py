import json

class Starter:
    """
    An instance of Starter describes how and with what you feed your sourdough starter
    """
    description = ""
    flour = {}
    hydration = 0
    innoculation = 0
    feeding_span = 0 # hours between each feeding

    def __init__(self,
                 description = "default",
                 hydration = 1,
                 span = 12,
                 flour = {"all-purpose":0.5, "whole-wheat":0.5},
                 innoculation = 0.5):
        """
        :param description: A comment about the starter used
        :param hydration: The weight of water ralative to the weight of flour used, hydration = 1 <=> 100%
        :param span: The time (in hours) between two feedings
        :param flour: A dict describing what flours are used to feed the starter and their respective proportions, the sum of values should be 1
        :param ratio: The feeding ratio describes how much water and flour is added when feeding relative to the weight of mature starter
        """
        self.description = description
        self.hydration = hydration
        self.span = span
        self.flour = flour
        self.innoculation = innoculation

    def __str__(self):
        res = "{:20} : {}\n".format('Description', self.description)
        res += "{:20} : {} %\n".format('Hydration', int(self.hydration*100))
        res += "{:20} : {} h\n".format('Time between feed', self.span)
        res += "Flour type :\n"
        for k, v in self.flour.items():
            res += "    {:16} : {:<2} %\n".format(k, int(v*100))
        res += "{:20} : {} %\n".format('Innoculation rate', int(self.innoculation*100))
        return res

    def build_schedule(self, target, stages = 1):
        """int target : amount of target starter un grams
           int stages : number of refreshes to build the levain
           prints instructions to build your desired amount of levain and
           return a dict with the amounts of starter:flour:water at each refresh
        """
        res = {}
        curr = target
        for k in range(stages):
            res [stages-k] = {'starter' : int(curr*self.innoculation),
                                                'flour' : int(curr*(1-self.innoculation)/(1+self.hydration)),
                                                'water' : int(curr*(1-self.innoculation)*(self.hydration)/(1+self.hydration))
                                                }
            curr *= self.innoculation
        res = dict(sorted(res.items()))
        for k,v in res.items():
            print("feed {} : {} h before mixing".format(k, (stages - k + 1)*self.span))
            for ingredient, weight in v.items():
                print("    {:<16} : {:<2} g".format(ingredient, weight))
        return res

    def save(self, file):
        """
        :param file: file name
        saves the object as a json file for persitance
        """
        fp = open(file, "w+")
        res = json.dumps(self.__dict__)
        json.dump(res, fp)

    def load(file):
        """
        :param file: file name
        :return: the instance of Starter class saved in the file
        """
        fp = open(file)
        res = json.load(fp)
        starter = Starter()
        starter.__dict__ = eval(res)
        return starter


def test():
    # instantiate starter
    starter = Starter()
    starter.description = "My example starter"
    starter.span = 24
    starter.hydration = 1
    starter.flour = {'all-purpose':1}
    # save starter in JSON file
    starter.save("data/example.json")
    # recover data from the JSON file
    starter = Starter.load("data/example.json")
    print(starter)
    # generate a levain build schedule
    starter.build_schedule(100, 2)

def main(name, target, stages):
    starter = Starter.load("data/{}.json".format(name))
    print(starter)
    starter.build_schedule(target, stages)

if __name__ == "__main__":
    test()
    main("tartine", 140, 3)