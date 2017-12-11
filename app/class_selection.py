import json, os, random, re
courses_file = os.path.join(os.path.dirname(__file__),"CompleteCourses.json")
degrees_file = os.path.join(os.path.dirname(__file__),"CompleteDegrees.json")


departments = ["MATH", "CMP_SC", "ECONOM", "FINANC", "MANGMT", "MRKTNG", "MUS_APMS", "MUS_ENS", "MUS_GENL", "MUS_H_LI", "MUS_THRY", "INFOTC", "ACCTCY"]
degrees = ["CSMajor","ITMajor", "MathMinor", "MusicStudiesMajor", "BusinessMinor"]
bad_requeset = {"error": "bad request"}

def get_classes_basic(numclasses, department):

   if department not in departments:
      return bad_requeset

   data = json.load(open(courses_file))

   department_classes =  data[department]["Courses"]
   if int(numclasses) > len(department_classes):
      numclasses = len(department_classes)

   classes_out = [department_classes[i] for i in range(int(numclasses))]
   return classes_out


def get_courses_for_degrees(degree1, degree2):
   if (degree1 and degree1 not in degrees) or (degree2 and degree2 not in degrees):
      return bad_requeset

   response_out = {}

   if degree1:
      response_out[degree1] = get_degree(degree1)
   if degree2:
      response_out[degree2] = get_degree(degree2)

   return response_out


def get_degree(degree):
   data = json.load(open(degrees_file))
   courses = []
   courses_full = []

   for requirement in data[degree]["requirements"]:
      ctemp = requirement["classes"]
      random.shuffle(ctemp)
      courses.extend(ctemp[:requirement["count"]])

   for course in courses:

      course_full = get_course_from_ID(course)
      if course_full != None:
         courses_full.append(course_full)
      else:
         print "didnt find course " + course

   return courses_full


def get_course_from_ID(cid):

   dept = filter(None, re.split(r'(\d+)', cid))[0]
   allcourses = json.load(open(courses_file))
   for course in allcourses[dept]["Courses"]:

      if "GUID" in course:
         if course["GUID"] == cid:
            return course
      else:
         print course["Description"]
         print "no GUID in "+ str(course)
   return None

def course_in_selection(courses, course):
