__all__ = ["random_day", "random_string"]

import string
import random
from datetime import date, timedelta


def random_day(day1: date, day2: date) -> date:
    total_days = (day2 - day1).days

    randays = random.randrange(total_days)

    return day1 + timedelta(days=int(randays))


def random_string() -> str:
    # choose from all lowercase letter
    letters = string.ascii_lowercase
    return "".join(random.choice(letters) for _ in range(random.randrange(1, 10)))
