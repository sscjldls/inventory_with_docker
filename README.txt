INVENTORY AGENT - NOTE ON USING GROQ INSTEAD OF GEMINI

The course tutorial builds this Django inventory agent using Google's Gemini API (the google-genai package and a GEMINI_API_KEY). With the professor's permission to use other models, this project uses Groq instead. Groq is an AI inference provider (not to be confused with Grok from xAI). Groq offers an API that follows the same format as OpenAI's API, so the project talks to it using the standard openai Python package, pointed at Groq's address. No OpenAI account or OpenAI service is used.

The model used is openai/gpt-oss-120b, served by Groq. The project structure, the database model, the inventory tools, the system prompt and the chat page are the same idea as in the tutorial. Only the parts that talk to the model had to change.

WHAT CHANGED

chat/agent.py was the main change. The Gemini SDK import was replaced with "from openai import OpenAI". The client is created with the base_url set to https://api.groq.com/openai/v1 and the api_key read from the environment. The model name is now the Groq model above instead of a Gemini model. The system prompt is now sent as the first message in the conversation, with the role "system". The loop that lets the model call tools was rewritten for the OpenAI-style format: the code calls client.chat.completions.create with the list of messages and the tools, checks whether the reply contains tool_calls, runs the matching Python function, and sends the result back as a message with the role "tool" and the matching tool_call_id. The loop repeats until the model replies with plain text, with a limit of 5 steps so it cannot run forever. This is the same agent idea as in the tutorial, just written in the other API's format.

chat/tools.py kept the same Python functions (check_stock, list_items, add_item, remove_stock, delete_item, get_item_price). What changed is the description list that tells the model which tools exist. Gemini and OpenAI-style APIs describe functions differently, so TOOL_DECLARATIONS is now written as a list of entries with "type": "function" and a JSON-schema description of the parameters. The functions still return normal Python dictionaries, and agent.py converts them to JSON text before sending them back to the model.

chat/views.py also had to change. The Gemini version remembered the conversation by saving an interaction id in the session and expected run_agent to return both an answer and a new id. The Groq API has no such id, so it works differently: the full conversation is kept in the session, and each time the user sends a message, the earlier messages (the last 20) are sent along with it, converted to the user and assistant roles that the API expects. run_agent now simply returns the answer text. Before this was updated, every message failed with the error "too many values to unpack".

.env now contains GROQ_API_KEY instead of GEMINI_API_KEY. settings.py is unchanged, since it already loads .env with python-dotenv. The key must never be put in the code or shared. Anyone running the project needs their own free key from console.groq.com.

Packages: the tutorial installs django, google-genai and python-dotenv. This project needs django, openai and python-dotenv instead, so google-genai is no longer required. Install them with: pip install django openai python-dotenv

ADDITIONS BEYOND THE TUTORIAL

The Item model has a price field (migration 0002_item_price), and the agent has tools to read prices (get_item_price) and to change them (set_price), so it can answer questions about totals and VAT and apply percentage price changes.

HOW TO RUN

Create a .env file in the project folder containing the line GROQ_API_KEY=your-key-here, or use my key, and also create a venv as it is a large file! Run python manage.py migrate, then python manage.py runserver, and open http://127.0.0.1:8000/ in a browser.
