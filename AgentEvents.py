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
                message = f"Planner: Generated {len(queries)} search strategies.\nQueries: {','.join(query_list)}"
                yield f"data:{json.dumps({'type': 'log','message': message}) }\n\n"
            elif node_name == "gather_results":
                results = state_update.get("search_results", [])
                message = f"Searching web ... \n found {len(results)} raw web pages."
                yield f"data:{json.dumps({'type':'log', 'message':message})}"
            elif node_name == "deduplicate":
                count = len(state_update.get("refined_search_results", []))
                message = f"Refining Search Results...\n Removing duplicates. {count} unique search results remain."
                yield f"data:{json.dumps({'type':'log', 'message': message})}\n\n"
            elif node_name == "SearchResultsEvaluation":
                good_urls = state_update.get("selected_urls", [])
                bad_urls = state_update.get("discarded_urls", [])
                message = f"Analyzing search results...\n found {len(good_urls)} relevant sources. \n Rejected {len(bad_urls)} irrelevant ones."
                yield f"data:{json.dumps({'type':'log', 'message':message})}\n\n"
            elif node_name == "ScrapeDispatch":
                mesage = "Launching parallel scrappers..."
                yield f"data:{json.dumps({'type':'log', 'message': message})}\n\n"
            elif node_name == "ScrapeNode":
                new_content = state_update.get("ScrapeNode",[])
                if new_content:
                    url = new_content[0]["url"]
                    message = f"Successfully scraped content from {url}"
                    yield f"data:{json.dumps({'type':'log', 'message': mesage})}\n\n"
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

        
