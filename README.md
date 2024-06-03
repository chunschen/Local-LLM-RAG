# Local-LLM-RAG

This personal project involves utilizing an open-source LLM model combined with local documents to enhance the model's knowledge and understanding of the document content.

## Start llama3 locally with Ollama
### CLI Example
If Ollama is not installed,go to https://ollama.com/ to download and install it on your computer.

After installation, run llama3(8B) locally in interactive mode by issuing the following CLI commands:
```ollama run llama3:latest```
Ollama will pull the specified model from registry to your local machine and running it locally:
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
`/bye` to exit the interactive mode. This ends the connection to the model hosted by Ollama, but the LLM model is still loaded in the memory for 5 minutes(default keep_alive = 5m). You can change the behavior by setting the `OLLAMA_KEEP_ALIVE` environment variable when starting the Ollama server. (refer to: https://github.com/ollama/ollama/blob/c02db93243353855b983db2a1562a02b57e66db1/docs/faq.md#how-do-i-keep-a-model-loaded-in-memory-or-make-it-unload-immediately)

You can also add your prompt to the command, Ollama will respond with the generated message. Model will be loaded into the memory if it is not already loaded:
`ollama run llama3:latest "why the sky is blue?"`
```
C:\Users\14254>ollama run llama3:latest "why the sky is blue?"
What a great question!

The short answer is: the sky appears blue because of a phenomenon called Rayleigh scattering, named after the British physicist Lord Rayleigh. Here's
why:

1. **Light from the sun**: When sunlight enters Earth's atmosphere, it contains all the colors of the visible spectrum (red, orange, yellow, green,
blue, indigo, and violet).
2. **Molecules in the air**: The air is made up of tiny molecules like nitrogen (N2) and oxygen (O2). These molecules are much smaller than the
wavelength of light.
3. **Scattering occurs**: When sunlight hits these molecules, it scatters in all directions. This scattering is more pronounced for shorter
wavelengths, like blue and violet light, due to their smaller size.

Here's what happens:

* Longer wavelengths (like red and orange) travel in a relatively straight line, reaching our eyes with little scattering.
* Shorter wavelengths (like blue and violet) are scattered in all directions by the tiny molecules. This is known as Rayleigh scattering.
* Our atmosphere contains more nitrogen (N2) than oxygen (O2), which absorbs some of the shorter wavelengths, making them less visible to our eyes.

As a result, the scattered blue light reaches our eyes from all directions, giving the sky its blue appearance! The color we see is actually an
average of all the scattered blue light mixed with the direct sunlight that hasn't been scattered as much.

In summary:

* Blue light is scattered more than other colors by tiny molecules in the air.
* Our atmosphere absorbs some shorter wavelengths, making them less visible.
* The scattered blue light reaches our eyes from all directions, giving the sky its blue color.

Now, go enjoy the blue sky and appreciate the science behind it!
```
### API example:
Ollama binds 127.0.0.1 port 11434 by default, our local RAG app can interact with the local LLM by sending requests to the localhost(127.0.0.1) and port 11434.
Here is an example of using `curl` to connect to Ollama's `generate` api for thee llama3 model:
`curl http://localhost:11434/api/generate -d "{\"model\": \"llama3:latest\", \"keep_alive\": 0, \"prompt\": \"Why is the sky blue?\", \"stream\": false}"`
```
C:\Users\14254>curl http://localhost:11434/api/generate -d "{\"model\": \"llama3:latest\", \"keep_alive\": \"3m\", \"prompt\": \"Why is the sky blue?\", \"stream\": false}"
{"model":"llama3:latest","created_at":"2024-06-03T19:20:04.3460261Z","response":"The sky appears blue because of a phenomenon called Rayleigh scattering. This occurs when sunlight interacts with tiny molecules of gases in the Earth's atmosphere, such as nitrogen (N2) and oxygen (O2).\n\nHere's what happens:\n\n1. Sunlight enters the Earth's atmosphere, comprising all colors of the visible spectrum (red, orange, yellow, green, blue, indigo, and violet).\n2. As sunlight travels through the atmosphere, it encounters tiny molecules of gases like nitrogen and oxygen.\n3. These molecules scatter the shorter, blue wavelengths of light more efficiently than the longer, red wavelengths. This is because the smaller molecules are better at scattering shorter wavelengths.\n4. The scattered blue light is then dispersed throughout the atmosphere in all directions, reaching our eyes from all parts of the sky.\n\nThe combined effect of this scattering process makes the sky appear blue during the daytime, especially when the sun is overhead (around noon). The color intensity can vary depending on atmospheric conditions, such as:\n\n* Dust and pollution particles: These can scatter shorter wavelengths, making the sky appear more hazy or gray.\n* Water vapor: High humidity can increase the scattering of light, resulting in a more intense blue color.\n* Clouds: Clouds can reflect and scatter sunlight, changing the apparent color of the sky.\n\nIt's worth noting that the sky can take on different hues during sunrise and sunset due to the scattering of longer wavelengths (like red and orange) by atmospheric particles. This is known as Rayleigh scattering again, but with a twist – the shorter blue wavelengths are scattered more effectively than the longer wavelengths, resulting in those beautiful warm colors we see during these times.\n\nSo, that's why the sky appears blue!","done":true,"done_reason":"stop","context":[128006,882,128007,271,10445,374,279,13180,6437,30,128009,128006,78191,128007,271,791,13180,8111,6437,1606,315,264,25885,2663,13558,64069,72916,13,1115,13980,994,40120,84261,449,13987,35715,315,45612,304,279,9420,596,16975,11,1778,439,47503,320,45,17,8,323,24463,320,46,17,3677,8586,596,1148,8741,1473,16,13,8219,4238,29933,279,9420,596,16975,11,46338,682,8146,315,279,9621,20326,320,1171,11,19087,11,14071,11,6307,11,6437,11,1280,7992,11,323,80836,4390,17,13,1666,40120,35292,1555,279,16975,11,433,35006,13987,35715,315,45612,1093,47503,323,24463,627,18,13,4314,35715,45577,279,24210,11,6437,93959,315,3177,810,30820,1109,279,5129,11,2579,93959,13,1115,374,1606,279,9333,35715,527,2731,520,72916,24210,93959,627,19,13,578,38067,6437,3177,374,1243,77810,6957,279,16975,304,682,18445,11,19261,1057,6548,505,682,5596,315,279,13180,382,791,11093,2515,315,420,72916,1920,3727,279,13180,5101,6437,2391,279,62182,11,5423,994,279,7160,374,32115,320,20019,38245,570,578,1933,21261,649,13592,11911,389,45475,4787,11,1778,439,1473,9,33093,323,25793,19252,25,4314,649,45577,24210,93959,11,3339,279,13180,5101,810,305,13933,477,18004,627,9,10164,38752,25,5234,38193,649,5376,279,72916,315,3177,11,13239,304,264,810,19428,6437,1933,627,9,15161,82,25,15161,82,649,8881,323,45577,40120,11,10223,279,10186,1933,315,279,13180,382,2181,596,5922,27401,430,279,13180,649,1935,389,2204,82757,2391,64919,323,44084,4245,311,279,72916,315,5129,93959,320,4908,2579,323,19087,8,555,45475,19252,13,1115,374,3967,439,13558,64069,72916,1578,11,719,449,264,27744,1389,279,24210,6437,93959,527,38067,810,13750,1109,279,5129,93959,11,13239,304,1884,6366,8369,8146,584,1518,2391,1521,3115,382,4516,11,430,596,3249,279,13180,8111,6437,0,128009],"total_duration":15815028000,"load_duration":1028900,"prompt_eval_duration":294653000,"eval_count":346,"eval_duration":15517806000}
```

To learn more about Ollama configuration and APIs, please refer to Ollama's FAQ page: https://github.com/ollama/ollama/blob/main/docs/faq.md
## Libraries
<li>langchain: a framework for developing applications powered by large language models (https://python.langchain.com/v0.1/docs/get_started/introduction)
<li>Ollama: to run open-source LLM locally (https://ollama.com/)
<li>Chroma: open-source local vector db (https://www.trychroma.com/)