import json


class NumpyArrayEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, np.ndarray):
            return obj.tolist()
        return super().default(obj)


with open('temp/img_0000000.jpg.json.bad', 'r') as f:
    data = f.read()

print(data)

with open('temp/test_convert.json', 'w') as f:
    json.dump(data, f, cls = NumpyArrayEncoder, indent = 4)
