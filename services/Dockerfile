FROM python:3.8-slim
WORKDIR /app

RUN apt-get update && apt-get -y install cron vim

COPY server ./
RUN pip install --no-cache-dir -r requirements.txt
ENV FLASK_DEBUG <0 or 1>
ENV ENVIRONMNET <"dev" or "prod">
ENV YOUTUBE_V3_API_KEY <YOUR-YOUTUBE-V3-API-KEY>

RUN mv cron_crawl /etc/cron.d/cron_crawl

# give execution rights
RUN chmod 0644 /etc/cron.d/cron_crawl

# apply cron job
RUN crontab /etc/cron.d/cron_crawl

# create log file
RUN touch /var/log/cron_crawl.log

EXPOSE 8000
CMD python3 hack.py
