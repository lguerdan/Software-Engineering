import json, os, random
file_path = os.path.join(os.path.dirname(__file__),"cs_classes_raw.json")

departments = ["MATH", "CMP_SC"]
bad_requeset = {"error": "bad request"}

def get_classes_basic(numclasses, department):

   if department not in departments:
      return bad_requeset

   data = json.load(open(file_path))

   department_classes =  data[department]["Courses"]
   if int(numclasses) > len(department_classes):
      numclasses = len(department_classes)

   random.shuffle(department_classes)
   classes_out = [department_classes[i] for i in range(int(numclasses))]
   return classes_out