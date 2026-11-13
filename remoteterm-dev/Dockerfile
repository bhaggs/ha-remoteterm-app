# Development build: tracks the latest upstream `main` via the `edge` image,
# which upstream publishes on every push to main. Not for production use.
#
# Upstream: https://github.com/statico/remoteterm-meshcore
FROM ghcr.io/statico/remoteterm-meshcore:edge

# Install jq (options parsing) and curl (Supervisor API + REST bootstrap)
RUN apt-get update \
    && apt-get install -y --no-install-recommends jq curl \
    && rm -rf /var/lib/apt/lists/*

# Zero the iOS safe-area padding when RemoteTerm runs inside Home Assistant's
# frame (see ha-frame-safe-area.html). Fails the build if upstream's
# index.html no longer has the expected <meta charset> tag.
COPY ha-frame-safe-area.html /tmp/ha-frame-safe-area.html
RUN sed -i '/<meta charset=/r /tmp/ha-frame-safe-area.html' /app/frontend/dist/index.html \
    && grep -q 'ha-app: in-frame safe-area fix' /app/frontend/dist/index.html \
    && rm /tmp/ha-frame-safe-area.html

COPY run.sh /run.sh
RUN chmod a+x /run.sh

CMD ["/run.sh"]
