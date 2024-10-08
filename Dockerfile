FROM tiangolo/uwsgi-nginx:python3.12

RUN apt-get update && apt-get install -y \
    wget \
    gnupg \
    curl \
    unzip \
    apt-transport-https \
    ca-certificates \
    --no-install-recommends && \
    apt-get clean

ENV TZ=Asia/Bangkok
RUN ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && echo $TZ > /etc/timezone

RUN wget -q -O - https://dl.google.com/linux/linux_signing_key.pub | apt-key add - && \
    sh -c 'echo "deb http://dl.google.com/linux/chrome/deb/ stable main" > /etc/apt/sources.list.d/google-chrome.list' && \
    apt-get update && apt-get install -y google-chrome-stable=129.0.6668.89-1

RUN CHROMEDRIVER_VERSION=129.0.6668.89 && \
    wget -q "https://storage.googleapis.com/chrome-for-testing-public/${CHROMEDRIVER_VERSION}/linux64/chromedriver-linux64.zip" -O /tmp/chromedriver.zip && \
    if [ -s /tmp/chromedriver.zip ]; then \
    echo "Download successful"; \
    unzip /tmp/chromedriver.zip -d /usr/local/bin/; \
    chmod +x /usr/local/bin/chromedriver; \
    echo "Unzip successful"; \
    else \
    echo "Download failed or file is empty" && exit 1; \
    fi && \
    rm /tmp/chromedriver.zip

ENV PATH="/usr/local/bin:${PATH}"

ADD . /code
WORKDIR /code

RUN pip install --upgrade pip && pip install -r requirements.txt

RUN chmod +rwx /etc/ssl/openssl.cnf \
    && sed -i 's/TLSv1.2/TLSv1/g' /etc/ssl/openssl.cnf \
    && sed -i 's/SECLEVEL=2/SECLEVEL=1/g' /etc/ssl/openssl.cnf

ENV LISTEN_PORT=5000 \
    UWSGI_INI=/code/uwsgi/uwsgi.ini \
    PYTHONPATH=/code/app \
    NGINX_WORKER_PROCESSES=auto \
    NGINX_WORKER_CONNECTIONS=65535 \
    UWSGI_PROCESSES=1 \
    UWSGI_CHEAPER=0

EXPOSE 5000
EXPOSE 1717
