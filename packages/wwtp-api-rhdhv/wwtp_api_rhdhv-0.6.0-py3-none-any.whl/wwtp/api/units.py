from abc import ABC

from wwtp.api.settings import ScenarioSettings


class Unit(ABC):
    day_number: int
    scenario_settings: ScenarioSettings


class ProcessUnit(Unit):
    pass


class MergeUnit(Unit):
    pass


class SplitUnit(Unit):
    pass
