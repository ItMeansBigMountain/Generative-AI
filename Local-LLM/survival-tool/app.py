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
    
    # Check for special commands
    if prompt.lower() in ['/reset', '/restart']:
        response = llm.reset_conversation()
    else:
        response = llm.query(prompt)
    
    return jsonify({
        'response': response,
        'context_length': len(llm.conversation_history)
    })

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
