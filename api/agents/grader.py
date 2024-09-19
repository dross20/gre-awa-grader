from langchain_core.prompts import ChatPromptTemplate
from models import EssayGrade

def get_grader(llm):
    structured_llm_grader = llm.with_structured_output(EssayGrade)

    system = """You are tasked with grading a GRE Analytical Writing essay on a scale from 0 to 6, in 0.5 increments, using the official ETS rubric.\n
    Assess the essay based on how well it addresses the prompt, the clarity and organization of the argument, the development of ideas with relevant support, and the use of language, including grammar and sentence structure.\n
    Ensure that the essay responds directly to the prompt and that the argument is logically sound and coherent.\n
    Provide a score along with a brief rationale, highlighting strengths and weaknesses based on these criteria.\n"""

    grade_prompt = ChatPromptTemplate.from_messages(
        [
            ("system", system),
            ("human", "Essay prompt: {prompt} \n\n User essay: {essay}")
        ]
    )

    essay_grader = grade_prompt | structured_llm_grader

    return essay_grader