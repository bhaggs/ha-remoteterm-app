# Development build: tracks the latest upstream `main` via the `edge` image,
# which upstream publishes on every push to main. Not for production use.
#
# Upstream: https://github.com/statico/remoteterm-meshcore
FROM ghcr.io/statico/remoteterm-meshcore:edge

# Install jq (options parsing) and curl (Supervisor API + REST bootstrap)
RUN apt-get update \
    && apt-get install -y --no-install-recommends jq curl \
    && rm -rf /var/lib/apt/lists/*

COPY run.sh /run.sh
RUN chmod a+x /run.sh

CMD ["/run.sh"]
