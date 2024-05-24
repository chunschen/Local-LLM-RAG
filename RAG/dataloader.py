## Data Ingestion
from langchain_community.document_loaders import TextLoader

data_Path= "data\TheArtOfWar_SunTzu.txt"
loader=TextLoader(data_Path, encoding="utf-8")
text_documents=loader.load()


from langchain.text_splitter import RecursiveCharacterTextSplitter
text_splitter=RecursiveCharacterTextSplitter(chunk_size=2000,chunk_overlap=200)
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
top_k_retriever=db.as_retriever(search_kwargs={"k":3})
retrived_documents = top_k_retriever.get_relevant_documents(query="Thus we may know that there are five essentials for victory")
print(retrived_documents)

