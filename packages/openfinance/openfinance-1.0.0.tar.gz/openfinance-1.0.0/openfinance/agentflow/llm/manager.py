from openfinance.utils.singleton import singleton

@singleton
class ModelManager:
    def __init__(
        self, 
        config
    ):
        self.config = config
        self.models = {}

    def conf(
        self,
        model,
        key
    ):
        return self.config.get("models")[model][key]

    def register_model(
        self, 
        model_name, 
        model_class
    ):
        self.models[model_name] = model_class
        
        if not self.config.get(model_name):
            self.config.set(model_name, {})
            
    def get_model(
        self, 
        model_name
    ):
        return self.models[model_name]

