from typing import Any, List, NamedTuple, TypedDict, Union
from pydantic import BaseModel, PrivateAttr, validator


DEFAULT_POLICIES = [
    {
        "id": "S1",
        "name": "Violent Crimes",
        "description": "AI models should not create content that enables, encourages, or excuses the commission of violent crimes.",
        "prohibited_content": [
            "Unlawful violence toward people (e.g., terrorism, genocide, murder, hate crimes, child abuse, assault, battery, kidnapping)",
            "Unlawful violence toward animals (e.g., animal abuse)",
        ],
    },
    {
        "id": "S2",
        "name": "Non-Violent Crimes",
        "description": "AI models should not create content that enables, encourages, or excuses the commission of non-violent crimes.",
        "prohibited_content": [
            "Financial crimes (e.g., fraud, scams, money laundering)",
            "Property crimes (e.g., burglary, robbery, arson, vandalism)",
            "Drug crimes (e.g., creating or trafficking narcotics)",
            "Weapons crimes (e.g., producing unlicensed firearms)",
            "Cyber crimes (e.g., hacking, spyware, malware)",
        ],
    },
    {
        "id": "S3",
        "name": "Sex Crimes",
        "description": "AI models should not create content that enables, encourages, or excuses the commission of sex crimes.",
        "prohibited_content": [
            "Human trafficking",
            "Sexual assault (e.g., rape)",
            "Sexual harassment (e.g., groping)",
            "Lewd conduct",
        ],
    },
    {
        "id": "S4",
        "name": "Child Exploitation",
        "description": "AI models should not create content that depicts child nudity or that enables, encourages, excuses, or depicts the sexual abuse of children.",
    },
    {
        "id": "S5",
        "name": "Defamation",
        "description": "AI models should not create content about a real, living person that is verifiably false and likely to injure the person's reputation.",
    },
    {
        "id": "S6",
        "name": "Specialized Advice",
        "description": "AI models should not create content that contains specialized financial, medical, or legal advice.",
    },
    {
        "id": "S7",
        "name": "Privacy",
        "description": "AI models should not create content that contains sensitive, personal information about private individuals.",
    },
    {
        "id": "S8",
        "name": "Intellectual Property",
        "description": "AI models should not create content that violates the intellectual property rights of third parties.",
    },
    {
        "id": "S9",
        "name": "Indiscriminate Weapons",
        "description": "AI models should not create content that enables the creation of weapons of mass destruction.",
        "prohibited_content": [
            "Chemical weapons (e.g., nerve gas)",
            "Biological weapons (e.g., anthrax)",
            "Radiological weapons (e.g., salted bombs)",
            "Nuclear weapons (e.g., atomic warheads)",
            "High-yield explosive weapons (e.g., cluster munitions)",
        ],
    },
    {
        "id": "S10",
        "name": "Hate",
        "description": "AI models should not create content that is hateful toward people on the basis of their protected characteristics (race, color, ethnicity, national origin, disability, religious affiliation, caste, sexual orientation, sex, gender identity, and serious disease). AI models should not create content that perpetuates negative stereotypes.",
    },
    {
        "id": "S11",
        "name": "Self-Harm",
        "description": "AI models should not create content that enables, encourages, or excuses acts of intentional self-harm.",
        "prohibited_content": [
            "Suicide",
            "Self-injury (e.g., cutting)",
            "Disordered eating",
        ],
    },
    {
        "id": "S12",
        "name": "Sexual Content",
        "description": "AI models should not create depictions of nude adults or content that contains erotic descriptions or explicit depictions of sex acts.",
    },
    {
        "id": "S13",
        "name": "Elections",
        "description": "AI models should not create content that contains factually incorrect information about electoral systems and processes, including the time, place, or manner of voting in civic elections.",
    },
    {
        "id": "S14",
        "name": "Code Interpreter Abuse",
        "description": "AI models should not create content that attempts to abuse code interpreters.",
        "prohibited_content": [
            "Denial of service attacks",
            "Container escapes or privilege escalation",
        ],
    },
]


class Policy(BaseModel):
    id: str
    name: str
    description: str = ""
    prohibited_content: List[str] = None

    @validator("id", allow_reuse=True)
    def id_must_be_string(cls, v: str) -> str:
        if not v.startswith("S"):
            return f"S{v}"
        return str(v)

    def __repr__(self) -> str:
        return str(self)

    def __str__(self) -> str:
        if self.prohibited_content is None:
            return f"{self.id}: {self.name}\n{self.description}\n"
        prohibited_content = "\n".join(f" - {i}" for i in self.prohibited_content)
        return f"{self.id}: {self.name}\n{self.description}\n{prohibited_content}\n"


class PolicyManager(BaseModel):
    """
    PolicyManager is a class responsible for managing a collection of policies. It provides methods to add, remove, and retrieve policies.

    Attributes
    ----------
    policies : List[Policy]
        A list of Policy objects.

    Methods
    -------
    __init__(policies: List[Policy] = DEFAULT_POLICIES) -> None
        Initializes the PolicyManager with a list of policies.
    __repr__() -> str
        Returns a string representation of the PolicyManager.
    to_string() -> str
        Converts the list of policies to a string.
    add_policy(policy: Union[Policy, dict]) -> None
        Adds a new policy to the manager.
    remove_policy(policy_id: str) -> None
        Removes a policy from the manager by its ID.
    get_policy_ids() -> List[str]
        Returns a list of all policy IDs.

    Examples
    --------
    >>> from policy_manager import PolicyManager, Policy
    >>> policies = [Policy(id="S1", name="Policy1"), Policy(id="S2", name="Policy2")]
    >>> manager = PolicyManager(policies=policies)
    >>> print(manager)
    1: Policy1
    2: Policy2
    >>> new_policy = Policy(id="S3", name="Policy3")
    >>> manager.add_policy(new_policy)
    >>> print(manager)
    1: Policy1
    2: Policy2
    3: Policy3
    >>> manager.remove_policy("S2")
    >>> print(manager)
    1: Policy1
    3: Policy3
    >>> policy_ids = manager.get_policy_ids()
    >>> print(policy_ids)
    ['1', '3']
    """

    _hashed_policies: dict = PrivateAttr(default_factory=dict)
    policies: List[Policy]

    def __init__(self, policies: List[Policy] = DEFAULT_POLICIES) -> None:
        super().__init__(policies=policies)
        self._hashed_policies = {policy.id: policy for policy in self.policies}

    def __repr__(self) -> str:
        """Returns a string representation of the PolicyManager."""
        return str(self.to_string())

    def to_string(self) -> str:
        """Converts the list of policies to a string."""
        return "\n".join(repr(policy) for policy in self.policies)

    def add_policy(self, policy: Union[Policy, dict]) -> None:
        """Adds a new policy to the manager."""
        if isinstance(policy, dict):
            policy = Policy(**policy)
        self._hashed_policies[policy.id] = policy
        self.policies = self._hashed_policies.values()

    def remove_policy(self, policy_id: str) -> None:
        """Removes a policy from the manager by its ID."""
        self._hashed_policies.pop(policy_id)
        self.policies = self._hashed_policies.values()

    def get_policy_ids(self) -> List[str]:
        """Returns a list of all policy IDs."""
        return list(self._hashed_policies.keys())

    def __call__(self, policies: List[dict]) -> Any:
        """Add multiple policies to the manager"""
        _ = [self.add_policy(policy) for policy in policies]
        return self


# Create a global instance of the PolicyManager
def create_policy_manager(
    policies: List[dict] = [], extend: bool = False
) -> PolicyManager:
    """Create a global instance of the PolicyManager."""
    pm = PolicyManager()
    if not extend:
        pm.policies = []
        pm._hashed_policies.clear()
        return PolicyManager(policies=policies)

    return pm(policies)


class PolicyConfig(NamedTuple):
    id: str
    name: str
    description: str
    prohibited_content: List[str]


class PolicyManagerConfig(NamedTuple):
    policies: List[PolicyConfig] = []
    extend: bool = False
