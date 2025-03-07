from backend.feature import generate_response

# Test the chatbot with various inputs
test_inputs = [
    "hello",
    "how are you doing?",
    "what time is it?",
    "what's today's date?",
    "what's the weather like?",
    "thank you",
    "goodbye",
    "who are you?",
    "what can you do?",
    "tell me a joke",
    "what's 2+2?",
    "tell me an interesting fact",
    "what's your favorite color?",
    "can you hear me now?",
    "whats my name?"
]

print("Testing chatbot responses:")
print("-" * 50)

for input_text in test_inputs:
    response = generate_response(input_text)
    print(f"Input: {input_text}")
    print(f"Response: {response}")
    print("-" * 50)

print("Test complete!")

