from arrow import get
from qa.engine.llm.gemma_2b import get_llm as get_gemma_2b
from qa.engine.llm.llama2 import get_llm as get_llama2

def get_llm(provider='gemma_2b', **kwargs):
    if provider=='gemma_2b':
        return get_gemma_2b(**kwargs)
    if provider=='llama2':
        return get_llama2(**kwargs)
    else:
        raise ValueError(f"Unknown provider: {provider}")
