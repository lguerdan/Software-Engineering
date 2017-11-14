import os, requests, json
from flask import Flask, send_file, jsonify, request
from class_selection import *

app = Flask(__name__)


@app.route("/")
def get_classes():
   n = request.args.get("num")
   if not n or not n.isdigit() or int(n) < 0 :
      return jsonify({"error": "bad request"})

   selected_classes = get_classes_basic(n)
   return jsonify(selected_classes)


if __name__ == '__main__':
    port = int(os.environ.get('PORT', 8080))
    app.run(host='0.0.0.0', port=port)