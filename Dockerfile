FROM tiangolo/uvicorn-gunicorn-fastapi:python3.7

LABEL maintainer="TJ Ward" \
    io.openshift.tags="quickapi" \
    io.k8s.description="Testing deploying a FastAPI application to openshift 3" \
    io.openshift.expose-services="8080:http,8443:https" \
    io.k8s.display-name="gene-tracker version 1" \
    io.openshift.tags="php,apache"

RUN apt-get -yqq update \
    && apt-get -yqq install --no-install-recommends vim

RUN pip install pipenv
ENV PORT=8080
ENV PROJECT_DIR=/app

EXPOSE 8080

COPY ./Pipfile ./Pipfile.lock ${PROJECT_DIR}/

RUN pipenv install --system --deploy

COPY ./app /app

RUN chgrp -R 0 /app \
    && chmod -R g+w /app

USER 1001
