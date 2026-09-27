# Use an official, minimal Python runtime blueprint image
FROM python:3.11-slim

# Set the working folder path inside the isolated container
WORKDIR /app

# Copy the app script from your local machine folder into the container
COPY app.py .

# Force Python outputs to print instantly to the terminal console screen
ENV PYTHONUNBUFFERED=1

# Tell the container to execute this command when it boots up
CMD ["python", "app.py"]
