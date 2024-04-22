from langchain_community.vectorstores.chroma import Chroma

def get_vectorstore(embeddings, dir='chroma_db'):
    vectorstore = Chroma(embedding_function=embeddings, persist_directory=dir)

    return vectorstore