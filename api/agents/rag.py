from langchain import hub
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser

def get_rag(llm):
    system = """You are tasked with providing improvement suggestions for a GRE Analytical Writing essay using relevant documents retrieved from a vector database as context.\n
            The essay has already been graded, and initial suggestions for improvement have been made.\n
            Review the retrieved documents to enhance the essay's argumentation, clarity, or development of ideas.\n
            Based on the context provided by these documents, suggest specific improvements that the student can implement, citing examples or evidence from the documents to support your suggestions.\n
            Don't specifically mention 'context', 'retrieved documents', or 'initial suggestions'."""

    prompt = ChatPromptTemplate.from_messages(
        [
            ("system", system),
            ("human", "Essay: {essay} \n\n Suggestions: {suggestions} \n\n Context: {context}")
        ]
    )

    rag_chain = prompt | llm | StrOutputParser()

    return rag_chain