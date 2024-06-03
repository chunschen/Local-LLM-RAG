from langchain_community.document_loaders import TextLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.vectorstores import Chroma
from langchain_community.llms import LlamaCpp
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
db.persist()

## Retriever: retrive top 5 relevant documents in the embedding space from db
k = 5
retriever=db.as_retriever(search_type="similarity", search_kwargs={"k": k})
retrived_documents = retriever.invoke("Thus we may know that there are five essentials for victory")
print(f"lenth of retrived_documents: {len(retrived_documents)}")
print(f"Content of retrived_documents: {retrived_documents}")

## load local LLM: mistral-instruct

N_GPU_LAYERS = -1  # -1: trying to use all available gpu layers
N_CTX = 2000  # context size of the model
N_BATCH = 512  # Should be between 1 and n_ctx

llm = LlamaCpp(  model_path = 'F:\\unsloth\\unsloth\\meta-llama-3-8b-instruct-imat-Q4_K_M.gguf', # the path of the local llm model
                 #n_gpu_layers = N_GPU_LAYERS,
                 n_batch = N_BATCH,
                 n_ctx = N_CTX,
                 max_tokens = 200,
                 verbose = True,
                 thread = 12
                 )

#no_context = llm.invoke("What are five essentials for victory")
#print(f"no_context: {no_context} <end of no_context>\n")

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

# Run
QUESTION = "What are the title of the first 3 chapters of the book: the art of war?"

response = retrieval_chain.invoke({"input": QUESTION})
print(response["answer"])
