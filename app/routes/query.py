from flask import Blueprint, request, jsonify
from app.utils import vector_db, openai_client

bp = Blueprint('query', __name__, url_prefix='/query')

@bp.route('', methods=['POST'])
def query_ai():
    data = request.get_json()
    if not data or 'prompt' not in data:
        return jsonify({'error': 'Prompt required'}), 400
    prompt = data['prompt']
    system_prompt = data.get('system_prompt', '')
    results = vector_db.search(prompt)
    context = "\n".join(results)
    ai_response = openai_client.get_ai_response(prompt, system_prompt, context)
    return jsonify({'response': ai_response})
