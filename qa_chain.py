import pickle

from config import EMBEDDINGS_FILE
from langchain import PromptTemplate
from langchain.chains import RetrievalQA
from langchain.chat_models import ChatOpenAI

TEMPLATE = """You are a CHAOS Architects customer success AI that answers customer questions.
    You should provide a conversational answers.
    Answer all questions as we, you are part of the team.
    Don't try to make up an answer.
    If you don't know the answer, refer to test@csm.com for more information.
    If the question is not about chaos or it's products, politely inform them 
        that you are tuned to only answer questions about CHAOS Architects 
        and it's products.

    {context}
    
    Question: {question}
    Answer:"""

PROMPT = PromptTemplate(
    template=TEMPLATE, input_variables=["context", "question"]
)


def get_qa_chain(model_name="gpt-3.5-turbo"):
    llm = ChatOpenAI(temperature=0.1, model_name=model_name)

    with open(EMBEDDINGS_FILE, "rb") as f:
        vector_store = pickle.load(f)

        retriever = vector_store.as_retriever(
            search_type="mmr", search_kwargs={"k": 2, "lambda_mult": 0.75}
        )

        return RetrievalQA.from_chain_type(
            llm=llm,
            chain_type="stuff",
            retriever=retriever,
            chain_type_kwargs={"prompt": PROMPT}
        )
