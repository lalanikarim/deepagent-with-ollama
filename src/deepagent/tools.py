"""Custom tools for the deep agent."""

from typing import Optional
from langchain_core.tools import tool
from ddgs import DDGS
import json


@tool
def web_search(
    query: str,
    max_results: int = 5,
    region: str = "us-en",
    safesearch: str = "moderate",
    time: str = None,
) -> str:
    """
    Search the web using DuckDuckGo.
    
    Args:
        query: The search query
        max_results: Maximum number of results to return (default: 5)
        region: Region for search results (default: us-en)
        safesearch: Safe search level - off, moderate, strict (default: moderate)
        time: Time filter - d (day), w (week), m (month), y (year) (optional)
    
    Returns:
        JSON string containing search results
    """
    try:
        with DDGS() as ddgs:
            # Perform the search
            results = list(ddgs.text(
                query,
                max_results=max_results,
                region=region,
                safesearch=safesearch
            ))
            
            # Format results for better readability
            formatted_results = []
            for result in results:
                formatted_result = {
                    "title": result.get("title", ""),
                    "body": result.get("body", ""),
                    "href": result.get("href", ""),
                    "hostname": result.get("hostname", ""),
                }
                formatted_results.append(formatted_result)
            
            return json.dumps(formatted_results, indent=2)
            
    except Exception as e:
        return f"Error performing web search: {str(e)}"


@tool
def get_current_time() -> str:
    """Get the current date and time."""
    from datetime import datetime
    
    now = datetime.now()
    return f"Current time: {now.strftime('%Y-%m-%d %H:%M:%S')}"


@tool
def calculate(expression: str) -> str:
    """
    Safely evaluate a mathematical expression.
    
    Args:
        expression: Mathematical expression to evaluate (e.g., "2 + 2", "10 * 5")
    
    Returns:
        Result of the calculation
    """
    try:
        # Only allow safe mathematical operations
        allowed_chars = set("0123456789+-*/()., ")
        if not all(c in allowed_chars for c in expression):
            return "Error: Only basic mathematical operations are allowed"
        
        result = eval(expression)
        return f"Result: {result}"
    except Exception as e:
        return f"Error calculating expression: {str(e)}"
