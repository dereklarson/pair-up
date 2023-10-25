FROM python:3.10-bookworm

RUN python3.10 -m pip install --upgrade pip

# Install Poetry for dependency management
RUN curl -sSL https://install.python-poetry.org | python3 -
WORKDIR /pair_up/
ADD pyproject.toml pyproject.toml
RUN /root/.local/bin/poetry config virtualenvs.create false \ 
    && /root/.local/bin/poetry install --compile --no-interaction --no-cache

ADD pairup pairup
ADD streamlit_app.py streamlit_app.py
ADD config.toml .streamlit/config.toml

CMD ["streamlit", "run", "--browser.serverAddress=0.0.0.0", "streamlit_app.py"]
