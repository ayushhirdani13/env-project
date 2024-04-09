from langchain_community.llms import Ollama

def get_llm(model="llama2", temperature=0.0, **kwargs):
    model = Ollama(model=model, temperature=temperature, **kwargs)

    return model