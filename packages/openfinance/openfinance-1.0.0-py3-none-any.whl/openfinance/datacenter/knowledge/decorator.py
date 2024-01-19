from functools import wraps
from openfinance.datacenter.knowledge.executor import ExecutorManager

def register(name, description, signature="default", graph_node=True, **extend):
    #print("register")
    def call(func):
        #print("call")
        ExecutorManager().register(
            name = name,
            func = func,
            description = description,
            signature = signature,
            graph_node = graph_node,
            **extend
        )
        @wraps(func)
        def wrapper(*args, **kwargs):
            return func(*args, **kwargs)
        return wrapper       
    return call