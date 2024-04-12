# base image
FROM python:3.9.7-buster

# options
ENV PYTHONUNBUFFERED 1
ENV PYTHONPATH=/app

# Set working directory
RUN mkdir app

# set the working directory
COPY . /app/

# coppy commands 
WORKDIR /app

# update docker-iamage packages
# RUN apt-get update && \
#     apt-get upgrade -y && \
#     apt-get install -y netcat-openbsd gcc && \
#     apt-get clean

# update pip 
RUN pip install --upgrade pip

# Install gunicorn
RUN pip install gunicorn

# install psycopg for connect to pgsql
RUN pip install psycopg2-binary

RUN pip install -r requirements.txt

COPY static /app/static

# Copy entrypoint script
COPY entrypoint.sh /entrypoint.sh

# Grant execute permissions to the entrypoint script
RUN chmod +x /entrypoint.sh

# Start the application
ENTRYPOINT ["/entrypoint.sh"]