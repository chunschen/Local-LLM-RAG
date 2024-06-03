from langchain_community.document_loaders import TextLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.vectorstores import Chroma
from langchain_community.llms import Ollama
from langchain_core.prompts import ChatPromptTemplate
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain.chains import create_retrieval_chain

## Data Ingestion

DATA_PATH = "data\TheArtOfWar_SunTzu.txt"
loader=TextLoader(DATA_PATH, encoding="utf-8")
text_documents=loader.load()

#Split the text into documents
text_splitter=RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=100)
documents=text_splitter.split_documents(text_documents)

## Vector Embedding And Vector Store
## We need a embedding model to embed sentences and paragrphs to a embedding vector.
## A embedding model that embeds sentences is needed, such as sentence transformers listed
## in https://huggingface.co/sentence-transformers

SENTENCE_EMBEDDING_MODEL = "sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2"
ef = HuggingFaceEmbeddings(model_name = SENTENCE_EMBEDDING_MODEL)
db = Chroma.from_documents(documents, ef)

## Retriever: retrive top 5 relevant documents in the embedding space from db
k = 5
retriever=db.as_retriever(search_type="similarity", search_kwargs={"k": k})
retrived_documents = retriever.invoke("Thus we may know that there are five essentials for victory")
print(f"lenth of retrived_documents: {len(retrived_documents)}")
print(f"Content of retrived_documents: {retrived_documents}")

## load local llama3(8B) using Ollama

llm = Ollama(model="llama3:latest")

## RAG : using local LLM to answer questions according to the retrieved documents

# prompt
prompt = ChatPromptTemplate.from_template("""
[inst]Answer the following question based only on the provided context:[/inst]

<context>
{context}
</context>

Q: {input} A:""") 

# Chain

document_chain = create_stuff_documents_chain(llm, prompt)
retrieval_chain = create_retrieval_chain(retriever, document_chain)

# Run the query through the defined chain;
QUESTION = "Who is the author of the book: the art of war?"

# Question -> RETRIEVER ->prepare PROMPT by combining retrived documents and the question -> LLM -> Answer 
response = retrieval_chain.invoke({"input": QUESTION})
print(response["answer"])
