# 🤖 LLMs.txt Generator Action - AI-Optimized Website Crawling

[![Latest Release](https://img.shields.io/github/v/release/kevinnkansah/llms-txt-action?style=for-the-badge&logo=github&color=blue)](https://github.com/kevinnkansah/llms-txt-action/releases)
[![Semantic Release](https://img.shields.io/badge/%20%20%F0%9F%93%A6%F0%9F%9A%80-semantic--release-e10079.svg?style=for-the-badge)](https://github.com/semantic-release/semantic-release)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg?style=for-the-badge)](https://opensource.org/licenses/MIT)
[![GitHub Stars](https://img.shields.io/github/stars/kevinnkansah/llms-txt-action?style=for-the-badge&logo=github)](https://github.com/kevinnkansah/llms-txt-action/stargazers)

A GitHub Action that automatically crawls websites using their sitemap and generates a single `llms.txt` file containing clean, markdown-formatted content from every page. Designed to create AI-friendly content for Large Language Models (LLMs) following the proposed llms.txt standard.

## What is llms.txt?

**llms.txt** is a proposed web standard by [Jeremy Howard](https://github.com/jph00) (Answer.AI) that provides AI-friendly website content in a structured format. It helps Large Language Models understand and extract your website's most important information efficiently.

### Why llms.txt Matters

- **AI Search Optimization**: Optimizes your content for AI-powered search engines like Perplexity, ChatGPT, and Claude
- **Better Attribution**: Ensures proper citation when AI models reference your content
- **Context Window Friendly**: Overcomes LLM token limitations with curated, essential content
- **Controlled AI Interaction**: You decide what content AI models should prioritize
- **Future-Proof**: Positions your website for the AI-driven web

### Companies Using llms.txt

- **Perplexity** - AI search engine  
- **ElevenLabs** - AI voice technology  
- **FastHTML** - Web framework documentation  
- **Answer.AI** - AI research company  
- **Mintlify** - Documentation platform

## Features

### Dual Content Extraction Backends
- **Jina AI (Default)**: Free content extraction via [Jina AI Reader API](https://r.jina.ai/)
- **Firecrawl**: Advanced crawling with [Firecrawl API](https://firecrawl.dev) for complex websites

### Crawling Capabilities
- **Sitemap Discovery**: Auto-detects sitemaps from `robots.txt`, `/sitemap.xml`, and `/sitemap_index.xml`
- **Asynchronous Processing**: Parallel content extraction for improved performance
- **Clean Markdown Output**: Converts HTML content to markdown format
- **Aggregated Output**: Combines all pages into a single llms.txt file

### Technical Details
- **GitHub Actions Integration**: Runs as a composite action
- **Python 3.11**: Built with modern Python and async/await
- **Dependencies**: Uses `httpx`, `beautifulsoup4`, `lxml`, and `firecrawl-py`
- **Error Handling**: Graceful handling of failed requests and missing content

## Quick Start

### Basic Usage (Jina AI - Free)

Create `.github/workflows/generate-llms-txt.yml` in your repository:

```yaml
name: Generate AI-Optimized llms.txt
permissions:
  contents: write
on:
  push:
    branches: [ main ]
  schedule:
    - cron: '0 2 * * 0' # Weekly updates

jobs:
  generate-llms-txt:
    runs-on: ubuntu-latest
    steps:
      - name: Checkout repository
        uses: actions/checkout@v4

      - name: Generate llms.txt with Jina AI
        uses: kevinnkansah/llms-txt-action@v1.1.0
        with:
          domain: https://your-website.com
          outputFile: public/llms.txt
          # backend: jina  # Default, free option

      - name: Commit and push llms.txt
        uses: EndBug/add-and-commit@v9
        with:
          author_name: 'AI Bot'
          author_email: 'ai-bot@your-domain.com'
          add: 'public/llms.txt'
          message: 'feat: update llms.txt for AI optimization'
```

### Advanced Usage (Firecrawl)

For complex websites requiring advanced crawling:

```yaml
- name: Generate llms.txt with Firecrawl
  uses: kevinnkansah/llms-txt-action@v1.1.0
  with:
    domain: https://your-complex-website.com
    outputFile: docs/llms.txt
    backend: firecrawl
    firecrawl_api_key: ${{ secrets.FIRECRAWL_API_KEY }}
```

## Inputs

| Name                | Required | Description                                                                                                | Default              |
|---------------------|----------|------------------------------------------------------------------------------------------------------------|----------------------|
| `domain`            | **Yes**  | The full URL of the site to crawl (e.g., `https://example.com`).                                            |                      |
| `outputFile`        | No       | The path where the final `llms.txt` file will be saved.                                                    | `public/llms.txt`    |
| `backend`           | No       | Content extraction backend: `"jina"` (free) or `"firecrawl"` (requires API key).                        | `jina`               |
| `jina_api_key`      | No       | Your Jina AI Reader API key. Optional for Jina backend, recommended for higher rate limits. Store this as a [GitHub Secret](https://docs.github.com/en/actions/security-guides/using-secrets-in-github-actions). |                      |
| `firecrawl_api_key` | No       | Your Firecrawl API key. Required when using Firecrawl backend. Get one from [firecrawl.dev](https://firecrawl.dev). Store this as a [GitHub Secret](https://docs.github.com/en/actions/security-guides/using-secrets-in-github-actions). |                      |

## How It Works

This action first attempts to find your sitemap by checking `/robots.txt` and common paths like `/sitemap.xml`. It then parses the sitemap(s) to get a list of all page URLs. For each URL, it uses the selected backend to fetch the content as clean markdown:

- **Jina Backend (Default)**: Uses the free Jina AI Reader API (`https://r.jina.ai/`) 
- **Firecrawl Backend**: Uses the Firecrawl API for more advanced crawling capabilities

Finally, it aggregates the content from all pages into the specified `outputFile`.

## Usage Examples

### Using Jina Backend (Default)

```yaml
- name: Generate llms.txt with Jina
  uses: kevinnkansah/llms-txt-action@v1.1.1
  with:
    domain: https://dewflow.xyz
    outputFile: public/llms.txt
    # backend: jina  # Optional, this is the default
```

### Using Firecrawl Backend

```yaml
- name: Generate llms.txt with Firecrawl
  uses: kevinnkansah/llms-txt-action@v1.1.1
  with:
    domain: https://dewflow.xyz
    outputFile: public/llms.txt
    backend: firecrawl
    firecrawl_api_key: ${{ secrets.FIRECRAWL_API_KEY }}
```

## Use Cases

### Suitable For
- **Documentation Sites**: API docs, technical guides, knowledge bases
- **E-commerce**: Product catalogs, store policies, FAQ sections
- **Content Publishers**: Blogs, news sites, educational content
- **SaaS Companies**: Feature documentation, help centers
- **Business Websites**: Company info, services, contact details
- **Educational Sites**: Course materials, research papers

### Benefits
- **Better AI Citations**: Content gets properly attributed in AI responses
- **Enhanced Discoverability**: Improved visibility in AI-powered search
- **Structured Content**: Pre-formatted content for AI consumption
- **Content Control**: Curated content selection for AI models
- **Standard Compliance**: Follows the proposed llms.txt specification

## Frequently Asked Questions

<details>
<summary><strong>What's the difference between Jina and Firecrawl backends?</strong></summary>

**Jina AI (Default - Free)**
- Completely free to use
- Works well for most websites
- Fast and reliable
- Limited customization options

**Firecrawl (Premium)**
- Advanced crawling capabilities
- Better handling of JavaScript-heavy sites
- More extraction options
- Requires API key and credits

</details>

<details>
<summary><strong>How often should I update my llms.txt file?</strong></summary>

It depends on your content update frequency:
- **Daily**: For news sites or frequently updated blogs
- **Weekly**: For most business websites
- **Monthly**: For stable documentation or corporate sites
- **On-demand**: Trigger manually when major content changes occur

</details>

<details>
<summary><strong>What's the optimal llms.txt file size?</strong></summary>

- **Small sites**: 10KB - 100KB
- **Medium sites**: 100KB - 1MB
- **Large sites**: 1MB+

Note: Most LLMs have context windows of 128K-200K tokens (approximately 500KB-800KB of text).

</details>

<details>
<summary><strong>Is my content safe when using these APIs?</strong></summary>

**Jina AI**: Processes content on-demand, doesn't store your data permanently
**Firecrawl**: Enterprise-grade security, GDPR compliant

Both services:
- Use HTTPS encryption
- Don't train models on your data
- Process content temporarily for extraction only

</details>

<details>
<summary><strong>What if my site has a robots.txt that blocks crawlers?</strong></summary>

This action respects your robots.txt file. If you're blocking crawlers, you have options:
1. Add specific allow rules for AI crawlers
2. Manually create your llms.txt file
3. Use this action on a staging environment
4. Temporarily modify robots.txt during generation

</details>

<details>
<summary><strong>What are the costs?</strong></summary>

**Jina AI**: Completely free
**Firecrawl**: Pay-per-use pricing
- Free tier: 500 pages/month
- Paid plans: Starting at $29/month
- Enterprise: Custom pricing

**GitHub Actions**: Free for public repos, included minutes for private repos

</details>

<details>
<summary><strong>Can I customize the output format?</strong></summary>

Currently, the action generates standard llms.txt format. For custom formatting:
1. Fork this repository
2. Modify the `crawler.py` aggregation logic
3. Submit a PR if you think others would benefit

</details>

## 🌟 Real-World Examples

### E-commerce Store
```yaml
- name: Generate Product Catalog for AI
  uses: kevinnkansah/llms-txt-action@v1.1.0
  with:
    domain: https://mystore.com
    outputFile: ai/product-catalog.txt
    backend: firecrawl  # Better for complex product pages
    firecrawl_api_key: ${{ secrets.FIRECRAWL_API_KEY }}
```

### Documentation Site
```yaml
- name: Generate API Docs for AI
  uses: kevinnkansah/llms-txt-action@v1.1.0
  with:
    domain: https://docs.myapi.com
    outputFile: public/llms.txt
```

### Multi-language Site
```yaml
strategy:
  matrix:
    locale: [en, es, fr, de]
steps:
  - name: Generate llms.txt for ${{ matrix.locale }}
    uses: kevinnkansah/llms-txt-action@v1.1.0
    with:
      domain: https://mysite.com/${{ matrix.locale }}
      outputFile: public/llms-${{ matrix.locale }}.txt
```

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
