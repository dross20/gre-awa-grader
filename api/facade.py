from agents import docgrader, formatter, grader, rag, websearch
from retriever import RetrieverFactory
from langchain.schema import Document

class AgentFacade():
    def __init__(self, llm):
        self.grader = self.get_grader(llm)
        self.formatter = self.get_formatter(llm)
        self.doc_grader = self.get_doc_grader(llm)
        self.rag_chain = self.get_rag(llm)
        self.retriever = self.get_retriever()
        self.web_retriever = self.get_web_retriever()

    def grade_essay(self, essay, prompt):
        return self.grader.invoke({"essay": essay, "prompt": prompt})
    
    def format_essay(self, essay):
        return self.formatter.invoke({"essay": essay})

    def grade_doc(self, doc, improvement):
        return self.doc_grader.invoke({"document": doc, "question": improvement})
    
    def rag(self, essay, suggestions, docs):
        return self.rag_chain.invoke({"essay": essay, "suggestions": suggestions, "context": docs})

    def retrieve(self, query):
        return self.retriever.invoke(query)
    
    def web_search(self, query):
        docs = self.web_retriever.invoke({"query": query})
        try:
            results = "\n".join([d["content"] for d in docs])
            return Document(page_content=results)
        finally:
            return docs

    def get_doc_grader(self, llm):
        return docgrader.get_document_grader(llm=llm)

    def get_formatter(self, llm):
        return formatter.get_formatter(llm=llm)

    def get_grader(self, llm):
        return grader.get_grader(llm=llm)
    
    def get_rag(self, llm):
        return rag.get_rag(llm=llm)
    
    def get_retriever(self):
        fac = RetrieverFactory()
        return fac.get_retriever()
    
    def get_web_retriever(self):
        return websearch.get_web_search()