import asyncio
from typing import (
    Any,
    Callable,
    Dict,
    Union,
    List
)

from openfinance.agentflow.flow.base import BaseFlow
from openfinance.agentflow.llm.chatgpt import ChatGPT
from openfinance.agentflow.llm.base import BaseLLM
from openfinance.agentflow.base_parser import BaseParser
from openfinance.agentflow.prompt.base import PromptTemplate

from openfinance.datacenter.knowledge.entity_graph import EntityGraph, EntityEnum
from openfinance.agents.promptflow.entity.prompt import OPINION_PROMPT
from openfinance.agents.promptflow.entity.output_parser import TaskOutputParser


class EntityFlow(BaseFlow):
    name = "EntityFlow"
    inputs: List[str] = ["content"]
    prompt: PromptTemplate = OPINION_PROMPT
    parser: BaseParser = TaskOutputParser()

    class Config:
        """Configuration for this pydantic object."""
        arbitrary_types_allowed = True

    @classmethod
    def from_llm(
        cls,
        llm: BaseLLM,
        **kwargs: Any        
    ) -> 'PercepFlow':
        return cls(llm=llm, **kwargs)

    async def acall(
        self,
        content: str,
        **kwargs: Any        
    ) -> Dict[str, str]:
        inputs = {"content": content}
        for i in self.inputs:
            if i != "content":
                inputs[i] = kwargs[i]
        resp = await self.llm.acall(self.prompt.prepare(inputs))
        resp = self.parser.parse(resp.content)
        return {self.output: resp}

if __name__ == "__main__":
    from openfinance.config import Config
    from openfinance.agentflow.llm.manager import ModelManager
    llm = ModelManager(Config()).get_model("aliyungpt")
    flow = EntityFlow.from_llm(llm)
    result = asyncio.run(flow._acall(
        #content="【食品股震荡反弹 惠发食品涨停】财联社12月27日电，惠发食品涨停，盖世食品、青岛食品、一鸣食品涨超5%，阳光乳业、仲景食品、海欣食品等跟涨。万和证券研报表示，具有中国特色口味特征的咸辣零食保持较高速增长，行业红利依旧存在。"
        content="翔腾新材涨停】财联社12月27日电，OLED板块震荡走强，翔腾新材涨停，冠石科技、凯盛科技、莱特光电、清越科技等跟涨。消息面上，根据公开信息显示，2024年三星低阶手机将有3000万支弃LCD改采OLED，为三星首次在低阶手机以OLED机种试水温。天风证券预计OLED面板大部分将采用自家产品。此次事件会进一步拉动OLED产业链明年景气度。"
    ))
    print(result)