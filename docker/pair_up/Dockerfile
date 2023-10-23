FROM python:3.10-bookworm

# Install Poetry for dependency management
RUN curl -sSL https://install.python-poetry.org | python3 -
WORKDIR /pair_up/
ADD pyproject.toml pyproject.toml
RUN /root/.local/bin/poetry config virtualenvs.create false \ 
    && /root/.local/bin/poetry install --compile --no-interaction --no-cache

RUN python3 -m pip install jupyterlab ipywidgets
