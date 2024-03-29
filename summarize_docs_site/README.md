# Summarize Docs

This script allows you to summarize multiple documents using the OpenAI API.

## Prerequisites

- Python 3.7 or higher
- An OpenAI API key

## Setup

1. Clone this repository to your local machine.
2. Create a virtual environment:
  ```bash
  python3 -m venv venv
  ```
3. Activate the virtual environment:
  - For Windows:
    ```bash
    venv\Scripts\activate
    ```
  - For macOS/Linux:
    ```bash
    source venv/bin/activate
    ```
4. Install the required packages:
  ```bash
  pip install -r requirements.txt
  ```
5. Export your OpenAI API key as an environment variable:
  ```bash
  export OPENAI_API_KEY=your-api-key
  ```

## Usage

To summarize documents in a directory, run the following command:

```
python ./summarize_docs.py /path/to/your/docs
```

Example output:
```
$ python ./summarize_docs.py/Users/petecheslock/repos/applandinc.github.io/_docs/integrations

Found 9 files.
Processing: //Users/petecheslock/repos/applandinc.github.io/_docs/integrations/atlassian-confluence.md
"AppMap integrates with Atlassian Confluence to generate interactive software diagrams from run-time data, enhancing documentation and collaboration on software projects."
Updated //Users/petecheslock/repos/applandinc.github.io/_docs/integrations/atlassian-confluence.md
Processing: //Users/petecheslock/repos/applandinc.github.io/_docs/integrations/postman.md
Learn how to import your OpenAPI definitions into Postman, adjust settings, and interact with your APIs. Detailed guide with visuals included.
Updated //Users/petecheslock/repos/applandinc.github.io/_docs/integrations/postman.md
Processing: //Users/petecheslock/repos/applandinc.github.io/_docs/integrations/smartbear-swaggerhub.md
"SwaggerHub allows teams to collaborate on API design, ensuring style, quality, and consistency. With AppMap integration, automate API documentation directly into SwaggerHub using GitHub Actions."
Updated //Users/petecheslock/repos/applandinc.github.io/_docs/integrations/smartbear-swaggerhub.md
Processing: //Users/petecheslock/repos/applandinc.github.io/_docs/integrations/readme.md
"Optimize your API interaction with Readme's developer hub. Easily add new endpoints and sync with your GitHub Action or CI system for efficient documentation."
```

If the description is already present or the title not found it will skip.

```
$ python ./summarize_docs.py /Users/petecheslock/repos/applandinc.github.io/_docs/integrations

Found 9 files.
Processing: /Users/petecheslock/repos/applandinc.github.io/_docs/integrations/atlassian-confluence.md
Skipping /Users/petecheslock/repos/applandinc.github.io/_docs/integrations/atlassian-confluence.md. Description present or title not found.
Processing: /Users/petecheslock/repos/applandinc.github.io/_docs/integrations/postman.md
Skipping /Users/petecheslock/repos/applandinc.github.io/_docs/integrations/postman.md. Description present or title not found.
Processing: /Users/petecheslock/repos/applandinc.github.io/_docs/integrations/smartbear-swaggerhub.md
Skipping /Users/petecheslock/repos/applandinc.github.io/_docs/integrations/smartbear-swaggerhub.md. Description present or title not found.
Processing: /Users/petecheslock/repos/applandinc.github.io/_docs/integrations/readme.md
```