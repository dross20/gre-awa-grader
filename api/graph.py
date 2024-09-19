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

# essay = """The debate over whether corporations should prioritize societal well-being or solely focus on maximizing profits is central to discussions about the role of business in modern society. I believe that corporations have a responsibility not only to pursue profits but also to contribute positively to the communities and environments in which they operate. This position is grounded in the growing influence of corporations on society, the long-term benefits of corporate social responsibility (CSR), and the ethical obligation businesses have as members of the global community. While profit maximization is a legitimate goal, it must be balanced with a commitment to sustainable and socially responsible practices. One of the strongest arguments for corporate social responsibility is the profound impact that corporations have on society and the environment. Large companies wield significant economic power, often rivaling that of governments. For example, companies like Amazon and Apple have global influence, shaping industries, labor practices, and consumer behavior. With this power comes a responsibility to address the broader consequences of their operations. When corporations neglect societal well-being in favor of short-term profits, the negative effects can be far-reaching, including environmental degradation, economic inequality, and exploitation of labor. Thus, it is imperative for corporations to recognize that their decisions can have lasting effects on society and the environment. Moreover, promoting the well-being of society and the environment is not only ethically sound but also strategically beneficial in the long run. A corporation’s reputation is increasingly tied to its social and environmental record, and consumers are more likely to support businesses that demonstrate a commitment to CSR. For example, companies like Patagonia and Ben & Jerry’s have built strong brand loyalty by aligning their business practices with sustainability and social justice causes. This consumer-driven demand for ethical practices highlights how CSR can contribute to a company’s long-term profitability. In contrast, corporations that engage in environmentally harmful practices or exploitative labor conditions often face backlash, regulatory penalties, and loss of consumer trust, ultimately jeopardizing their financial success. Critics of CSR argue that a corporation’s primary duty is to maximize profits within the confines of the law, contending that businesses exist to serve shareholders rather than society. However, this view is short-sighted. While businesses do have a responsibility to generate profits, this obligation need not be in conflict with social and environmental concerns. In fact, corporations that engage in CSR often find that ethical practices and profitability are mutually reinforcing. For instance, companies that invest in sustainable energy solutions may reduce operational costs in the long term while simultaneously contributing to environmental preservation. The dichotomy between profit and social responsibility is therefore a false one; businesses can and should pursue both. Opponents may also argue that imposing social responsibilities on businesses distracts from their primary purpose and introduces inefficiencies. However, this perspective underestimates the adaptability of corporations. Many companies have successfully integrated CSR into their core business strategies without sacrificing profitability. The key lies in aligning a company’s social and environmental initiatives with its economic goals. For example, Starbucks has committed to sourcing ethically produced coffee and reducing its carbon footprint, actions that enhance the company’s brand image while maintaining a profitable business model. In conclusion, while profit maximization is an essential goal for corporations, it should not come at the expense of societal well-being or environmental sustainability. Corporations are integral members of the global community and have a responsibility to contribute positively to the societies and environments they impact. By adopting socially responsible practices, companies can build trust with consumers, ensure long-term profitability, and fulfill their ethical obligations. Thus, the future of business lies not in a singular focus on profits but in a balanced approach that considers both financial success and the greater good."""

# inputs = {
#     "essay": essay
# }

# app = workflow.compile()

# for output in app.stream(inputs):
#     for key, value in output.items():
#         # Node
#         print(f"Node '{key}':")
#         # Optional: print full state at each node
#         # pprint.pprint(value["keys"], indent=2, width=80, depth=None)
#     print("\n---\n")

# # Final generation
# print(value["score"])
# print(value["rationale"])
# print(value["generations"])