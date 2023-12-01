FROM mcr.microsoft.com/devcontainers/python:3
RUN apt-get update && export DEBIAN_FRONTEND=noninteractive \
    && apt-get -y install --no-install-recommends ca-certificates \
    && apt-get autoremove -y && apt-get clean -y && rm -rf /var/lib/apt/lists/*
