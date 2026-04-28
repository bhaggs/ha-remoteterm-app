# ── test/upstream-ha branch ──────────────────────────────────────────────────
# Builds from the upstream `ha` branch source to test MQTT Discovery support.
# This branch is NOT for production use.
#
# When the upstream merges ha → main and cuts a release, this branch should be
# retired and main reverted to the simpler pre-built-image approach.
# ─────────────────────────────────────────────────────────────────────────────

# Stage 1: Clone upstream ha branch and build the React frontend
FROM node:20-slim AS frontend-builder

RUN apt-get update \
    && apt-get install -y --no-install-recommends git ca-certificates \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /build
RUN git clone --branch main --depth 1 \
    https://github.com/jkingsman/Remote-Terminal-for-MeshCore.git .

WORKDIR /build/frontend
# Apply local patch for iOS keyboard overlay fix (pending upstream acceptance)
COPY MessageInput.tsx src/components/MessageInput.tsx
RUN npm ci
RUN npm run build

# Stage 2: Python runtime (mirrors upstream Dockerfile)
FROM python:3.12-slim

WORKDIR /app

# Install uv
COPY --from=ghcr.io/astral-sh/uv:latest /uv /usr/local/bin/uv

# Copy dependency files from cloned source for layer caching
COPY --from=frontend-builder /build/pyproject.toml /build/uv.lock ./
RUN uv sync --frozen --no-dev

# Copy application code and assets
COPY --from=frontend-builder /build/app/ ./app/
COPY --from=frontend-builder /build/LICENSES.md ./
COPY --from=frontend-builder /build/frontend/dist ./frontend/dist

RUN mkdir -p /app/data

# Install jq (options parsing) and curl (Supervisor API + REST bootstrap)
RUN apt-get update \
    && apt-get install -y --no-install-recommends jq curl \
    && rm -rf /var/lib/apt/lists/*

COPY run.sh /run.sh
RUN chmod a+x /run.sh

EXPOSE 8000
CMD ["/run.sh"]
