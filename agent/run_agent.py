# agent/router.py
import os
from typing import Dict, Any, List
from dotenv import load_dotenv
from openai import OpenAI
from .tools import TOOLS_SPEC, TOOLS_IMPL

load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

SYSTEM_PROMPT = """You are an HR copilot for salary prediction, job fit, resume screening, and candidate prioritization.
- Speak concise French.
- Use tools when needed.
- Prefer calling predict_salary when a user asks about salary, and so on.
"""

def run_agent_turn(history: List[Dict[str, str]]) -> Dict[str, Any]:
    """
    history: [{"role":"system"/"user"/"assistant","content":"..."}]
    returns a dict with either final text OR a tool call result integrated.
    """
    # 1) Appel LLM avec tool spec
    response = client.chat.completions.create(
        model="gpt-4o-mini",  # ou gpt-4o / gpt-4.1 si tu veux
        messages=history,
        tools=[{"type": "function", "function": spec} for spec in TOOLS_SPEC],
        tool_choice="auto",
        temperature=0.2,
    )

    choice = response.choices[0]
    msg = choice.message

    # 2) Si le LLM veut appeler un tool
    if msg.tool_calls:
        tool_call = msg.tool_calls[0]
        fn_name = tool_call.function.name
        fn_args = tool_call.function.arguments  # JSON string
        import json
        args = json.loads(fn_args) if fn_args else {}

        impl = TOOLS_IMPL.get(fn_name)
        if not impl:
            return {"role":"assistant","content":f"Outil inconnu: {fn_name}"}

        # 3) Exécuter le tool côté Python (HTTP vers Flask ou stub)
        result = impl(args)

        # 4) Renvoyer le résultat au LLM pour qu’il formule la réponse finale
        history_plus = history + [
            {"role":"assistant","tool_calls":[{"id": tool_call.id, "type":"function", "function":{"name":fn_name,"arguments":fn_args}}]},
            {"role":"tool","tool_call_id": tool_call.id, "content": str(result)}
        ]
        response2 = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=history_plus,
            temperature=0.2,
        )
        return response2.choices[0].message.dict()

    # 5) Sinon, juste une réponse textuelle
    return msg.dict()
