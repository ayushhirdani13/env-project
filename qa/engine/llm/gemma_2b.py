from langchain_community.llms import Ollama

def get_llm(model="gemma:2b-instruct", temperature=0.0, **kwargs):
    model = Ollama(model=model, temperature=temperature, **kwargs)

    return model