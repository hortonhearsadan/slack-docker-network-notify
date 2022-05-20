import os

PERIOD = 60


class Settings:
    def __init__(self):
        self.period = os.getenv("PERIOD", PERIOD)
        self._check_alive = os.getenv("CHECK_ALIVE", None)
        self._check_country = os.getenv("CHECK_COUNTRY", None)
        self.country = os.getenv("COUNTRY", "CA")

        self.check_alive = parse(self._check_alive)
        self.check_country = parse(self._check_country)
        self.slack_webhook = os.getenv("SLACK_WEBHOOK")


def parse(s: str):
    if s:
        return s.split(",")


settings = Settings()
