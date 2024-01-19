# flake8: noqa
from openfinance.agentflow.prompt.base import PromptTemplate
from openfinance.agents.role.role_base import build_from_name

Catherine_Wood_PROMPT = PromptTemplate(
    prompt=build_from_name("Catherine Wood") + "\n{content}\m", variables=["content"])