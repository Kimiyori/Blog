FROM python:3.11
# Set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
# Set work directory
WORKDIR /backend
# Install dependencies
COPY poetry.lock pyproject.toml /backend/
RUN pip install poetry
RUN poetry config virtualenvs.create false
RUN poetry install --no-root
# Copy project
COPY . /backend
