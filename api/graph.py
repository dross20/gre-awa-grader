from llm import get_llm
from models import GraphState
from facade import AgentFacade
from langgraph.graph import START, END, StateGraph

llm=get_llm()
agents = AgentFacade(llm)

def format(state):
    essay = state["essay"]

    formatted_essay = agents.format_essay(
        essay=essay
    )

    prompt = formatted_essay.prompt
    body = formatted_essay.body

    state["prompt"] = prompt
    state["body"] = body

    return state

def grade(state):
    body = state["body"]
    prompt = state["prompt"]

    grade = agents.grade_essay(
        essay=body,
        prompt=prompt
    )

    score = grade.score
    rationale = grade.rationale
    improvement = grade.improvement

    state["score"] = score
    state["rationale"] = rationale
    state["improvement"] = improvement

    return state

def retrieve(state):
    query = state["improvement"]

    docs = agents.retrieve(
        query=query
    )

    state["documents"] = docs

    return state

def grade_docs(state):
    docs = state["documents"]

    filtered_docs = []

    for doc in docs:
        grade = agents.grade_doc(docs, state["improvement"])
        score = grade.binary_score

        if score == "yes":
            filtered_docs.append(doc)

    state["documents"] = filtered_docs

    return state

def web_search(state):
    query = state["improvement"]

    docs = agents.web_search(
        query=query
    )

    state["documents"] = docs

    return state

def rag(state):
    body = state["body"]
    improvement = state["improvement"]
    docs = state["documents"]

    generation = agents.rag(
        essay=body,
        suggestions=improvement,
        docs=docs
    )

    state["generations"] = generation

    return state

def decide_to_generate(state):
    filtered_documents = state["documents"]

    if not filtered_documents:
        return "web_search"
    else:
        return "generate"

workflow = StateGraph(GraphState)

workflow.add_node("format", format)
workflow.add_node("grade", grade)
workflow.add_node("retrieve", retrieve)
workflow.add_node("grade_docs", grade_docs)
workflow.add_node("web_search", web_search)
workflow.add_node("generate", rag)

workflow.add_edge(START, "format")
workflow.add_edge("format", "grade")
workflow.add_edge("grade", "retrieve")
workflow.add_edge("retrieve", "grade_docs")

workflow.add_conditional_edges(
    "grade_docs",
    decide_to_generate,
    {
        "web_search": "web_search",
        "generate": "generate"
    }
)

workflow.add_edge("web_search", "generate")
workflow.add_edge("generate", END)

def get_app():
    return workflow.compile()