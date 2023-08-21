from qa_chain import get_qa_chain

chain = get_qa_chain()

while True:
    user_input = input('You: ')
    ai_response = chain.run(user_input)
    print(f"AI: {ai_response}")