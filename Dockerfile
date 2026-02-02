FROM python:3.11

# The installer requires curl (and certificates) to download the release archive
RUN apt-get update && apt-get install -y --no-install-recommends curl ca-certificates \
    && rm -rf /var/lib/apt/lists/*

# Download the latest installer
ADD https://astral.sh/uv/0.5.26/install.sh /uv-installer.sh

# Run the installer then remove it
RUN sh /uv-installer.sh && rm /uv-installer.sh

# Ensure the installed binary is on the `PATH`
ENV PATH="/root/.local/bin/:$PATH"

WORKDIR /app

# Copy dependency files
ADD ./pyproject.toml ./uv.lock ./
RUN pip install uv

# Create virtual environment in a location that won't be overwritten
RUN uv venv /opt/venv
RUN uv sync --frozen

# Activate the virtual environment by updating PATH
ENV PATH="/opt/venv/bin:$PATH"

RUN echo "hello world"

ADD ./ ./

EXPOSE 8000
EXPOSE 8001

CMD [ "uv", "run", "uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000" ]