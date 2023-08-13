import pickle

from config import EMBEDDINGS_FILE
from langchain import PromptTemplate
from langchain.chains import ConversationChain
from langchain.chat_models import ChatOpenAI
from langchain.memory import VectorStoreRetrieverMemory

TEMPLATE = """
    You are a CHAOS Architects customer success AI that answers customer questions.
    You should provide a conversational answers.
    If you don't know the answer, refer to test@csm.com for more information.
    Don't try to make up an answer.
    If the question is not about chaos or it's products, politely inform them that you are tuned to only answer questions about CHAOS Architects and it's products.

    Relevant pieces of previous conversation:
    {history}

    (You do not need to use these pieces of information if not relevant)

    Current conversation:
    Human: {input}
    AI:"""


def get_chat_chain(model_name="gpt-3.5-turbo"):
    llm = ChatOpenAI(temperature=0, model_name=model_name)

    with open(EMBEDDINGS_FILE, "rb") as f:
        vector_store = pickle.load(f)

        memory = VectorStoreRetrieverMemory(
            retriever=vector_store.as_retriever()
        )

        prompt = PromptTemplate(
            input_variables=["history", "input"], template=TEMPLATE
        )
        return ConversationChain(
            llm=llm, prompt=prompt, memory=memory, verbose=False
        )
