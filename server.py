from flask import Flask, request, jsonify
from validation import callGPT

app = Flask(__name__)

@app.route('/', methods=['GET'])
def ping():
  return 'pong', 200

@app.route('/', methods=['POST'])
def home():
  rating_answer, reasoning_answer = callGPT(request)
  final_response = {
    "Rating": rating_answer,
    "Reasoning": reasoning_answer
  }
  return jsonify(final_response), 200

if __name__ == '__main__':
  app.run(host='0.0.0.0', port=5000)