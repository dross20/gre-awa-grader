from langchain_core.prompts import ChatPromptTemplate
from models import Essay
from langchain_core.output_parsers import JsonOutputParser

def get_formatter(llm):
    structured_llm_formatter = llm.with_structured_output(Essay)

    system="""You are an agent that separates a student's prompt and essay submission.\n
        If the human explicitly states the prompt, identify and separate it from the essay.\n
        If no prompt is provided, make a reasonable guess as to what the prompt might be based on the essay's content.
        """

    essay_prompt = ChatPromptTemplate.from_messages(
        [
            ("system", system),
            ("human", "Essay: {essay}")
        ]
    )

    essay_formatter = essay_prompt | structured_llm_formatter

    return essay_formatter