from flask import Flask, request, jsonify, render_template_string
from chatbot import Chatbot

app = Flask(__name__)
chatbot = Chatbot()

html_page = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <script src="https://cdn.tailwindcss.com"></script>
    <title>Chatbot</title>
</head>
<body class="bg-gray-100 min-h-screen flex flex-col justify-center items-center">
    <div class="bg-white shadow-lg rounded-lg w-1/3">
        <div class="bg-blue-500 text-white p-4 rounded-t-lg">
            <h1 class="text-lg font-bold">Chatbot</h1>
        </div>
        <div id="chatbox" class="p-4 h-80 overflow-y-auto space-y-4">
            <!-- Chat messages will appear here -->
        </div>
        <div class="p-4 border-t">
            <form id="chat-form" class="flex">
                <input
                    type="text"
                    id="user-input"
                    placeholder="Type your message..."
                    class="flex-1 border border-gray-300 rounded-l-lg px-4 py-2 focus:outline-none"
                />
                <button
                    type="submit"
                    class="bg-blue-500 text-white px-4 py-2 rounded-r-lg hover:bg-blue-600"
                >
                    Send
                </button>
            </form>
        </div>
    </div>

    <script>
        const chatForm = document.getElementById("chat-form");
        const userInput = document.getElementById("user-input");
        const chatbox = document.getElementById("chatbox");

        chatForm.addEventListener("submit", async (e) => {
            e.preventDefault();
            const message = userInput.value.trim();
            if (!message) return;

            addMessage("You", message);
            userInput.value = "";

            try {
                const response = await fetch("/chat/", {
                    method: "POST",
                    headers: {
                        "Content-Type": "application/json",
                    },
                    body: JSON.stringify({ user_input: message }),
                });
                const data = await response.json();
                addMessage("Bot", data.response);
            } catch (error) {
                addMessage("Bot", "Error: Unable to connect to the server.");
            }
        });

        function addMessage(sender, message) {
            const messageDiv = document.createElement("div");
            messageDiv.className = "p-2 bg-gray-200 rounded-lg";
            messageDiv.innerHTML = `<strong>${sender}:</strong> ${message}`;
            chatbox.appendChild(messageDiv);
            chatbox.scrollTop = chatbox.scrollHeight;
        }
    </script>
</body>
</html>
"""

@app.route("/")
def home():
    return render_template_string(html_page)

@app.route("/chat/", methods=["POST"])
def chat():
    user_input = request.json.get('user_input')
    response = chatbot.get_response(user_input)
    return jsonify({"response": response})

if __name__ == "__main__":
    app.run(port=8000, debug=True)
