from flask import Blueprint, request, jsonify
from agent.router import run_agent_turn, SYSTEM_PROMPT

bp = Blueprint("agent", __name__)

@bp.post("/chat")
def chat():
    # expect: {"history":[{"role":"user"/"assistant","content":"..."}]}
    body = request.get_json(silent=True) or {}
    user_history = body.get("history", [])
    # always inject the system prompt at the start
    history = [{"role": "system", "content": SYSTEM_PROMPT}] + user_history
    try:
        msg = run_agent_turn(history)  # returns {"role":"assistant","content": "..."}
        return jsonify({"message": msg}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500
