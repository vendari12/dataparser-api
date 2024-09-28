FROM python:3.12-bullseye


# Install system dependencies and psycopg2 dependencies in one go, and clean up
RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc \
    build-essential \
    musl-dev \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Set working directory
WORKDIR /src

# Set environment variables for Python behavior
ENV PYTHONIOENCODING=UTF-8
ENV PYTHONUNBUFFERED=1


# Copy the entire application to /src
COPY .. /src/

# Upgrade pip and setuptools, then install the required dependencies
RUN python -m pip install --upgrade pip setuptools \
    && pip install --no-cache-dir -r ./requirements.txt 

# Expose the desired port
EXPOSE 8080

CMD ["gunicorn", "-c", "parserapp/gunicorn.conf.py", "parserapp.wsgi:application"]
