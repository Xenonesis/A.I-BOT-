import json
from transformers import AutoModelForCausalLM, AutoTokenizer

class Chatbot:
    def __init__(self, model_name="microsoft/DialoGPT-medium", storage_file="conversation.json"):
        # Load a pre-trained model and tokenizer
        self.tokenizer = AutoTokenizer.from_pretrained(model_name)
        self.model = AutoModelForCausalLM.from_pretrained(model_name)
        self.chat_history = []
        self.storage_file = storage_file

        # Load previous conversation, if available
        self.load_conversation()

    def get_response(self, user_input):
        # Add user input to chat history
        self.chat_history.append(user_input)

        # Tokenize the input with the chat history for context
        input_ids = self.tokenizer.encode(
            " ".join(self.chat_history[-5:]) + self.tokenizer.eos_token,  # Limit history for performance
            return_tensors="pt",
        )

        # Generate a response
        chat_history_ids = self.model.generate(
            input_ids,
            max_length=1000,
            pad_token_id=self.tokenizer.eos_token_id,
        )

        # Decode the model's response
        bot_response = self.tokenizer.decode(
            chat_history_ids[:, input_ids.shape[-1]:][0],
            skip_special_tokens=True,
        )

        # Add bot response to chat history
        self.chat_history.append(bot_response)
        return bot_response

    def save_conversation(self):
        # Save the conversation to a local file
        try:
            with open(self.storage_file, "w") as f:
                json.dump(self.chat_history, f, indent=2)
            print(f"Conversation saved to {self.storage_file}.")
        except Exception as e:
            print(f"Error saving conversation: {e}")

    def load_conversation(self):
        # Load conversation from the local file
        try:
            with open(self.storage_file, "r") as f:
                self.chat_history = json.load(f)
            print("Previous conversation loaded.")
        except FileNotFoundError:
            print("No previous conversation found. Starting fresh.")
        except Exception as e:
            print(f"Error loading conversation: {e}")

# Main chat loop
if __name__ == "__main__":
    chatbot = Chatbot()
    print("Chatbot is ready! Type 'exit' to end the conversation.")

    while True:
        user_input = input("You: ").strip()
        if user_input.lower() == "exit":
            print("Goodbye!")
            chatbot.save_conversation()
            break
        elif not user_input:
            print("Please enter some text!")
            continue

        response = chatbot.get_response(user_input)
        print(f"Bot: {response}")
