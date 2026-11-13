# Upstream RemoteTerm image tag to build on. The build workflow passes the
# version from config.yaml so each app release pins the matching upstream
# release; the `latest` default only applies to local builds.
#
# Upstream: https://github.com/statico/remoteterm-meshcore (a continuation of
# the paused jkingsman/Remote-Terminal-for-MeshCore project).
ARG REMOTETERM_VERSION=latest
FROM ghcr.io/statico/remoteterm-meshcore:${REMOTETERM_VERSION}

# Install jq (options parsing) and curl (Supervisor API + REST bootstrap)
RUN apt-get update \
    && apt-get install -y --no-install-recommends jq curl \
    && rm -rf /var/lib/apt/lists/*

COPY run.sh /run.sh
RUN chmod a+x /run.sh

CMD ["/run.sh"]
