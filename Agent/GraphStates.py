from typing import TypedDict, List, Annotated
import operator

class SearchQuery(TypedDict):
    query : str
    id : str

class SearchResult(TypedDict):
    id: str
    url : str
    title : str
    page_age : str
    description : str
    search_query : SearchQuery

class ScrapedContent(TypedDict):
    url : str
    content : str
    source : SearchResult
    image_url: str

class AgentState(TypedDict):
    # 1. Input user query
    topic : str

    # 2. Planner node, list of search quries design by Gemini
    search_queries: List[SearchQuery]

    # 3. Search results from Brave API
    search_results: Annotated[List[SearchResult], operator.add]

    # 3.1 This will have non duplicate and evaluated urls by gemini
    refined_search_results: List[SearchResult]

    # 3.2 Selected urls from evaluation
    selected_urls: List[SearchResult]

    # 3.3 Discarded urls from evaluation
    discarded_urls: List[str]

    # 4. Scraped contents of the search results
    scraped_contents: Annotated[List[ScrapedContent], operator.add]

    # 5. CRITIC NODE: Facts that have been cross-referenced
    verified_claims: List[str]
    
    # 6. REPORTER NODE: The final markdown output
    final_report: str
    
    # SYSTEM: Tracks how many times we've looped (to prevent infinite loops)
    loop_step: int
