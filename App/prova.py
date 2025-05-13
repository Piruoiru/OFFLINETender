from litellm import completion

messages = [{"content": "Hello, how are you?", "role": "user"}]

completion = completion(
    model="gpt-3.5-turbo",
    messages=messages
)

print(completion.choices[0].message.content)