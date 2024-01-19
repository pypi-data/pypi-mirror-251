# flake8: noqa
from openfinance.agentflow.prompt.base import PromptTemplate

plan_prompt_template_v1 ="""
Question: {content}
```
{document}
```
Try you best to answer reasonable and helpfully in Chinese, think step by step.
"""

plan_prompt_template_v2 ="""
Question: {content}
Tasks:
```
{document}
```
Infer reasonable and helpfully to Question task by task.
After all tasks, then conclude your answer
"""

PROMPT = PromptTemplate(
    prompt=plan_prompt_template_v2, variables=["content", "document"])