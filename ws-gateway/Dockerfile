FROM python:3.10 as requirements-stage

WORKDIR /tmp

RUN pip install poetry

COPY ./pyproject.toml ./poetry.lock* /tmp/

RUN poetry export -f requirements.txt --output requirements.txt --without-hashes

# This is the final stage, anything here will be preserved in the final container image.
FROM python:3.10

WORKDIR /code

COPY --from=requirements-stage /tmp/requirements.txt /code/requirements.txt

RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt

COPY ./ws_gateway /code

CMD ["uvicorn", "main:application", "--proxy-headers", "--forwarded-allow-ips", "'*'", "--host", "0.0.0.0", "--port", "80", "--log-level", "warning"]