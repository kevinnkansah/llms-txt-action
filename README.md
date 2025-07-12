# LLMs.txt Generator Action

[![Semantic Release](https://img.shields.io/badge/%20%20%F0%9F%93%A6%F0%9F%9A%80-semantic--release-e10079.svg)](https://github.com/semantic-release/semantic-release)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

This GitHub Action automatically crawls a website using its sitemap and generates a single `llms.txt` file containing the clean, markdown-formatted content from every page. It's designed to create a corpus for Large Language Models (LLMs) or for search indexing.

The action leverages the powerful [Jina AI Reader API](https://r.jina.ai/) to handle the heavy lifting of content extraction.

## Features

- **Sitemap-Driven Crawling**: Intelligently discovers and parses your `sitemap.xml` to find every page.
- **Clean Markdown Output**: Uses the Jina AI Reader API to extract high-quality content in markdown format.
- **Asynchronous & Fast**: Built with Python, `httpx`, and `uv` for efficient, non-blocking execution.
- **Easy to Integrate**: Drop it into any workflow to keep your `llms.txt` file up-to-date.

## Usage

Create a workflow file (e.g., `.github/workflows/update-llms.yml`) in your repository and add the following content. This example workflow runs on every push to the `main` branch, generates the `llms.txt` file, and commits it back to the repository.

```yaml
name: Update LLMs.txt
on:
  push:
    branches: [ main ]
jobs:
  build-llms:
    runs-on: ubuntu-latest
    steps:
      - name: Checkout repository
        uses: actions/checkout@v4

      - name: Generate llms.txt
        uses: kevinnkansah/llms-txt-action@v1
        with:
          domain: https://your-website.com
          outputFile: public/llms.txt
          jina_api_key: ${{ secrets.JINA_API_KEY }} # Optional, but recommended

      - name: Commit and push llms.txt
        uses: EndBug/add-and-commit@v9
        with:
          add: 'public/llms.txt'
          message: 'chore: update llms.txt'
```

## Inputs

| Name           | Required | Description                                                                                                | Default              |
|----------------|----------|------------------------------------------------------------------------------------------------------------|----------------------|
| `domain`       | **Yes**  | The full URL of the site to crawl (e.g., `https://example.com`).                                            |                      |
| `outputFile`   | No       | The path where the final `llms.txt` file will be saved.                                                    | `public/llms.txt`    |
| `jina_api_key` | No       | Your Jina AI Reader API key. Recommended for higher rate limits. Store this as a [GitHub Secret](https://docs.github.com/en/actions/security-guides/using-secrets-in-github-actions). |                      |

## How It Works

This action first attempts to find your sitemap by checking `/robots.txt` and common paths like `/sitemap.xml`. It then parses the sitemap(s) to get a list of all page URLs. For each URL, it calls the Jina AI Reader API (`https://r.jina.ai/`) to fetch the content as clean markdown. Finally, it aggregates the content from all pages into the specified `outputFile`.

## Development

This project uses `uv` for package management and `pre-commit` with `commitizen` to enforce conventional commit messages.

1.  **Clone the repository**
2.  **Install dependencies**:
    ```bash
    uv pip install -e .[dev]
    ```
3.  **Activate pre-commit hooks**:
    ```bash
    uv run pre-commit install --hook-type commit-msg
    ```
4.  **Make your changes**
5.  **Commit your work** using the guided prompt:
    ```bash
    uv run cz commit
    ```

Your contributions will be automatically versioned and released upon merging to `main`.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.
