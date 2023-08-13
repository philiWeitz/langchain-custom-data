from chat_chain import get_chat_chain
from qa_chain import get_qa_chain

questions = [
    "Who are chaos's partners?",
    "How many employees does chaos have?",
    "Do you know the color 'blue'?",
    "What are it's values?",
    "Who is the CEO?",
    "What's the yearly revenue?"
]

# chain = get_chat_chain()
chain = get_qa_chain()

for question in questions:
    print(f"Human: {question}")
    print(f"AI: {chain.run(question)}")