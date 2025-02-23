import os
import json

from langchain_community.chat_models import ChatOpenAI
from langchain_community.llms import OpenAI
from langchain_community.embeddings import OpenAIEmbeddings
from langchain_community.vectorstores import FAISS
from langchain.chains import RetrievalQA
from langchain.text_splitter import RecursiveCharacterTextSplitter


OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

def load_articles():
    """Load articles from JSON and return as list of strings."""
    try:
        with open("data/articles.json", "r", encoding="utf-8") as f:
            articles = json.load(f)
        if not articles:
            return []
        docs = []
        for article in articles:
            content = f"Title: {article['title']}\nContent: {article['content']}\nURL: {article['url']}"
            docs.append(content)
        return docs
    except Exception as e:
        print(f"❌ Error loading articles: {e}")
        return []

def create_vector_store():
    """Convert articles into embeddings for retrieval."""
    articles = load_articles()
    if not articles:
        return None

    embeddings = OpenAIEmbeddings(openai_api_key=OPENAI_API_KEY)
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=50)
    docs = text_splitter.create_documents(articles)

    vector_store = FAISS.from_documents(docs, embeddings)
    return vector_store

def create_chatbot():
    """Create an OpenAI-powered chatbot with retrieval capabilities."""
    vector_store = create_vector_store()
    llm = ChatOpenAI(
        model_name="gpt-4",
        openai_api_key=OPENAI_API_KEY
    )

    if vector_store:
        retriever = vector_store.as_retriever(search_type="similarity", search_kwargs={"k":3})
        # ✅ Use from_chain_type instead of direct constructor
        return RetrievalQA.from_chain_type(
            llm=llm,
            chain_type="stuff",
            retriever=retriever
        )
    else:
        # If no articles found, fallback to direct LLM usage
        return llm

def ask_question(query: str) -> str:
    """Ask a question to the chatbot. Returns a string response."""
    chatbot = create_chatbot()
    if isinstance(chatbot, ChatOpenAI):
        # fallback: just LLM with no retrieval
        return chatbot.predict(query)
    else:
        # run the retrieval QA chain
        return chatbot.run(query)
