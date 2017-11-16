FROM python:3.6-jessie

RUN wget -q -O - https://dl-ssl.google.com/linux/linux_signing_key.pub | apt-key add - \
&& echo "deb [arch=amd64] http://dl.google.com/linux/chrome/deb/ stable main" >> /etc/apt/sources.list.d/google.list \
&& apt-get update \
&& apt-get install -y google-chrome-stable

RUN apt-get install -y bash nano vim \
&& pip install --upgrade pip \
&& pip install git+https://github.com/pilate/pyppeteer.git@dev
# && python -c 'from pyppeteer.chromium_downloader import download_chromium ; download_chromium()'

RUN useradd -ms /bin/bash feye
USER feye
COPY --chown=feye . /home/feye/
ENV CHROME_PATH /usr/bin/google-chrome-stable
WORKDIR /home/feye/
