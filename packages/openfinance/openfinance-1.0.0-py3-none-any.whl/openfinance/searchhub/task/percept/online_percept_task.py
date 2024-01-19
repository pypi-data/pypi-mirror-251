import asyncio
import json
import re

from time import strftime, gmtime
from typing import Dict
from openfinance.config import Config

from openfinance.datacenter.database.source.event.cailianshe import get_cailianshe_news

from openfinance.datacenter.database.base import Database
from openfinance.searchhub.recall.base import IndexManager
from openfinance.utils.embeddings.embedding_manager import EmbeddingManager

from openfinance.robot.wechat.base import Wechat
from openfinance.service.base import wrapper_return

from openfinance.searchhub.task.percept.percept_task import PerceptTask

db = Database(Config().get("db"))

class OnlinePerceptTask(PerceptTask):
    name = "online_percept"
    async def aexecute(
        self, 
        text, 
        **kwargs
    ) -> Dict[str, str]:
        print("text", text)
        websocket = kwargs.get("websocket", None)
        wechat = kwargs.get("wechat", None)

        if websocket:
            if websocket.open:
                await websocket.send(wrapper_return("\n开始分析新闻...\n"))
            else:
                raise f"websocket lost"
        save_db = kwargs.get("save_db", False)
        sleep_duration = 5 * 60
        docs = list()
        max_len = 15
        while True:
            try:
                jsondata = get_cailianshe_news()
                for d in jsondata["data"]["roll_data"]:
                    if d["id"] in docs:
                        continue
                    if len(docs) == 10:
                        docs.pop(0)
                    docs.append(d["id"])
                    # delete summary docs
                    if re.search(r".*（.*）.*", d["title"]):
                        continue
                    if len(docs) == max_len:
                        docs.pop(0)
                    content = d["content"]
                    percept_data = await self.percept.acall(**{
                        "content": content
                    })

                    match_result = await self.match.acall(**{
                        "content": percept_data["output"],
                        "channel": self.name,         
                    })
                    
                    if save_db:
                        for match in match_result['output']:
                            db.insert(
                                "t_news_percept",
                                {
                                    "entity": match["entity"],
                                    "entity_type": match["level"],
                                    "indicator": match["indicator"],
                                    "effect": match["sentiment"],
                                    "src": match["event"],
                                    "sid": str(d["id"])
                                }
                            )
                    if websocket:
                        if websocket.open:
                            await websocket.send(wrapper_return(
                                output = str(news)
                            ))                            
                            await websocket.send(wrapper_return(
                                output = str(match)
                            ))
                        else:
                            raise f"websocket lost" 
                    if wechat:
                        for match in match_result['output']:
                            #msg = "新闻: " + d["title"] + "\n"
                            msg = ""
                            msg += "主体: " + match["entity"] + "\n"
                            msg += "事件: " + match["event"] + "\n"
                            msg += "指标: " + match["indicator"] + "\n"
                            msg += "情绪: " + match["sentiment"]
                            Wechat.push(msg)
                await asyncio.sleep(sleep_duration)
            except Exception as e:
                print("Exception:", e)
        return {self.output: "finish detect!"}

if __name__ == '__main__':
    task = OnlinePerceptTask() 
    result = asyncio.run(task.aexecute("开始", save_db=True, wechat=True))
    print(result)