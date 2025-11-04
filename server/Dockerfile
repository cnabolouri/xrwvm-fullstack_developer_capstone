FROM python:3.12.0-slim-bookworm

ENV PYTHONUNBUFFERED=1
ENV PYTHONWRITEBYTECODE=1
ENV APP=/app

WORKDIR $APP

# Copy dependency file and install requirements
COPY requirements.txt $APP
RUN pip install --no-cache-dir -r requirements.txt

# Copy project files
COPY . $APP

EXPOSE 8000

# Make entrypoint script executable
RUN chmod +x /app/entrypoint.sh

# Run DB migrations automatically and start Gunicorn
ENTRYPOINT ["/bin/bash","/app/entrypoint.sh"]
CMD ["gunicorn", "--bind", ":8000", "--workers", "3", "djangoproj.wsgi"]
