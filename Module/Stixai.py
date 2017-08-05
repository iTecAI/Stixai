import random

class ai:
    def __init__(self, actions, responses):
        self.IN = actions
        self.OUT = responses
    def get_act(self, action, valres):
        if action in self.IN:
            mList = {}
            for response in self.OUT:
                if self.IN[self.OUT.index(response)] == action and not response in mList:
                    mList[response] = 1
                elif response in mList:
                    mList[response] += 1
            print mList
            keys = []
            vals = []
            for v in sorted(mList.values(), reverse = True):
                for k in mList.keys():
                    if mList[k] == v:
                        keys.append(k)
                        vals.append(v)
            print keys
            print vals
            try:
                resp = keys[valres]
            except:
                resp = random.choice(self.OUT)
        else:
            resp = random.choice(self.OUT)

        return resp
    def update(ins, outs):
        self.IN = ins
        self.OUT = outs
                        
            
def test():
    stix = ai(['attack', 'retreat', 'eat', 'attack', 'attack'], ['run', 'cheer', 'share lunch', 'fall', 'run'])
    print stix.get_act('attack', 0)

#test()
            
            
