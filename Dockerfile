FROM python:3.10.2-slim as builder

WORKDIR /alco-map
RUN apt update && apt install -y build-essential
RUN python -m venv env
COPY requirements/production.txt requirements/production.txt
RUN env/bin/python -m pip install -r requirements/production.txt


FROM python:3.10.2-slim as runner

COPY --from=builder /alco-map /alco-map
WORKDIR /alco-map
COPY ./ ./
RUN env/bin/python -m pip install -e ./

CMD ["env/bin/python", "-m", "alco_map"]
