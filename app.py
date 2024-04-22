import gradio as gr

from langchain_community.embeddings.sentence_transformer import (
    SentenceTransformerEmbeddings,
)

embedding = SentenceTransformerEmbeddings(
    model_name="sentence-transformers/all-MiniLM-L6-v2"
)

from qa.engine.llm import get_llm
from qa.engine.rag import make_rag_chain
from qa.engine.vectorstore import get_vectorstore
from qa.engine.retriever import ClimateXRetriever
from qa.templates import QUESTIONS
import re

dir = "chroma_db"
db = "guardian" if dir == "chroma_db_guardian" else "chroma_db"

llm = get_llm(provider="gemma_2b")
vectorstore = get_vectorstore(embeddings=embedding, dir=dir)
retriever = ClimateXRetriever(vectorstore=vectorstore, db=db)

chain = make_rag_chain(retriever=retriever, llm=llm)


def parse_output_llm_with_sources(output):
    # Split the content into a list of text and "[Doc X]" references
    content_parts = re.split(r"\[(Doc\s?\d+(?:,\s?Doc\s?\d+)*)\]", output)
    parts = []
    for part in content_parts:
        if part.startswith("Doc"):
            subparts = part.split(",")
            subparts = [
                subpart.lower().replace("doc", "").strip() for subpart in subparts
            ]
            subparts = [
                f"""<a href="#doc{subpart}" class="a-doc-ref" target="_self"><span class='doc-ref'><sup>{subpart}</sup></span></a>"""
                for subpart in subparts
            ]
            parts.append("".join(subparts))
        else:
            parts.append(part)
    content_parts = "".join(parts)
    return content_parts


def make_html_source(source, i, db="chroma_db"):
    meta = source.metadata
    # print(meta)
    # content = source.page_content.split(":",1)[1].strip()
    content = source.page_content.strip()

    card = None

    if db == "guardian":
        meta['Authors'] = ','.join(eval(meta['Authors']))
        card = f"""
        <div class="card" id="doc{i}">
            <div class="card-content">
                <h2>Doc {i} - "{meta['Title']}"
                    by: {meta['Authors']}</h2>
                <p>{content}</p>
            </div>
        </div>
        """
    else:
        card = f"""
        <div class="card" id="doc{i}">
            <div class="card-content">
                <h2>Doc {i} - {meta['source_name']} - Page {int(meta['page'])}</h2>
                <p>{content}</p>
            </div>
            <div class="card-footer">
                <a href="{meta['source']}#page={int(meta['page'])}" target="_blank" class="pdf-link">
                    <span role="img" aria-label="Open PDF">🔗</span>
                </a>
            </div>
        </div>
        """

    return card


async def chat(query, history):
    input = {"question": query}
    response = chain.astream_log(input)

    path_retriever = "/logs/find_docs/final_output"
    path_answer = "/logs/answer/streamed_output_str/-"

    try:
        async for chunks in response:
            chunk = chunks.ops[0]
            if chunk["path"] == path_retriever:  # documents
                try:
                    docs = chunk["value"]["docs"]  # List[Document]
                    docs_html = []
                    for i, d in enumerate(docs, 1):
                        docs_html.append(make_html_source(d, i, db))
                    docs_html = "".join(docs_html)
                except TypeError:
                    print("No documents found")
                    print("chunk: ", chunk)
                    continue

            elif chunk["path"] == path_answer:  # final answer
                try:
                    # print("Deb app.py:", chunk)
                    new_token = chunk["value"]  # str
                    # time.sleep(0.01)
                    previous_answer = history[-1][1]
                    previous_answer = (
                        previous_answer if previous_answer is not None else ""
                    )
                    answer_yet = previous_answer + new_token
                    answer_yet = parse_output_llm_with_sources(answer_yet)
                    history[-1] = (query, answer_yet)
                except TypeError:
                    print("This is TypeError.")
                    continue

            else:
                continue

        history = [tuple(x) for x in history]
        yield history, docs_html

    except Exception as e:
        raise gr.Error(f"{e}")

    yield history, docs_html


# --------------------------------------------------------------------
# Gradio
# --------------------------------------------------------------------

theme = gr.themes.Soft(
    font=[gr.themes.GoogleFont("Poppins"), "ui-sans-serif", "system-ui", "sans-serif"],
)

init_prompt = """
Hello, I am Climate-X, a conversational assistant designed to help you understand climate change and biodiversity loss.

- I answer questions based on IPCC Reports 2023 or [Guardian](https://theguardian.com) Articles.
- I may provide wrong or insufficient answers sometimes. I am at an early stage so my responses may not be upto the mark.

⚠️ Limitations
*Please note that the AI is not perfect and may sometimes give irrelevant answers. If you are not satisfied with the answer, please ask a more specific question or report your feedback to help us improve the system.*

What do you want to learn ?
"""

with gr.Blocks(title="Climate-X", theme=theme, elem_id="main_component") as demo:
    with gr.Tab("Climate-X"):
        with gr.Row(elem_id="chatbot-row"):
            with gr.Column(scale=2):
                # state = gr.State([system_template])
                chatbot = gr.Chatbot(
                    value=[(None, init_prompt)],
                    show_copy_button=True,
                    show_label=False,
                    elem_id="chatbot",
                    layout="panel",
                )

                with gr.Row(elem_id="input-message"):
                    textbox = gr.Textbox(
                        placeholder="Ask me anything here!",
                        show_label=False,
                        scale=7,
                        lines=1,
                        interactive=True,
                        elem_id="input-textbox",
                    )

            with gr.Column(scale=1):
                with gr.Tabs() as tabs:
                    with gr.TabItem("Examples", elem_id="tab-examples", id=0):

                        examples_hidden = gr.Textbox(visible=False)
                        first_key = list(QUESTIONS.keys())[0]
                        dropdown_samples = gr.Dropdown(
                            QUESTIONS.keys(),
                            value=first_key,
                            interactive=True,
                            show_label=True,
                            label="Select a category of sample questions",
                            elem_id="dropdown-samples",
                        )

                        samples = []
                        for i, key in enumerate(QUESTIONS.keys()):

                            examples_visible = True if i == 0 else False

                            with gr.Row(visible=examples_visible) as group_examples:

                                examples_questions = gr.Examples(
                                    QUESTIONS[key],
                                    [examples_hidden],
                                    examples_per_page=8,
                                    run_on_click=False,
                                    elem_id=f"examples{i}",
                                    api_name=f"examples{i}",
                                    # label = "Click on the example question or enter your own",
                                    # cache_examples=True,
                                )

                            samples.append(group_examples)

                    with gr.Tab("Sources", elem_id="tab-citations", id=1):
                        sources_textbox = gr.HTML(
                            show_label=False, elem_id="sources-textbox"
                        )
                        docs_textbox = gr.State("")

    def start_chat(query, history):
        history = history + [(query, None)]
        history = [tuple(x) for x in history]
        return (gr.update(interactive=False), gr.update(selected=1), history)

    def finish_chat():
        return gr.update(interactive=True, value="")

    (
        textbox.submit(
            start_chat,
            [textbox, chatbot],
            [textbox, tabs, chatbot],
            queue=False,
            api_name="start_chat_textbox",
        )
        .then(
            chat,
            [textbox, chatbot],
            [chatbot, sources_textbox],
            concurrency_limit=8,
            api_name="chat_textbox",
        )
        .then(finish_chat, None, [textbox], api_name="finish_chat_textbox")
    )

    (
        examples_hidden.change(
            start_chat,
            [examples_hidden, chatbot],
            [textbox, tabs, chatbot],
            queue=False,
            api_name="start_chat_examples",
        )
        .then(
            chat,
            [examples_hidden, chatbot],
            [chatbot, sources_textbox],
            concurrency_limit=8,
            api_name="chat_examples",
        )
        .then(finish_chat, None, [textbox], api_name="finish_chat_examples")
    )

    def change_sample_questions(key):
        index = list(QUESTIONS.keys()).index(key)
        visible_bools = [False] * len(samples)
        visible_bools[index] = True
        return [gr.update(visible=visible_bools[i]) for i in range(len(samples))]

    dropdown_samples.change(change_sample_questions, dropdown_samples, samples)

demo.queue()
demo.launch()
