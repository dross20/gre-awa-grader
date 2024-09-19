from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.document_loaders import WebBaseLoader
from langchain_community.vectorstores import Chroma
from langchain_openai import AzureOpenAIEmbeddings
import os

class RetrieverFactory():
    def __init__(self) -> None:
        self.retriever = self.create_retriever()

    def create_retriever(self):
        embed = AzureOpenAIEmbeddings(
            deployment="test-embed"
        )

        urls = [
            'https://www.ets.org/gre/score-users/scores/descriptions-guides.html',
            'https://magoosh.com/gre/awa-issue-essay-strategies/',
            'https://www.kaptest.com/study/gre/how-to-structure-the-gre-issue-essay/?srsltid=AfmBOopNPnO5aQ4JzAOjoHfSJIfrbIAU6qYLNNPbWpQxk2Mtf2jYmqPN',
            'https://www.ets.org/gre/test-takers/general-test/prepare/content/analytical-writing.html'
        ]

        docs = [WebBaseLoader(url).load() for url in urls]
        docs_list = [item for sublist in docs for item in sublist]

        text_splitter = RecursiveCharacterTextSplitter.from_tiktoken_encoder(
            chunk_size = 250, chunk_overlap = 0
        )

        doc_splits = text_splitter.split_documents(docs_list)

        vectorstore = Chroma.from_documents(
            documents = doc_splits,
            collection_name = "rag-chroma",
            embedding = embed,
        )

        return vectorstore.as_retriever()

    def get_retriever(self):
        return self.retriever
    
os.environ["OPENAI_API_VERSION"] = "2023-03-15-preview"
os.environ["AZURE_OPENAI_ENDPOINT"] = "https://langchain-test-3.openai.azure.com/"
os.environ["AZURE_OPENAI_API_KEY"] = "330d8510da75488fac135dad59c736af"
os.environ["AZURE_OPENAI_DEPLOYMENT"] = "test-gpt-deployment"


retriever = RetrieverFactory().get_retriever()