from flask import Flask, render_template, request, jsonify
from modules.llm_interface import LLMInterface

app = Flask(__name__)
llm = LLMInterface()

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/query', methods=['POST'])
def process_query():
    data = request.json
    prompt = data.get('prompt', '')
    response = llm.query(prompt)
    return jsonify({'response': response})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
