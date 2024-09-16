from langchain_core.prompts import PromptTemplate

# Used to build a context window from passages retrieved
document_prompt_template = """
---
EVENT NAME: {name}
EVENT PASSAGE:
{page_content}
---
"""

DOCUMENT_PROMPT = PromptTemplate.from_template(document_prompt_template)
