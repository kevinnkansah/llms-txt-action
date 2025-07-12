# Build LLMs.txt GitHub Action

This GitHub Action uses the [Jina AI Reader API](https://r.jina.ai/) to crawl a website and compile all page content into a single `llms.txt` file, formatted as clean markdown.

## Features

- **Powered by Jina AI**: Leverages a powerful, specialized crawling service.
- **Markdown Output**: Fetches content in a clean, structured markdown format.
- **Simple & Fast**: Asynchronous Python script using `httpx` and `uv` for speed.
- **Sitemap-driven**: Intelligently uses the site's sitemap for comprehensive crawling.

## Usage

1.  **Publish this action**: Make this repository public (e.g., `github.com/you/build-llms-action`).
2.  **(Optional) Get a Jina API Key**: For higher rate limits, get a free API key from the [Jina AI Cloud](https://cloud.jina.ai/).
3.  **Set up the workflow**: In your target repository, create a workflow file (e.g., `.github/workflows/llms.yml`) and add the following:

```yaml
name: Rebuild LLMs
on:
  push:
    branches: [ main ]
jobs:
  build-llms:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4

      - name: Run LLMs crawler
        uses: you/build-llms-action@v1 # Replace with your action's repo
        with:
          domain: https://r.jina.ai
          outputFile: public/llms.txt
          jina_api_key: ${{ secrets.JINA_API_KEY }} # Optional, but recommended

      - name: Commit & Push llms.txt
        uses: EndBug/add-and-commit@v9
        with:
          author_name: github-actions
          author_email: actions@github.com
          message: "chore: regenerate llms.txt"
          add: public/llms.txt
          push: true
```

## Inputs

-   `domain` (**required**): The full URL of the site to crawl (e.g., `https://example.com`).
-   `outputFile`: The path where the final `llms.txt` file will be saved. (Default: `public/llms.txt`).
-   `jina_api_key` (**optional**): Your Jina AI Reader API key. It's recommended to store this as a [GitHub Secret](https://docs.github.com/en/actions/security-guides/using-secrets-in-github-actions).

## How It Works

On each push, the action sends a request to the Jina AI Reader API to crawl the specified `domain`. Jina's service follows the sitemap, extracts the main content from each page as markdown, and returns it. The action then aggregates all the markdown content into the `outputFile`.
