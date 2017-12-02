import json, os, random
file_path = os.path.join(os.path.dirname(__file__),"CompleteJSON.json")

departments = ["MATH", "CMP_SC", "ECONOM", "FINANC", "MANGMT", "MRKTNG", "MUS_APMS", "MUS_ENS", "MUS_GENL", "MUS_H_LI", "MUS_THRY", "INFOTC", "ACCTCY"]
degrees = ["CSMajor","ITMajor", "MathMinor", "MusicStudiesMajor", "BusinessMinor"]
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

def get_courses_for_degrees(degree1, degree2):
   if (degree1 and degree1 not in degrees) or (degree2 and degree2 not in degrees):
      return bad_requeset

   if not degree1 or not degree2:
      if degree1:
         return get_degree(degree1)
      else:
         return get_degree(degree2)

   else:
      deg1_courses = get_degree(degree1)
      deg2_courses = get_degree(degree2)
      return [deg1_courses, deg2_courses]


def get_degree(degree):
   print degree
   return {}

