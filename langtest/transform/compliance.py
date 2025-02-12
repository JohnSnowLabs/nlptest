from abc import ABC, abstractmethod
import asyncio
from collections import defaultdict
from typing import Dict, List, TypedDict
from langtest.errors import Errors
from langtest.modelhandler.modelhandler import ModelAPI
from langtest.transform.base import ITests
from langtest.utils.custom_types.sample import Sample


class ComplianceTestFactory(ITests):
    """
    A class for running compliance tests.
    """

    alias_name = "compliance"

    def __init__(self, data_handler: List[Sample], tests: Dict = None, **kwargs):

        self.supported_tests = self.available_tests()
        self.data_handler = data_handler
        self.tests = tests
        self.kwargs = kwargs

        if not isinstance(self.tests, dict):
            raise ValueError(Errors.E048())

        if len(self.tests) == 0:
            self.tests = self.supported_tests

        non_supported_tests = set(self.tests.keys()) - set(self.supported_tests.keys())

        if len(non_supported_tests) > 0:
            raise ValueError(
                Errors.E049(
                    non_supported_tests, supported_tests=list(self.supported_tests.keys())
                )
            )

    def transform(self) -> List[Sample]:

        all_samples = []

        for test_name, params in self.tests.items():
            test = self.supported_tests[test_name](
                data_handler=self.data_handler, **params
            )
            all_samples.extend(test.transform())

        return all_samples

    @staticmethod
    def available_tests() -> Dict[str, type["BaseCompliance"]]:

        return BaseCompliance.test_types


class BaseCompliance(ABC):

    test_types = defaultdict(lambda: BaseCompliance)
    alisa_name = None

    supported_tasks = [
        "question_answering",
    ]

    TestConfig = TypedDict(
        "TestConfig",
        min_pass_rate=float,
    )

    @staticmethod
    @abstractmethod
    def transform(sample_list: List[Sample]) -> List[Sample]:
        pass

    @staticmethod
    @abstractmethod
    async def run(sample_list: List[Sample], model: ModelAPI, **kwargs) -> List[Sample]:
        pass

    @classmethod
    async def async_run(cls, sample_list: List[Sample], model: ModelAPI, **kwargs):
        created_task = asyncio.create_task(cls.run(sample_list, model, **kwargs))
        return created_task

    def __init_subclass__(cls, *args, **kwargs):
        alias = cls.alias_name if isinstance(cls.alias_name, list) else [cls.alias_name]
        for name in alias:
            BaseCompliance.test_types[name] = cls


class ClincialGuidelines(BaseCompliance):
    pass
