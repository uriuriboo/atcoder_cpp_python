# AtCoder の言語環境（2025-10）に合わせる: C++23 (GCC 15.2.0)・Python (CPython 3.13.7)・Python (PyPy 3.11-v7.3.20)
# Ubuntu 26.04 は apt の g++ が GCC 15.2、pypy3 が 7.3.20 で、AtCoder と同じ
FROM mcr.microsoft.com/devcontainers/base:3-ubuntu26.04

# gdb はデバッガ、graphviz はグラフ可視化、gmp・boost は AtCoder にもあるライブラリ。ac-library は AtCoder と同じ v1.6
RUN apt-get update \
    && apt-get install -y g++ gdb graphviz libgmp-dev libboost-dev pypy3 \
    && git clone --depth 1 --branch v1.6 https://github.com/atcoder/ac-library.git /opt/ac-library

# CPython は uv で入れ、AtCoder と同じライブラリ（requirements.txt）を入れた venv を PATH の先頭に置く
# online-judge-tools（oj）は distutils を使うため、Python 3.12 以降では setuptools を一緒に入れる
COPY --from=ghcr.io/astral-sh/uv:latest /uv /usr/local/bin/
COPY requirements.txt /tmp/
USER vscode
ENV VIRTUAL_ENV=/home/vscode/.venv PATH=/home/vscode/.venv/bin:/home/vscode/.local/bin:$PATH
RUN uv venv --python 3.13.7 $VIRTUAL_ENV \
    && uv pip install -r /tmp/requirements.txt \
    && uv tool install --python 3.13.7 --with setuptools online-judge-tools

# AddressSanitizer のメモリリーク検出を切る（new したまま終わるコードを RE にしないため）
ENV ASAN_OPTIONS=detect_leaks=0
