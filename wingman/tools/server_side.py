from langchain_community.tools.tavily_search import TavilySearchResults

from dotenv import load_dotenv

load_dotenv()

search = TavilySearchResults(max_results=2)
tools = [search]
tool_names = {tool.name:tool for tool in tools}