FROM acidrain/python-poetry:3.10
RUN apt-get update
RUN apt-get -y install apt-transport-https ca-certificates curl gnupg2 software-properties-common
RUN curl -fsSL https://download.docker.com/linux/debian/gpg | apt-key add -
RUN add-apt-repository "deb [arch=amd64] https://download.docker.com/linux/debian $(lsb_release -cs) stable"

RUN apt-get update
RUN apt-get -y install docker-ce



COPY ./ /app/

WORKDIR /app

RUN set -eu; \
    export PATH="${HOME}/.local/bin:${PATH}"; \
    poetry config virtualenvs.in-project true; \
    poetry install --no-dev;

CMD poetry run python tunnel_warden/main.py