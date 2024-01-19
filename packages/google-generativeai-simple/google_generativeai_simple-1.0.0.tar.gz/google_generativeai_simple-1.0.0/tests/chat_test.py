from genai import Chat

assistant_name: str = "Google"
user_name: str = "John"
api_key: str = "AIzaSyBGp2_7lqFPa_FQnrKZuLrR7eJy06ZetLs"
assistant = Chat(assistant_name, user_name, api_key)
while True:
    query = input(f"{user_name}: ")
    response = assistant.run(query)
    print(f"\nTim: {response}")