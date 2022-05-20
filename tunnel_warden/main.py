import json
from json import JSONDecodeError
from time import sleep

import docker
import slack_sdk

from tunnel_warden.config import settings

CMD = "curl -m 3 -s ipinfo.io"


class BadDataException(Exception):
    pass


def check(container):
    response = container.exec_run(CMD)
    if response.exit_code == 0:
        try:
            data = json.loads(response.output.decode())
            return data
        except JSONDecodeError:
            print("Bad response, probably not connected")
    else:
        print("command didnt execute properly")


def check_connected(container):
    ip_check = check(container)
    return is_valid(ip_check)


def check_country(container, country):
    ip_check = check(container)
    if is_valid(ip_check):
        return is_correct_country(ip_check, country)
    else:
        return False


def is_valid(d):
    return isinstance(d, dict) and "ip" in d.keys()


def is_correct_country(d, country):
    return d["country"] == country


def main():
    sleep_time = settings.period
    client = docker.from_env()
    while True:
        connected_status, correct_country_status = get_statuses(client)
        print(correct_country_status)
        print(connected_status)

        if not all(connected_status.values()):
            send_message(connected_status, "Disconnected containers")
        if not all(correct_country_status.values()):
            send_message(
                correct_country_status,
                f"Containers not connected to {settings.country}",
            )

        sleep(int(sleep_time))


def format_msg(status, message):
    msg = message + "\n" + "\n".join(k for k, v in status.items() if not v)
    return msg


def get_statuses(client):
    targets = set(settings.check_country or [] + settings.check_country or [])

    if not targets:
        print("no targets set, please set correct env vars")
    connected_status = {}
    correct_country_status = {}
    for container in client.containers.list():
        name = container.name
        if name not in targets:
            continue

        ip_info = check(container)

        if name in settings.check_alive:
            connected_status[name] = is_valid(ip_info)

        if name in settings.check_country:
            correct_country_status[name] = is_correct_country(ip_info, settings.country)
    return connected_status, correct_country_status


def send_message(status, message):
    if not settings.slack_webhook:
        print("No webhook provided")
    slack_client = slack_sdk.WebhookClient(settings.slack_webhook)
    msg = format_msg(status, message)
    print(msg)
    slack_client.send(text=msg)


if __name__ == "__main__":
    main()
