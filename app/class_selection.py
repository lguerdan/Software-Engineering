import json, os, random
file_path = os.path.join(os.path.dirname(__file__),"cs_classes_raw.json")

def get_classes_basic(numclasses):
   data = json.load(open(file_path))
   if int(numclasses) > len(data):
      numclasses = len(data)

   random.shuffle(data)
   classes_out = [data[i] for i in range(int(numclasses))]
   return classes_out