ARG WORKDIR=/usr/local/conveniencer \
    VIRTUALENV=$WORKDIR/env \
    VPATH=$VIRTUALENV/bin


FROM python:3.12-slim AS build

ARG WORKDIR \
    VIRTUALENV \
    VPATH

ENV PATH=$VPATH:$PATH

WORKDIR $WORKDIR

RUN python3 -m venv $VIRTUALENV

COPY requirements.txt .

RUN pip install -r requirements.txt

COPY . .

RUN pip install .


FROM python:3.12-slim AS final

ARG WORKDIR \
    VIRTUALENV \
    VPATH

ENV PATH=$VPATH:$PATH

WORKDIR $WORKDIR

COPY --from=build $VIRTUALENV $VIRTUALENV

COPY .bot .

CMD ["run"]
