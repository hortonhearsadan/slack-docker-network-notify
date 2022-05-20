import os

PERIOD = 60


class Settings:
    def __init__(self):
        self.period = os.getenv("PERIOD", PERIOD)
        self._check_alive = os.getenv("CHECK_ALIVE", [])
        self._check_country = os.getenv("CHECK_COUNTRY", [])
        self.country = os.getenv("COUNTRY", "CA")

        self.check_alive = parse(self._check_alive)
        self.check_country = parse(self._check_country)
        self.slack_webhook = os.getenv("SLACK_WEBHOOK")

    def __repr__(self):
        return f"{self.period} {self.check_country} {self.check_alive} {self.country}"


def parse(s: str):
    if s:
        return s.split(",")
    else:
        return s


settings = Settings()
