# Function to respond based on user input
def chatbot_response(user_input):
    user_input = user_input.lower()

    # Greeting responses
    if "hi" in user_input or "hello" in user_input or "hey" in user_input:
        return "Hello! How can I help you today?"

    # Farewell responses
    elif "bye" in user_input or "goodbye" in user_input or "see you" in user_input:
        return "Goodbye! Have a great day!"

    # How are you responses
    elif "how are you" in user_input:
        return "I'm just a bot, but I'm here to help you!"

    # Name inquiries
    elif "what is your name" in user_input:
        return "I'm ChatBot! What's your name?"

    # Default response for unrecognized input
    else:
        return "I'm sorry, I don't understand that. Can you please rephrase?"

# Main loop to interact with the user
def chat():
    print("Welcome to ChatBot! Type 'bye' to end the conversation.")
    while True:
        user_input = input("You: ")
        if "bye" in user_input.lower() or "goodbye" in user_input.lower() or "see you" in user_input.lower():
            print("ChatBot: Goodbye! Have a great day!")
            break
        response = chatbot_response(user_input)
        print(f"ChatBot: {response}")

chat()
