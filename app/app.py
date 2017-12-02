import os, requests, json
from flask import Flask, send_file, jsonify, request
from class_selection import *

app = Flask(__name__)

@app.route("/")
def root():
   return "<h1>Hello! Welcome to the best class selector ever</h1>"

@app.route("/get_classes")
def get_classes():
   n = request.args.get("num")
   dept = request.args.get("department")


   if not n or not n.isdigit() or int(n) < 0 :
      return jsonify({"error": "bad request"})

   selected_classes = get_classes_basic(n, dept)
   return jsonify(selected_classes)


@app.route("/get_degree")
def get_degree():
   deg1 = request.args.get("deg1")
   deg2 = request.args.get("deg2")
   print deg1
   if not deg1 and not deg2:
      return jsonify({"error": "bad request"})

   selected_classes = get_courses_for_degrees(deg1, deg2)
   return jsonify(selected_classes)



if __name__ == '__main__':
    port = int(os.environ.get('PORT', 8080))
    app.run(host='0.0.0.0', port=port)