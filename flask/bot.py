# Core imports
import os

import chromadb
from chromadb.config import Settings
from sentence_transformers import SentenceTransformer
# LangChain components
from langchain.vectorstores import Chroma  # Vector database
from chromadb.utils import embedding_functions
from langchain.schema import Document  # Document schema
# LangChain community-specific components

# LangChain OpenAI components
from langchain_openai import OpenAI, ChatOpenAI, OpenAIEmbeddings  # OpenAI utilities

# LangChain Core components
from langchain_core.documents.base import Document  # Base document class

# LangChain Groq components
from langchain_groq import ChatGroq  # Groq-specific chat model

os.environ["GROQ_API_KEY"] = None# insert API key here

if not os.environ["GROQ_API_KEY"]: 
    throw new Error("Insert a Groq API key.")

from langchain.schema import HumanMessage, SystemMessage, AIMessage

class ChatBot:
    def __init__(self,book_text):
        # Load your model (ChatGroq in this case)
        self.chat_model = ChatGroq(model="llama3-70b-8192")
        # Define the system prompt for the agent
        self.system_prompt = SystemMessage(content="""
        You are an expert on the following topic below. Summarize the text below and answer questions using your knowledge and from the text below:""" + book_text)
        self.messages = [self.system_prompt]

    # Function to interact with the agent
    def chat_with_agent(self,user_input):
        self.messages.append(HumanMessage(content=user_input))
        response = self.chat_model(self.messages)
        self.messages.append(AIMessage(content=response.content))
        return response.content
    
    # def chat_loop(self):
    #     print("Chat with your agent! Type 'exit' to quit.")
    #     response = self.chat_with_agent("Summarize the text")
    #     print(f"Agent: {response}")
    #     while True:
    #         user_input = input("You: ")
    #         if user_input.lower() in ["exit", "quit"]:
    #             print("Goodbye!")
    #             break
    #         response = self.chat_with_agent(user_input)
    #         print(f"Agent: {response}")

class VectorDB:
    def __init__(self):
        # Initialize ChromaDB client
        self.client = chromadb.Client()
        self.collection = self.client.create_collection(name="books")
        self.count = 0
    def add_book(self, book_title):
        self.count +=1
        # Add the title and embedding to the collection
        self.collection.add(
            documents=[book_title],
            ids=[str(self.count)]
        )

        print(f"Added book: {book_title}")

    def find_book(self,query_title, top_n=3):
        # Embed the query title
        results = self.collection.query(
        query_texts=[query_title], # Chroma will embed this for you
        n_results=top_n)
        print(results['documents'])
        print(results['distances'])
        return results