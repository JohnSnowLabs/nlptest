from typing import Dict, List, Union

from langtest.metrics.utils import PolicyManagerConfig, create_policy_manager


class SafetyEval:
    pipeline = None

    def __init__(
        self,
        model_name: str = "meta-llama/Llama-Guard-3-8B-INT8",
        hub: str = "huggingface",
        model_kwargs: Dict[str, str] = None,
        policies: PolicyManagerConfig = None,
    ) -> None:
        self.model_name = model_name
        self.hub = hub
        self.model_kwargs = model_kwargs or {}
        self.policy_manager = create_policy_manager(**policies)

        if SafetyEval.pipeline is None:
            SafetyEval.pipeline = self.load_pipeline()

    def load_pipeline(self):
        # from transformers import pipeline

        if self.hub == "huggingface":
            from transformers import pipeline

            pipe = pipeline("text-generation", model=self.model_name, **self.model_kwargs)
            return pipe
        else:
            from langtest.tasks import TaskManager

            task = TaskManager("question-answering")
            model = task.model(self.model_name, self.hub)
            return model.predict

    def evaluate_reponse(self, response: str) -> str:
        return response

    def evaluate(self, data: Union[str, List[str]]) -> str:
        return data

    def evaluate_batch(self, data: List[str]) -> List[str]:
        return data

    @staticmethod
    def reset_pipeline():
        SafetyEval.pipeline = None
