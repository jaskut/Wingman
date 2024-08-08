from langchain_community.tools.tavily_search import TavilySearchResults

search = TavilySearchResults(max_results=2)
tools = [search]
tool_names = {tool.name:tool for tool in tools}