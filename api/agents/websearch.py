from langchain_community.tools.tavily_search import TavilySearchResults

def get_web_search():
    return TavilySearchResults(k=3)