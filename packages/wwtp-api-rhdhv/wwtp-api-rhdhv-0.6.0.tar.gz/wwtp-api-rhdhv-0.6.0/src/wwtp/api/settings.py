from abc import ABC
from typing import TypeVar


class IScenarioSettings(ABC):
    pass


ScenarioSettings = TypeVar('ScenarioSettings', bound=IScenarioSettings)
