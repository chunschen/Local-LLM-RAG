## Data Ingestion
from langchain_community.document_loaders import TextLoader

data_Path= "data\TheArtOfWar_SunTzu.txt"
loader=TextLoader(data_Path, encoding="utf-8")
text_documents=loader.load()


from langchain.text_splitter import RecursiveCharacterTextSplitter
text_splitter=RecursiveCharacterTextSplitter(chunk_size=1000,chunk_overlap=100)
documents=text_splitter.split_documents(text_documents)
#print(type(documents[0]))


## Vector Embedding And Vector Store
## We need a embedding model to embed sentences and paragrphs to a embedding vector.
## A embedding model that embeds sentences is needed, such as sentence transformers listed in https://huggingface.co/sentence-transformers
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.vectorstores import Chroma

ef = HuggingFaceEmbeddings(model_name="sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2")
db = Chroma.from_documents(documents,ef)
db.persist()

## Retriever: retrive top 3 relevant documents in the embedding space from db
retriever=db.as_retriever(search_type="similarity", search_kwargs={"k": 5})
retrived_documents = retriever.invoke("Thus we may know that there are five essentials for victory")
print(f"lenth of retrived_documents: {len(retrived_documents)}")
print(f"Content of retrived_documents: {retrived_documents}")

## load local LLM: mistral-instruct
from langchain_community.llms import LlamaCpp
from transformers import AutoTokenizer, AutoModelForCausalLM

n_gpu_layers = -1  # -1: trying to use all available gpu layers
n_batch = 512  # Should be between 1 and n_ctx

llm = LlamaCpp(  model_path ="F:\\unsloth\\unsloth\model-unsloth.Q4_K_M.gguf", 
                 n_gpu_layers = n_gpu_layers,
                 n_batch=n_batch,
                 n_ctx=8192,
                 max_tokens=200,
                 )

#no_context = llm.invoke("What are five essentials for victory")
#print(f"no_context: {no_context} <end of no_context>\n")

## RAG : using local LLM to answer questions according to the retrieved documents
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import PromptTemplate
from langchain_core.runnables import RunnablePassthrough
from transformers import AutoTokenizer
from langchain import hub
from langchain_core.prompts import ChatPromptTemplate
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain.chains import create_retrieval_chain

# prompt
#prompt = hub.pull("rlm/rag-prompt-llama")
prompt = ChatPromptTemplate.from_template("""
Context information is below.
---------------------
{context}
---------------------
Given the context information and not prior knowledge, answer the query in the range of 200 to 400 words.
Query: {input}
Answer:
""")

# Chain
def format_docs(docs):
    return "\n\n".join(doc.page_content for doc in docs)

document_chain = create_stuff_documents_chain(llm, prompt)
retrieval_chain = create_retrieval_chain(retriever, document_chain)

# Run
question = "What are the title of the first 3 chapters?"

print("chain invoke")

response = retrieval_chain.invoke({"input": question})
print(response["answer"])
