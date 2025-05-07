import os
from dotenv import load_dotenv
from groq import Groq

load_dotenv()
groq_api_key = os.getenv("GROQ_API_KEY")

client = Groq(api_key=groq_api_key)

def chatbot_response(user_input):
    """
    Function to get a response from the Groq chatbot.
    """
    chat_completion = client.chat.completions.create(
    messages = [
        {"role": "user",
        "content": user_input}
    ],
    model="llama-3.3-70b-versatile",
    temperature=0.7,
    max_tokens=100,
    )

    response = chat_completion.choices[0].message.content
    return response

if __name__ == "__main__":
    print("Chatbot is running. Type 'exit' to quit.")
    while True:
        user_input = input("You: ")
        if user_input.lower() == "exit":
            print("Goodbye!")
            break
        try:
            bot_response = chatbot_response(user_input)
            print(f"Bot: {bot_response}")
        except Exception as e:
            print(f"An error occurred: {e}")
