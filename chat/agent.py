import json
import os
from openai import OpenAI

from .tools import TOOL_DECLARATIONS, TOOL_FUNCTIONS

# Initialize OpenAI client targeting Groq's endpoint
client = OpenAI(
    base_url="https://api.groq.com/openai/v1",
    api_key=os.environ.get("GROQ_API_KEY"),
)

MODEL = "openai/gpt-oss-120b"

SYSTEM_PROMPT = """You are an inventory assistant for a small hardware warehouse.

You help the user check stock, update inventory, and look up item prices by calling the tools available to you.

Rules:
- Always use a tool to fetch stock or price data. Never guess or rely on memory.
- When asked to calculate total costs, item totals, or tax/VAT (e.g., 10% VAT), use your pricing tools to get the base unit price first, then calculate the total clearly for the user.
- If a tool returns an error, explain the problem to the user in plain language.
- Before deleting an item entirely, make sure that is what the user meant.
- Keep your answers helpful, clear, and factual.
- Do not answer any question unrelated to the inventory task.
"""

MAX_STEPS = 5


def run_agent(user_message, history=None, verbose=False):
    """Send a message to the agent and run tools until it produces an answer."""
    messages = [{"role": "system", "content": SYSTEM_PROMPT}]

    # Append past dialogue history if provided
    if history:
        messages.extend(history)

    # Append current user prompt
    messages.append({"role": "user", "content": user_message})

    for _ in range(MAX_STEPS):
        response = client.chat.completions.create(
            model=MODEL,
            messages=messages,
            tools=TOOL_DECLARATIONS,
            tool_choice="auto",
        )

        response_message = response.choices[0].message

        # If the model didn't call any tools, return its final response text
        if not response_message.tool_calls:
            return response_message.content

        # Append assistant message (containing tool calls) to message history
        messages.append(response_message)

        # Process each requested function call
        for tool_call in response_message.tool_calls:
            function_name = tool_call.function.name
            function_args = json.loads(tool_call.function.arguments)

            if function_name in TOOL_FUNCTIONS:
                try:
                    tool_output = TOOL_FUNCTIONS[function_name](**function_args)
                except Exception as exc:
                    tool_output = {"error": f"Tool failed: {exc}"}
            else:
                tool_output = {"error": f"Function '{function_name}' not found."}

            if verbose:
                print(f"  -> {function_name}({function_args}) = {tool_output}")

            # Append the tool execution result back to the messages list
            messages.append({
                "role": "tool",
                "tool_call_id": tool_call.id,
                "content": json.dumps(tool_output),
            })

    return "I got stuck working on that. Please try rephrasing."