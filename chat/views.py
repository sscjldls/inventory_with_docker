from django.shortcuts import redirect, render

from .agent import run_agent


def chat_view(request):
    if request.method == "POST":
        user_message = request.POST.get("message", "").strip()

        if user_message:
            history = request.session.get("history", [])

            # Turn the saved chat into the format the model expects.
            # (Only the last 20 messages, so it doesn't grow forever.)
            model_history = [
                {
                    "role": "assistant" if m["role"] == "agent" else "user",
                    "content": m["text"],
                }
                for m in history[-20:]
            ]

            try:
                answer = run_agent(user_message, model_history)
            except Exception as exc:
                answer = f"Something went wrong: {exc}"

            history.append({"role": "user", "text": user_message})
            history.append({"role": "agent", "text": answer or "(No response)"})
            request.session["history"] = history

        return redirect("chat")

    return render(request, "chat.html", {
        "history": request.session.get("history", []),
    })


def reset_view(request):
    request.session.flush()
    return redirect("chat")