from operator import itemgetter

from langchain.prompts import ChatPromptTemplate, PromptTemplate
from langchain_core.runnables import RunnablePassthrough, RunnableBranch
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts.base import format_document

from qa.engine.utils import pass_values, flatten_dict,prepare_chain,rename_chain
from qa.templates import  prompt_with_docs_template, prompt_without_docs_template

DEFAULT_DOCUMENT_PROMPT = PromptTemplate.from_template(template="{page_content}")

def _combine_documents(
    docs, document_prompt=DEFAULT_DOCUMENT_PROMPT, sep="\n\n"
):

    doc_strings =  []

    for i,doc in enumerate(docs):
        # chunk_type = "Doc" if doc.metadata["chunk_type"] == "text" else "Image"
        chunk_type = "Doc"
        if isinstance(doc,str):
            doc_formatted = doc
        else:
            doc_formatted = format_document(doc, document_prompt)
        doc_string = f"{chunk_type} {i+1}: " + doc_formatted
        doc_string = doc_string.replace("\n"," ") 
        doc_strings.append(doc_string)

    return sep.join(doc_strings)

def make_rag_chain(retriever, llm):
    prompt = PromptTemplate.from_template(template=prompt_with_docs_template)
    prompt_without_docs = PromptTemplate.from_template(
        template=prompt_without_docs_template
    )

    find_docs = {"docs": itemgetter("question") | retriever} | RunnablePassthrough()
    find_docs = prepare_chain(find_docs, "find_docs")

    input_docs = {
        "context": lambda x: _combine_documents(x["docs"]),
        **pass_values(["question"]),
    }

    llm_final = rename_chain(llm, "answer")

    answer_with_docs = {
        "answer": input_docs | prompt | llm_final | StrOutputParser(),
        **pass_values(["question", "docs"]),
    }

    answer_without_docs = {
        "answer": prompt_without_docs | llm_final | StrOutputParser(),
        **pass_values(["question", "docs"]),
    }

    def has_docs(x):
        return len(x["docs"]) > 0
        # return False

    answer = RunnableBranch(
        (lambda x: has_docs(x), answer_with_docs), answer_without_docs
    )

    chain = find_docs | answer

    return chain