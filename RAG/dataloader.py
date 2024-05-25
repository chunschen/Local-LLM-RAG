from langchain_community.document_loaders import TextLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.vectorstores import Chroma
from langchain_community.llms import LlamaCpp
from langchain_core.prompts import ChatPromptTemplate
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain.chains import create_retrieval_chain

## Data Ingestion

data_Path= "data\TheArtOfWar_SunTzu.txt"
loader=TextLoader(data_Path, encoding="utf-8")
text_documents=loader.load()

#Split the text into documents
text_splitter=RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=100)
documents=text_splitter.split_documents(text_documents)

## Vector Embedding And Vector Store
## We need a embedding model to embed sentences and paragrphs to a embedding vector.
## A embedding model that embeds sentences is needed, such as sentence transformers listed in https://huggingface.co/sentence-transformers
sentence_embedding_model = "sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2"
ef = HuggingFaceEmbeddings(model_name = sentence_embedding_model)
db = Chroma.from_documents(documents, ef)
db.persist()

## Retriever: retrive top 5 relevant documents in the embedding space from db
k = 5
retriever=db.as_retriever(search_type="similarity", search_kwargs={"k": k})
retrived_documents = retriever.invoke("Thus we may know that there are five essentials for victory")
print(f"lenth of retrived_documents: {len(retrived_documents)}")
print(f"Content of retrived_documents: {retrived_documents}")

## load local LLM: mistral-instruct

n_gpu_layers = -1  # -1: trying to use all available gpu layers
n_ctx = 2000  # context size of the model
n_batch = 512  # Should be between 1 and n_ctx

llm = LlamaCpp(  model_path ="F:\\unsloth\\unsloth\model-unsloth.Q4_K_M.gguf", # the path of the local llm model
                n_gpu_layers = n_gpu_layers,
                 n_batch=n_batch,
                 n_ctx=n_ctx,
                 max_tokens=200,
                 verbose=True,
                 thread=12
                 )

#no_context = llm.invoke("What are five essentials for victory")
#print(f"no_context: {no_context} <end of no_context>\n")

## RAG : using local LLM to answer questions according to the retrieved documents

# prompt
prompt = ChatPromptTemplate.from_template("""
Answer the following question based only on the provided context:

<context>
{context}
</context>

Question: {input}""")

# Chain
def format_docs(docs):
    return "\n\n".join(doc.page_content for doc in docs)

document_chain = create_stuff_documents_chain(llm, prompt)
retrieval_chain = create_retrieval_chain(retriever, document_chain)

# Run
question = "What are the title of the first 3 chapters of the book: the art of war?"

response = retrieval_chain.invoke({"input": question})
print(response["answer"])
