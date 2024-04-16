from typing import List
from langchain_core.callbacks.manager import CallbackManagerForRetrieverRun
from langchain_core.documents import Document
from langchain_core.retrievers import BaseRetriever
from langchain_core.vectorstores import VectorStore


class ClimateXRetriever(BaseRetriever):
    vectorstore:VectorStore
    k:int = 5
    threshold:float = 0.5
    namespace:str = "vectors"

    def _get_relevant_documents(self, query: str, *, run_manager: CallbackManagerForRetrieverRun) -> List[Document]:
        docs = self.vectorstore.similarity_search_with_score(query=query, k=self.k)

        docs = [x for x in docs if x[1] > self.threshold]

        results = []
        for doc, score in docs:
            doc.metadata['score'] = score
            doc.metadata['page'] = int(doc.metadata['page'])+1
            doc.metadata['source'] = doc.metadata['source']+f"#page={doc.metadata['page']}"

            results.append(doc)

        return results