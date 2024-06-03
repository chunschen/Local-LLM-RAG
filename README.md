# Local-LLM-RAG

This personal project involves utilizing an open-source LLM model combined with local documents to enhance the model's knowledge and understanding of the document content.

## Start local llama3 using Ollama library
if you don'e have an Ollama installed, you can go to https://ollama.com/ and follow the instructions to download and install it on your computer.

After installation, I start the llama3 (8B) locally by issuing the following command:
```ollama run llama3:latest```
The ollama will pull the specified model to your local machine and start the it in command line:

```C:\Users\14254>ollama run llama3:latest```
```pulling manifest```
```pulling 6a0746a1ec1a... 100% ▕████████████████████████████████████████████████████████▏ 4.7 GB```
```pulling 4fa551d4f938... 100% ▕████████████████████████████████████████████████████████▏  12 KB```
```pulling 8ab4849b038c... 100% ▕████████████████████████████████████████████████████████▏  254 B```
```pulling 577073ffcc6c... 100% ▕████████████████████████████████████████████████████████▏  110 B```
```pulling 3f8eb4da87fa... 100% ▕████████████████████████████████████████████████████████▏  485 B```
```verifying sha256 digest```
```writing manifest```
```removing any unused layers```
```success```
```>>> Send a message (/? for help)```


## Libraries
<li>langchain: a framework for developing applications powered by large language models (https://python.langchain.com/v0.1/docs/get_started/introduction)
<li>Ollama: to run open-source LLM locally (https://ollama.com/)
<li>Chroma: open-source local vector db (https://www.trychroma.com/)