# Local-LLM-RAG

This personal project involves utilizing an open-source LLM model combined with local documents to enhance the model's knowledge and understanding of the document content.

## Start local llama3 using Ollama library
if you don'e have an Ollama installed, you can go to https://ollama.com/ and follow the instructions to download and install it on your computer.

After installation, I start the llama3 (8B) locally by issuing the following command:
```ollama run llama3:latest```
The ollama will pull the specified model to your local machine and start the it in command line:
```
C:\Users\14254>ollama run llama3:latest
pulling manifest
pulling 6a0746a1ec1a... 100% ▕████████████████████████████████████████████████████████▏ 4.7 GB
pulling 4fa551d4f938... 100% ▕████████████████████████████████████████████████████████▏  12 KB
pulling 8ab4849b038c... 100% ▕████████████████████████████████████████████████████████▏  254 B
pulling 577073ffcc6c... 100% ▕████████████████████████████████████████████████████████▏  110 B
pulling 3f8eb4da87fa... 100% ▕████████████████████████████████████████████████████████▏  485 B
verifying sha256 digest
writing manifest
removing any unused layers
success
>>> Send a message (/? for help)
```
`/bye` to exit the command line mode. It ends the command line connection to the model hosted by Ollama, but service is still running in the background.
you can verify it by issuing the command `ollama ps` to see the running model.
```
C:\Users\14254>ollama ps
NAME            ID              SIZE    PROCESSOR       UNTIL
llama3:latest   365c0bd3c000    5.4 GB  3%/97% CPU/GPU  3 minutes from now
```
Ollama binds 127.0.0.1 port 11434 by default, our local RAG app will send requests to this address:port. The default can be canged by setting the `OLLAMA_HOST ` environment variable. 

To learn more about Ollama configuration, please refer to Ollama's FAQ page: https://github.com/ollama/ollama/blob/main/docs/faq.md
## Libraries
<li>langchain: a framework for developing applications powered by large language models (https://python.langchain.com/v0.1/docs/get_started/introduction)
<li>Ollama: to run open-source LLM locally (https://ollama.com/)
<li>Chroma: open-source local vector db (https://www.trychroma.com/)