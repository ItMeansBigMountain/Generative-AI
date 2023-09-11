import os
import sys

import openai
from langchain.chains import ConversationalRetrievalChain, RetrievalQA
from langchain.chat_models import ChatOpenAI
from langchain.document_loaders import DirectoryLoader, TextLoader, WebBaseLoader
from langchain.embeddings import OpenAIEmbeddings
from langchain.indexes import VectorstoreIndexCreator
from langchain.indexes.vectorstore import VectorStoreIndexWrapper
from langchain.llms import OpenAI
from langchain.vectorstores import Chroma

import constants




# OPENAI API KEY
os.environ["OPENAI_API_KEY"] =  constants.APIKEY
os.environ["OPENAI_ORGANIZATION_ID"] = constants.ORGANIZATION_ID


# USER INPUT
q = input("> ")


# LOAD PERSONAL DATA 
loader = TextLoader("notes.txt")
# loader = DirectoryLoader(".", glob="*.txt")
# loader = WebBaseLoader("https://github.com/ItMeansBigMountain")



# VECTOR DATABASE THAT HOLDS PERSONAL INFORMATION
index = VectorstoreIndexCreator().from_loaders([loader])



# LLM RESPONSE 
r = index.query(
    question=q,
    llm=ChatOpenAI()
)



print( r )