import asyncio
import json
from typing import Dict
from openfinance.config import Config

from openfinance.agents.agent.base import Agent
from openfinance.agentflow.llm.manager import ModelManager 
from openfinance.agents.tool.factor_search import FactorSearchTool

from openfinance.agents.promptflow.plan.base import PlanFlow
from openfinance.agents.promptflow.summary.base import SummaryFlow

from openfinance.datacenter.echarts.base import ChartManager
from openfinance.service.base import wrapper_return
from openfinance.searchhub.task.base import Task

class AnalysisTask(Task):
    name = "analysis"

    def __init__(
        self
    ):
        llm = ModelManager(Config()).get_model("aliyungpt")
        self.agent = Agent.from_scratch(
            llm = llm,
            role="Stock Analyst",
            goal="Try your best to provide professional and helpful financial advices",
            tools={
                "search": FactorSearchTool.create()
            },
            skills={
                "plan":  PlanFlow.from_llm(llm),
                "summary": SummaryFlow.from_llm(llm)
            }
        )

    def execute(
        self,
        text,
        **kwargs
    ) -> Dict[str, str]:
        pass

    async def aexecute(
        self,
        text,
        **kwargs
    ) -> Dict[str, str]:
        # print("enter async")
        plan_data = await self.agent.skills["plan"].acall(**{
            "content": text
        })

        websocket = kwargs.get("websocket", None)

        chart = ChartManager().get("tree")(plan_data['output'])
        if websocket:
            if websocket.open:
                await websocket.send(wrapper_return(
                    output=f"\n{text}正在从基于以下维度分析，请耐心等待...\n", chart=chart
                ))
            else:
                raise f"websocket lost"
        
        #summary_data = {}
        summary_data = ""
        for item in plan_data["output"].keys():
            result = await self.agent.tools["search"].acall(
                item,
                **kwargs
            )
            if isinstance(result["output"], list):
                summary_data += "Task(" + item + "):---\n"               
                for it in result["output"]:
                    if it["result"]:
                        summary_data += it["result"] + "\n"
                        if websocket:
                            if websocket.open:
                                await websocket.send(wrapper_return(
                                    output = it
                                ))
                            else:
                                raise f"websocket lost"   
                summary_data += "---"            
            else:
                if websocket:
                    if websocket.open:
                        await websocket.send(wrapper_return(
                            output = item
                        ))
                        await websocket.send(wrapper_return(
                            output = result["output"]
                        ))
                    else:
                        raise f"websocket lost"
                print(result)
                #summary_data[item] = result["output"]["result"]
                if result["output"]:
                    summary_data += "Task(" + item + "):\n" + result["output"]["result"] + "\n"
        
        result = await self.agent.skills["summary"].acall(**{
            "content": text,
            "document": str(summary_data)
        })
        print(result)
        return {"result": result['output']}

if __name__ == '__main__':
    task = AnalysisTask()
    result = asyncio.run(task.aexecute("是否可以买入比亚迪的股票", company="比亚迪"))
    #result = asyncio.run(task.aexecute("为什么最近一直在下跌", company="华工科技"))
    #result = asyncio.run(task.aexecute("为什么游戏公司股价下跌这么多", company="游戏"))
    print(result)
