#!/usr/bin/env python3
"""
This script discovers and crawls all pages in a website's sitemap(s)
using the Jina AI Reader API and aggregates the content into a single file.
"""

import os
import sys
import asyncio
from pathlib import Path
from urllib.parse import urljoin
import httpx
from bs4 import BeautifulSoup

# Optional Firecrawl import
try:
    from firecrawl import AsyncFirecrawlApp

    FIRECRAWL_AVAILABLE = True
except ImportError:
    FIRECRAWL_AVAILABLE = False
    AsyncFirecrawlApp = None  # type: ignore[misc]

# --- Configuration ---
JINA_API_URL = "https://r.jina.ai/"
SITEMAP_PATHS = ["/sitemap.xml", "/sitemap_index.xml"]

# --- Helper Functions ---


async def fetch_url(client, url):
    """Fetches content from a URL.
    Returns the response object or None on failure.
    """
    try:
        response = await client.get(url, follow_redirects=True)
        response.raise_for_status()
        return response
    except httpx.RequestError as e:
        print(f"- Skipping {url}: Request failed: {e}")
        return None


async def fetch_page_content_from_jina(client, page_url, headers):
    """Fetches markdown content for a single page URL from Jina API.
    Returns a tuple of (url, content) or None.
    """
    try:
        response = await client.get(f"{JINA_API_URL}{page_url}", headers=headers)
        response.raise_for_status()
        data = response.json().get("data")
        if data and data.get("content"):
            return (data.get("url"), data.get("content"))
    except httpx.HTTPStatusError as e:
        print(
            f"- Skipping {page_url}: Jina API failed with status {e.response.status_code}"
        )
    except Exception as e:
        print(f"- Skipping {page_url}: An unexpected error occurred: {e}")


async def fetch_page_content_from_firecrawl(firecrawl_app, page_url):
    """Fetches markdown content for a single page URL from Firecrawl API.
    Returns a tuple of (url, content) or None.
    """
    try:
        result = await firecrawl_app.scrape_url(page_url, formats=["markdown"])
        if result and result.get("markdown"):
            return (page_url, result.get("markdown"))
    except Exception as e:
        print(f"- Skipping {page_url}: Firecrawl API failed: {e}")
    return None


async def find_sitemap_urls(client, domain):
    """Discovers sitemap URLs from robots.txt or common paths.
    Returns a list of sitemap URLs.
    """
    # 1. Check robots.txt
    robots_url = urljoin(domain, "/robots.txt")
    response = await fetch_url(client, robots_url)
    if response:
        for line in response.text.splitlines():
            if line.lower().startswith("sitemap:"):
                return [line.split(":", 1)[1].strip()]

    # 2. Check common paths
    for path in SITEMAP_PATHS:
        sitemap_url = urljoin(domain, path)
        response = await fetch_url(client, sitemap_url)
        if response:
            return [sitemap_url]

    return []


async def parse_sitemap(client, sitemap_url):
    """Parses a sitemap (or sitemap index) and returns a list of page URLs.
    Recursively handles nested sitemaps.
    """
    page_urls = set()
    response = await fetch_url(client, sitemap_url)
    if not response:
        return list(page_urls)

    soup = BeautifulSoup(response.content, "xml")

    # Check for sitemap index
    sitemap_tags = soup.find_all("sitemap")
    if sitemap_tags:
        nested_sitemap_urls = [tag.find("loc").text for tag in sitemap_tags]
        tasks = [parse_sitemap(client, url) for url in nested_sitemap_urls]
        results = await asyncio.gather(*tasks)
        for result in results:
            page_urls.update(result)
    else:
        # Regular sitemap
        url_tags = soup.find_all("url")
        for tag in url_tags:
            loc = tag.find("loc")
            if loc:
                page_urls.add(loc.text)

    return list(page_urls)


# --- Main Execution ---


async def main():
    """Main function to orchestrate the crawling process."""
    domain = os.environ.get("INPUT_DOMAIN")
    output_file = os.environ.get("INPUT_OUTPUTFILE", "public/llms.txt")
    backend = os.environ.get("INPUT_BACKEND", "jina").lower()
    jina_api_key = os.environ.get("INPUT_JINA_API_KEY")
    firecrawl_api_key = os.environ.get("INPUT_FIRECRAWL_API_KEY")

    if domain is None:
        print("Error: INPUT_DOMAIN is not set.", file=sys.stderr)
        return

    # Validate backend selection
    if backend not in ["jina", "firecrawl"]:
        print(
            f"Error: Invalid backend '{backend}'. Must be 'jina' or 'firecrawl'.",
            file=sys.stderr,
        )
        return

    if backend == "firecrawl":
        if not FIRECRAWL_AVAILABLE:
            print(
                "Error: Firecrawl backend selected but firecrawl-py is not installed.",
                file=sys.stderr,
            )
            return
        if not firecrawl_api_key:
            print(
                "Error: Firecrawl backend selected but INPUT_FIRECRAWL_API_KEY is not set.",
                file=sys.stderr,
            )
            return

    # Ensure domain has a scheme
    if not domain.startswith(("http://", "https://")):
        domain = f"https://{domain}"

    headers = {"Accept": "application/json"}
    if jina_api_key and backend == "jina":
        headers["Authorization"] = f"Bearer {jina_api_key}"

    async with httpx.AsyncClient(timeout=60.0) as client:
        print(f"🔍 Discovering sitemaps for {domain}...")
        sitemap_urls = await find_sitemap_urls(client, domain)
        if not sitemap_urls:
            print("❌ No sitemap found. Cannot proceed.", file=sys.stderr)
            return

        print(f"🗺️ Found sitemap(s): {', '.join(sitemap_urls)}")

        all_page_urls = []
        for url in sitemap_urls:
            all_page_urls.extend(await parse_sitemap(client, url))

        if not all_page_urls:
            print("No URLs found in sitemap(s).", file=sys.stderr)
            return

        print(
            f"Found {len(all_page_urls)} URLs. Fetching content from {backend.title()}..."
        )

        if backend == "jina":
            tasks = [
                fetch_page_content_from_jina(client, url, headers)
                for url in all_page_urls
            ]
            results = await asyncio.gather(*tasks)
        else:  # firecrawl
            firecrawl_app = AsyncFirecrawlApp(api_key=firecrawl_api_key)
            tasks = [
                fetch_page_content_from_firecrawl(firecrawl_app, url)
                for url in all_page_urls
            ]
            results = await asyncio.gather(*tasks)

        successful_pages = [res for res in results if res is not None]

    if not successful_pages:
        print("No content could be fetched for any URL.", file=sys.stderr)
        return

    # Aggregate and write content
    all_content = [f"# Source: {url}\n\n{content}" for url, content in successful_pages]
    output_path = Path(output_file)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    with open(output_path, "w", encoding="utf-8") as f:
        f.write("\n\n---\n\n".join(all_content))

    print(f"✅ Wrote content from {len(successful_pages)} pages to {output_file}")


if __name__ == "__main__":
    asyncio.run(main())
