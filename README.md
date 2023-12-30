# ollama_python_interface

The `ollamaChat` class designed to interact with a chat-based language model. This class provides functionalities to send prompts to the model, handle responses, and maintain the context and history of the conversation.

- Each new instance of `ollamaChat(model, system)` is a new conversation. 
- In each conversation, user can ask multiple questions by call `justPrompt` repeatedly.

## Note

- **Make sure ollama is running when using this class.**

## Example usage:

```python
model = "llama2"
system = "You are a scientist. Answer all of the questions and explaining the scientific principles involved. The response should be detailed."
ollama = ollamaChat(model, system)

# First question
q1 = "Why is the sky blue?"
print("user:>>", q1)
response = ollama.justPrompt(q1)
print("LLM:>>", response)

# 2nd question in the same context
q2 = "What else tiny molecules of gases may also affect this phenomenon?"
print("user:>>", q2)
response = ollama.justPrompt(q2)
print("LLM:>>", response)
```


## Class Difination

### Constructor: `__init__(self, model="llama2", system=None, options=None, base_url="http://localhost:11434")`
- **Parameters:**
  - `model`: The model name (default: "llama2").
  - `system`: Optional system configuration.
  - `options`: Additional options. 
  - `base_url`: The base URL for the API (default: "http://localhost:11434").
- **Functionality:**
  - Initializes the class with model, system, options, base URL.
  - Sets up an empty context and history list.
- **Valid options**

| Parameter      | Description                                                                                                                                                                                                                                             | Value Type | Example Usage        |
| -------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ---------- | -------------------- |
| mirostat       | Enable Mirostat sampling for controlling perplexity. (default: 0, 0 = disabled, 1 = Mirostat, 2 = Mirostat 2.0)                                                                                                                                         | int        | mirostat 0           |
| mirostat_eta   | Influences how quickly the algorithm responds to feedback from the generated text. A lower learning rate will result in slower adjustments, while a higher learning rate will make the algorithm more responsive. (Default: 0.1)                        | float      | mirostat_eta 0.1     |
| mirostat_tau   | Controls the balance between coherence and diversity of the output. A lower value will result in more focused and coherent text. (Default: 5.0)                                                                                                         | float      | mirostat_tau 5.0     |
| num_ctx        | Sets the size of the context window used to generate the next token. (Default: 2048)                                                                                                                                                                    | int        | num_ctx 4096         |
| num_gqa        | The number of GQA groups in the transformer layer. Required for some models, for example it is 8 for llama2:70b                                                                                                                                         | int        | num_gqa 1            |
| num_gpu        | The number of layers to send to the GPU(s). On macOS it defaults to 1 to enable metal support, 0 to disable.                                                                                                                                            | int        | num_gpu 50           |
| num_thread     | Sets the number of threads to use during computation. By default, Ollama will detect this for optimal performance. It is recommended to set this value to the number of physical CPU cores your system has (as opposed to the logical number of cores). | int        | num_thread 8         |
| repeat_last_n  | Sets how far back for the model to look back to prevent repetition. (Default: 64, 0 = disabled, -1 = num_ctx)                                                                                                                                           | int        | repeat_last_n 64     |
| repeat_penalty | Sets how strongly to penalize repetitions. A higher value (e.g., 1.5) will penalize repetitions more strongly, while a lower value (e.g., 0.9) will be more lenient. (Default: 1.1)                                                                     | float      | repeat_penalty 1.1   |
| temperature    | The temperature of the model. Increasing the temperature will make the model answer more creatively. (Default: 0.8)                                                                                                                                     | float      | temperature 0.7      |
| seed           | Sets the random number seed to use for generation. Setting this to a specific number will make the model generate the same text for the same prompt. (Default: 0)                                                                                       | int        | seed 42              |
| stop           | Sets the stop sequences to use. When this pattern is encountered the LLM will stop generating text and return. Multiple stop patterns may be set by specifying multiple separate `stop` parameters in a modelfile.                                      | string     | stop "AI assistant:" |
| tfs_z          | Tail free sampling is used to reduce the impact of less probable tokens from the output. A higher value (e.g., 2.0) will reduce the impact more, while a value of 1.0 disables this setting. (default: 1)                                               | float      | tfs_z 1              |
| num_predict    | Maximum number of tokens to predict when generating text. (Default: 128, -1 = infinite generation, -2 = fill context)                                                                                                                                   | int        | num_predict 42       |
| top_k          | Reduces the probability of generating nonsense. A higher value (e.g. 100) will give more diverse answers, while a lower value (e.g. 10) will be more conservative. (Default: 40)                                                                        | int        | top_k 40             |
| top_p          | Works together with top-k. A higher value (e.g., 0.95) will lead to more diverse text, while a lower value (e.g., 0.5) will generate more focused and conservative text. (Default: 0.9)                                                                 | float      | top_p 0.9            |

### Method: `justPrompt(self, prompt, stream=False)`
- **Parameters:**
  - `prompt`: The prompt to send to the model.
  - `stream`: Whether to stream the response (default: False).
- **Functionality:**
  - Sends a prompt to the model and handles the response.
  - Updates the context and history after receiving the response.
- **Returns:**
  - The response from the model.

### Method: `getAllMetadata(self)`
- **Functionality:**
  - Retrieves the entire history of prompts and responses.
- **Returns:**
  - History list containing all metadata.
- **How to use metadata to find the performance bottle neck**
  - `total_duration`: time spent generating the response
  - `load_duration`: time spent in nanoseconds loading the model
  - `prompt_eval_count`: number of tokens in the prompt
  - `prompt_eval_duration`: time spent in nanoseconds evaluating the prompt
  - `eval_count`: number of tokens the response
  - `eval_duration`: time in nanoseconds spent generating the response
  - `context`: an encoding of the conversation used in this response, this can be sent in the next request to keep a conversational memory
  - `response`: empty if the response was streamed, if not streamed, this will contain the full response

### Method: `getCurrentContext(self)`
- **Functionality:**
  - Retrieves the current context of the conversation.
- **Returns:**
  - The current context.

