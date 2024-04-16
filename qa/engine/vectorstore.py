from langchain_community.vectorstores.chroma import Chroma

def get_vectorstore(embeddings):
    vectorstore = Chroma(embedding_function=embeddings, persist_directory='chroma_db')

    return vectorstore