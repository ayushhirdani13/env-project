import gradio as gr

from qa.engine.llm import get_llm
from qa.engine.rag import make_rag_chain
# from qa.sample_questions import QUESTIONS
# from qa.constants import POSSIBLE_REPORTS

llm = get_llm(provider='gemma_2b')

chain = make_rag_chain(llm)

def chat(input, _):
    response = chain.invoke(input)
    return response
# --------------------------------------------------------------------
# Gradio
# --------------------------------------------------------------------

theme = gr.themes.Base(
    primary_hue="blue",
    secondary_hue="red",
    font=[gr.themes.GoogleFont("Poppins"), "ui-sans-serif", "system-ui", "sans-serif"],
)

init_prompt = """
Hello, I am Climate-X, a conversational assistant designed to help you understand climate change and biodiversity loss. I will answer your questions by **sifting through the IPCC and IPBES scientific reports**.

⚠️ Limitations
*Please note that the AI is not perfect and may sometimes give irrelevant answers. If you are not satisfied with the answer, please ask a more specific question or report your feedback to help us improve the system.*

What do you want to learn ?
"""

iface = gr.ChatInterface(fn=chat, theme=theme, undo_btn=None, title='Climate-X')

iface.queue()
iface.launch()