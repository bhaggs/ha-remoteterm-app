# Upstream RemoteTerm image tag to track.
# Update REMOTETERM_VERSION here (and in config.yaml) when the upstream releases a new version.
ARG REMOTETERM_VERSION=latest
FROM docker.io/jkingsman/remoteterm-meshcore:${REMOTETERM_VERSION}

# Install jq for parsing Home Assistant add-on options.json
RUN apt-get update \
    && apt-get install -y --no-install-recommends jq \
    && rm -rf /var/lib/apt/lists/*

COPY run.sh /run.sh
RUN chmod a+x /run.sh

CMD ["/run.sh"]
