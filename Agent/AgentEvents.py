import json
from Graph import graph as agent_app


async def news_event_stream_generator(topic: str):
    inputs = {
        "topic": topic
    }
    
    async for event in agent_app.astream(inputs):

        for node_name, state_update in event.items():
            if node_name == "planner":
                queries = state_update.get("search_queries",[])
                query_list = [q["query"] for q in queries]

                data = {
                    "type": "log", 
                    "step": "planner", 
                    "message": f"Generated {len(query_list)} search queries",
                    "details": query_list # <--- SEND THE LIST
                }
                yield f"data: {json.dumps(data)}\n\n"
                
            elif node_name == "SearchNode":
                results = state_update.get("search_results", [])
                message = f"Searching web ... \n found {len(results) if len(results) > 0 else 0} raw web pages."
                yield f"data:{json.dumps({'type':'log', 'message':message})}\n\n"
            elif node_name == "deduplicate":
                unique_results = state_update.get("refined_search_results", [])
                # Send the list of found sources (Title + URL)
                source_list = [{"title": r["title"], "url": r["url"]} for r in unique_results]
                
                data = {
                    "type": "log", 
                    "step": "sources", 
                    "message": f"Found {len(source_list)} potential sources",
                    "details": source_list # <--- SEND THE SOURCES
                }
                yield f"data: {json.dumps(data)}\n\n"

            elif node_name == "SearchResultsEvaluation":
                good_urls = state_update.get("selected_urls", [])
                bad_urls = state_update.get("discarded_urls", [])
                message = f"Analyzing search results...\n found {len(good_urls) if len(good_urls) > 0 else 0} relevant sources. \n Rejected {len(bad_urls) if len(bad_urls) > 0 else 0} irrelevant ones."
                yield f"data:{json.dumps({'type':'log', 'message':message})}\n\n"
            elif node_name == "ScrapeDispatch":
                message = "Launching parallel scrappers..."
                yield f"data:{json.dumps({'type':'log', 'message': message})}\n\n"
            elif node_name == "ScrapeNode":
                new_content = state_update.get("scraped_contents",[])
                if new_content:
                    url = new_content[0]["url"]
                    data = {
                        "type": "log",
                        "step": "scraping",
                        "message": f"Reading: {url}",
                        "details": url
                    }
                    yield f"data: {json.dumps(data)}\n\n"
            elif node_name == "ReporterNode":
                final_report = state_update.get("final_report", "")
                all_scraped_data = state_update.get("scraped_contents", [])

                clean_sources = []
                for item in all_scraped_data:
                    clean_sources.append({
                        "title": item["source"].get("title", "Unknown Source"),
                        "url": item["url"],
                        "image": item.get("image_url", "")
                    })

                payload = {
                    "type": "result",
                    "markdown": final_report,
                    "sources": clean_sources
                }

                yield f"data:{json.dumps(payload)}\n\n"

        
