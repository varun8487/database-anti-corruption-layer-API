FROM python:3.9-slim

WORKDIR /app

# Copy the requirements file and install dependencies.
COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the source code.
COPY . .

# Expose the port the app will run on.
EXPOSE 3000

# Set the environment variable to specify the configuration file location.
ENV QUERY_MAPPING_FILE=/app/query_mappings.yaml

CMD ["python", "app.py"]
