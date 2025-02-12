from abc import ABC
from langtest.transform.base import ITests


class ComplianceTestFactory(ITests):
    """
    A class for running compliance tests.
    """


class BaseCompliance(ABC):
    pass


class ClincialGuidelines(BaseCompliance):
    pass
