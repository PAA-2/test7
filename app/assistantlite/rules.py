import re
from .intents import IntentRule, intent
from .handlers import (
    create_action_handler,
    request_check_handler,
    set_due_handler,
    sync_plan_handler,
    export_csv_handler,
)

intent(
    IntentRule(
        name="create_action",
        pattern=re.compile(r"^(?:nouvelle|new)\s+action\s*:\s*(?P<title>.+)$", re.I),
        handler=create_action_handler,
    )
)

intent(
    IntentRule(
        name="request_check",
        pattern=re.compile(
            r"^(?:check|demander\s+check)\s+(?P<code>[A-Z0-9\-]{3,})$", re.I
        ),
        handler=request_check_handler,
    )
)

intent(
    IntentRule(
        name="set_due_plus",
        pattern=re.compile(
            r"^(?:delai|deadline)\s+(?P<code>[A-Z0-9\-]{3,})\s*\+\s*(?P<days>\d{1,3})j$",
            re.I,
        ),
        handler=set_due_handler,
    )
)

intent(
    IntentRule(
        name="sync_plan",
        pattern=re.compile(r"^(?:sync|synchro)\s+(?P<plan>[A-Z0-9\-]{2,})$", re.I),
        handler=sync_plan_handler,
    )
)

intent(
    IntentRule(
        name="export_csv",
        pattern=re.compile(r"^(?:export\s+actions)$", re.I),
        handler=export_csv_handler,
    )
)
