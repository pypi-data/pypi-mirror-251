# flake8: noqa
from openfinance.agentflow.prompt.base import PromptTemplate
from openfinance.agents.role.role_base import build_from_name

growth_PROMPT = PromptTemplate(
    prompt=build_from_name("Growth Investor") + "\n{content}\m", variables=["content"])