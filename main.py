from qa_chain import get_qa_chain

questions = [
    "Who are chaos's partners?",
    "How many employees does chaos have?",
    "Do you know the color 'blue'?",
    "Do you have demographic data?",
    "What kind of data do you have?"
]

chain = get_qa_chain()

for question in questions:
    print(f"Human: {question}")
    print(f"AI: {chain.run(question)}")