# flake8: noqa
# flake8: noqa
from openfinance.agentflow.prompt.base import PromptTemplate

prompt_template_cot = """
Only use you stock analysis framework to analyze as accurately as possible. 
Input: 
{content}
you must respond in following format

Thought:  
- what entity is influenced mainly, entity must be in Chinese
- which level entity belong to, must one of [{types}]
- what financial indicator is influenced mainly, indicator must be in English
- what event is happenning to entity, event must be briefly in Chinese
- what sentiment is event, one of [Positive Negative Neural]
Result:
{{
    "consequence": [
        {{  
            "entity": "",
            "level": "",            
            "event": "",
            "indicator": "",
            "sentiment": ""
        }}
    ]
}}

Let's begin! 
"""


OPINION_PROMPT = PromptTemplate(
    prompt=prompt_template_cot, variables=["content", "types"])

match_prompt_template = """
Task: 
you must find the most related indicator to {content} from [{indicators}]
you can only reply the indicator name, otherwise None
Answer:
"""

MATCH_PROMPT = PromptTemplate(
    prompt=match_prompt_template, variables=["content", "indicators"])