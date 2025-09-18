import os
from agent.tools import TOOLS_SPEC, TOOLS_IMPL
from openai import OpenAI

# Charger la clé OpenAI
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
client = OpenAI(api_key=OPENAI_API_KEY)

def run_cli():
    print("🤖 HR Agent CLI (q to quit)")
    while True:
        user_input = input("You: ")
        if user_input.lower() in ["q", "quit", "exit"]:
            print("👋 Bye!")
            break

        # Exemple : juste tester l'appel
        print("Thinking...")
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": "You are an HR assistant."},
                {"role": "user", "content": user_input}
            ]
        )
        print("Agent:", response.choices[0].message.content)

# 👇 Important : point d’entrée
if __name__ == "__main__":
    run_cli()
