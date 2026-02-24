FROM nikolaik/python-nodejs:python3.10-nodejs20

RUN apt-get update \
    && apt-get install -y --no-install-recommends ffmpeg git zip curl \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

RUN which node && node --version && npm --version

ENV PATH="/usr/local/bin:/usr/bin:${PATH}"
ENV NODE_PATH="/usr/local/lib/node_modules"

RUN mkdir -p /root/.config/yt-dlp && \
    printf "# yt-dlp configuration - enable Node.js JavaScript runtime\njs-runtimes=node\nno-check-for-updates\n" > /root/.config/yt-dlp/config.txt

COPY . /app/
WORKDIR /app/
RUN pip3 install --no-cache-dir -U -r requirements.txt

CMD bash start
