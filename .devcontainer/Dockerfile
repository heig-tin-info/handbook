FROM ubuntu:24.04

RUN apt-get update && apt-get install -y \
    curl git wget curl python-is-python3 \
    python3-pip python3-poetry \
    build-essential make cmake gdb \
    libcairo2-dev \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /workspace