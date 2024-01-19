from openfinance.agentflow.llm.manager import ModelManager
from openfinance.agentflow.llm.chatgpt import ChatGPT
from openfinance.agentflow.llm.webgpt import WebGPT
from openfinance.agentflow.llm.aliyungpt import AliyunGPT
from openfinance.config import Config

ModelManager(Config()).register_model(
    model_name = "chatgpt",
    model_class = ChatGPT(
        model = ModelManager().conf("chatgpt", "model_name"),
        api_key = ModelManager().conf("chatgpt", "token"),
        base_url = ModelManager().conf("chatgpt", "api_base")
    )
)

ModelManager(Config()).register_model(
    model_name = "webgpt",
    model_class = WebGPT(
        model = ModelManager().conf("webgpt", "model_name"),
        api_key = ModelManager().conf("webgpt", "token"),
        base_url = ModelManager().conf("webgpt", "api_base")
    )
)

ModelManager(Config()).register_model(
    model_name = "aliyungpt",
    model_class = AliyunGPT(
        model = ModelManager().conf("aliyungpt", "model_name"),
        api_key = ModelManager().conf("aliyungpt", "token"),
        base_url = ModelManager().conf("aliyungpt", "api_base")
    )
)
