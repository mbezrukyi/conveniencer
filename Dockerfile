FROM python:3.12-slim

ENV WORKDIR=/usr/local/conveniencer
ENV VIRTUALENV=$WORKDIR/env
ENV PATH=$VIRTUALENV/bin/:$PATH

WORKDIR $WORKDIR

RUN python3 -m venv $VIRTUALENV

COPY . .

RUN pip install -e .

CMD ["run"]
