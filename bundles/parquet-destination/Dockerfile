# Hook image for the parquet-destination bundle. Everything the
# setup/validate/cleanup scripts need (Python + pyarrow) is baked in here, so a
# bundle run needs nothing installed on the host beyond Docker itself.
FROM python:3.12-slim

RUN pip install --no-cache-dir pyarrow

COPY scripts/ /scripts/
RUN chmod +x /scripts/*
