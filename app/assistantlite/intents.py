import re
from dataclasses import dataclass
from typing import Callable, Dict, Any


@dataclass
class IntentRule:
    name: str
    pattern: re.Pattern
    handler: Callable[[Any, Dict[str, Any]], Dict[str, Any]]


INTENTS: list[IntentRule] = []


def intent(rule: IntentRule):
    INTENTS.append(rule)
    return rule
