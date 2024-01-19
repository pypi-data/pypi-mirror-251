from typing import Any, Dict, List, Optional, Callable
from openfinance.datacenter.knowledge.executor import Executor
from openfinance.datacenter.knowledge.wrapper import wrapper
from openfinance.datacenter.knowledge.entity_graph import EntityEnum

factor_to_type = {
    "Industry Analysis": EntityEnum.Industry.type,
    "Market Analysis": EntityEnum.Market.type,
    "Macro Economic": EntityEnum.Economy.type,        
}

class Factor:
    '''
        class for factor, used in graph
    '''    
    def __init__(
        self,
        name: str,
        description: str,
        paths: List[str],
        parents: List['Factor'] = [],
        childrens: List['Factor'] = [],
        executor: Executor = None,
    ):
        self.name = name
        self.description = description
        self.paths = paths
        self.parents = parents
        self.childrens = childrens
        self.executor = executor

    @classmethod
    def create(
        cls,
        name: str,
        description: str
    ) -> 'Factor':
        return cls(name=name, description=description)

    def __call__(
        self,
        *args: Any,        
        **kwargs: Any        
    ) -> Any:
        """
            Args:
                    rootNode: original rootNode for choosing path
            Return:
                    list of dict
        """
        # print(self.name)
        # print(kwargs)
        funcs = kwargs.get("func", []) # get existed function
        if self.executor.func.__name__ in funcs:
            return 
        funcs.append(self.executor.func.__name__)
        kwargs["func"] = funcs 
        # print(self.name, funcs, kwargs)      
        kwargs = self.update_entity_type(**kwargs)
        # print(kwargs)
        result = self.executor(*args, **kwargs)
        if result:           
            if len(self.childrens):
                result = [result]
                for child in self.childrens:
                    if child.executor: # if no excutor, drop it
                        child_ret = child(*args, **kwargs)
                        if child_ret: # if empty response, drop it
                            result.append(child_ret)
                return wrapper(result)
        return wrapper(result)

    def update_entity_type(
        self,
        **kwargs: Any        
    ) -> {}:
        if "entity_type" in kwargs:
            return kwargs
        else:
            if self.name in factor_to_type:
                kwargs.update({
                    "entity_type": factor_to_type[self.name]
                })
        return kwargs

    def add_path(
        self, 
        paths
    ):
        self.paths.append(paths)

    def register_func(
        self, 
        func: Executor
    ):
        self.executor = func
    
    def add_parents(
        self, 
        parent: 'Factor'
    ):
        if parent not in self.parents:
            self.parents.append(parent)

    def get_parents(
        self
    ) -> List['Factor']:
        return self.parents

    def add_childrens(
        self, 
        child: 'Factor'
    ):
        if child not in self.childrens:
            self.childrens.append(child)

    def get_childrens(
        self
    ) -> List['Factor']:
        return self.childrens