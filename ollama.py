import requests

class ollamaChat:
    def __init__(self, model = "llama2", system = None, options = None, base_url="http://localhost:11434"):
        self.base_url = base_url
        self.model = model
        self.optional = {"system": system, "options": options}
        # Each chat will be a brand new start.
        self.context = None
        self.history = []

    # Just promt it.
    def justPrompt(self, prompt, stream=False):
        url = f"{self.base_url}/api/generate"
        data = {"model": self.model, "prompt": prompt, "stream": stream,}
        for key in self.optional.keys():
            if self.optional[key] is not None:
                data[key] = self.optional[key]
        # Add context if not the first prompt
        if self.context is not None:
            data["context"] = self.context
        try:
            http_response = requests.post(url, json=data)
            response_dict = http_response.json()
            # No matter what happens, save the history.
            self.history.append(response_dict)
            # The key 'done' must equal to true.
            assert response_dict["done"] is True, "Ollama error. Ollama LLM text generation not yet complete."
            # Update the context
            self.context = response_dict["context"]
        except Exception as e:
            print(e)
            print("raw response:>>", http_response)
        return response_dict["response"]
    
    # Use metadata to help figure out the bottle neck.
    def getAllMetadata(self,):
        return self.history
    
    # In case the context needs to be saved.
    def getCurrentContext(self,):
        return self.context


if __name__ == "__main__":
    # Example usage:
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
