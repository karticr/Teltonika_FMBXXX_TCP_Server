import json

class avlIdMatcher:
    def __init__(self):
        self.avl_data = self.loadData()

    def loadData(self):
        with open('avlIds.json') as f:
            data = json.load(f)
        return data

    def getAvlInfo(self, id):
        try:
            data = self.avl_data[id]
            return data
        except:
            print("id not found")
            return -1

    def idToAvl(self, data):
        format = {}
        for i in data:
            n_data = data[i]
            for j in n_data:
                id      = str(j)
                id_name = self.getAvlInfo(id)['name']
                value   = n_data[j]
                # print("Key: {}, Value: {}".format(id_name, value))
                format[id_name] = value            
        return format

if __name__ == "__main__":
    data = avlIdMatcher()
    # print(data.avl_data)
    print(data.getAvlInfo("4")['name'])
    print(data.getAvlInfo("1"))