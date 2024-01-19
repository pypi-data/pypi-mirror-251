# flake8: noqa
# flake8: noqa
from openfinance.agentflow.prompt.base import PromptTemplate

prompt_template_cot = """
Extract the main Industry and Company Entities from Article:
```
{content}
```
Entity must belong to Industry or Company, if not, you should remain empty

Answer in format:
Result:
{{
    "Industry": [],
    "Company": []
}}

Let's begin! 
"""

OPINION_PROMPT = PromptTemplate(
    prompt=prompt_template_cot, variables=["content"])