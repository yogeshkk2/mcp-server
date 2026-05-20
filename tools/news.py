"""News fetching tool for the MCP server."""

import requests
import os
from typing import Optional

NEWSAPI_KEY = os.getenv("NEWSAPI_KEY", "2c8b34b19ace4152bb605d364d1d3426")

def get_latest_news(
    query: str = "technology",
    country: str = "us",
    language: str = "en",
    max_results: int = 5
) -> str:
    """
    Fetch the latest news articles from NewsAPI.

    Args:
        query (str): Search query/topic for news (e.g., "technology", "sports", "business")
        country (str): ISO 2-letter country code (e.g., "us", "uk", "in"). Only used with top-headlines endpoint.
        language (str): ISO 639-1 language code (e.g., "en", "es", "fr")
        max_results (int): Maximum number of articles to return (1-100, default: 5)

    Returns:
        str: Formatted string containing latest news articles with titles and descriptions,
             or an error message if the API call fails.

    Examples:
        >>> get_latest_news("python programming")
        'Article 1: Python 3.12 Released\\nDescription: The latest version...\\n\\nArticle 2: ...'
    """
    try:
        # Use NewsAPI.org free tier endpoint
        api_key = NEWSAPI_KEY
        max_results = min(max(1, max_results), 100)  # Clamp between 1-100

        # Using NewsAPI everything endpoint
        url = "https://newsapi.org/v2/everything"
        params = {
            "q": query,
            "language": language,
            "sortBy": "publishedAt",
            "pageSize": max_results,
            "apiKey": api_key
        }

        response = requests.get(url, params=params, timeout=10)
        response.raise_for_status()
        data = response.json()

        if data.get("status") != "ok":
            error_msg = data.get("message", "Unknown error from NewsAPI")
            return f"Error fetching news: {error_msg}"

        articles = data.get("articles", [])
        if not articles:
            return f"No news articles found for query: '{query}'"

        # Format the results
        result = f"Latest News for '{query}' ({len(articles)} articles):\n"
        result += "=" * 70 + "\n\n"

        for i, article in enumerate(articles, 1):
            title = article.get("title", "No title")
            description = article.get("description", "No description available")
            source = article.get("source", {}).get("name", "Unknown source")
            published_at = article.get("publishedAt", "Unknown date")
            url_link = article.get("url", "No URL")

            result += f"Article {i}: {title}\n"
            result += f"Source: {source}\n"
            result += f"Published: {published_at}\n"
            result += f"Description: {description}\n"
            result += f"URL: {url_link}\n"
            result += "-" * 70 + "\n"

        return result

    except requests.exceptions.Timeout:
        return "Error: Request to NewsAPI timed out. Please try again later."
    except requests.exceptions.ConnectionError:
        return "Error: Unable to connect to NewsAPI. Please check your internet connection."
    except requests.exceptions.HTTPError as e:
        return f"Error: HTTP error occurred: {e.response.status_code} - {e.response.text}"
    except Exception as e:
        return f"Error fetching news: {str(e)}"


def get_top_headlines(
    country: str = "us",
    category: Optional[str] = None,
    max_results: int = 5
) -> str:
    """
    Fetch top headlines for a specific country.

    Args:
        country (str): ISO 2-letter country code (e.g., "us", "uk", "in", "fr", "de")
        category (str, optional): News category - business, entertainment, general, health,
                                 science, sports, technology. If None, returns general headlines.
        max_results (int): Maximum number of articles to return (1-100, default: 5)

    Returns:
        str: Formatted string containing top headline articles,
             or an error message if the API call fails.

    Examples:
        >>> get_top_headlines("us", "technology")
        'Top Headlines for US - Technology:\\n\\nArticle 1: ...'
    """
    try:
        api_key = NEWSAPI_KEY
        max_results = min(max(1, max_results), 100)

        # Using NewsAPI top-headlines endpoint
        url = "https://newsapi.org/v2/top-headlines"
        params = {
            "country": country.lower(),
            "pageSize": max_results,
            "apiKey": api_key
        }

        if category:
            params["category"] = category.lower()

        response = requests.get(url, params=params, timeout=10)
        response.raise_for_status()
        data = response.json()

        if data.get("status") != "ok":
            error_msg = data.get("message", "Unknown error from NewsAPI")
            return f"Error fetching headlines: {error_msg}"

        articles = data.get("articles", [])
        if not articles:
            country_name = country.upper()
            category_name = f" - {category.title()}" if category else ""
            return f"No headlines found for {country_name}{category_name}"

        # Format the results
        country_name = country.upper()
        category_name = f" - {category.title()}" if category else ""
        result = f"Top Headlines for {country_name}{category_name} ({len(articles)} articles):\n"
        result += "=" * 70 + "\n\n"

        for i, article in enumerate(articles, 1):
            title = article.get("title", "No title")
            description = article.get("description", "No description available")
            source = article.get("source", {}).get("name", "Unknown source")
            published_at = article.get("publishedAt", "Unknown date")
            url_link = article.get("url", "No URL")

            result += f"Headline {i}: {title}\n"
            result += f"Source: {source}\n"
            result += f"Published: {published_at}\n"
            result += f"Description: {description}\n"
            result += f"URL: {url_link}\n"
            result += "-" * 70 + "\n"

        return result

    except requests.exceptions.Timeout:
        return "Error: Request to NewsAPI timed out. Please try again later."
    except requests.exceptions.ConnectionError:
        return "Error: Unable to connect to NewsAPI. Please check your internet connection."
    except requests.exceptions.HTTPError as e:
        return f"Error: HTTP error occurred: {e.response.status_code} - {e.response.text}"
    except Exception as e:
        return f"Error fetching headlines: {str(e)}"
