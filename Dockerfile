# ? OpenCV Dependencies, probably needed in all images
FROM python:3.11-slim as base

# Install system dependencies for OpenCV
RUN apt-get update && apt-get install -y \
  ffmpeg \
  libsm6 \
  libxext6 \
  libxrender-dev

# ? Python Server Builder
FROM base as backend-builder

# Install Poetry and project dependencies
# https://medium.com/@albertazzir/blazing-fast-python-docker-builds-with-poetry-a78a66f5aed0
RUN pip install poetry
ENV POETRY_NO_INTERACTION=1 \
  POETRY_VIRTUALENVS_IN_PROJECT=1 \
  POETRY_VIRTUALENVS_CREATE=1 \
  POETRY_CACHE_DIR=/tmp/poetry_cache

WORKDIR /app

# Copy source files
COPY pyproject.toml ./

RUN --mount=type=cache,target=$POETRY_CACHE_DIR poetry install --without dev --no-root

# Needed by Astro Builder
COPY static.py ./
RUN poetry run python3 static.py


# ? Astro Builder
FROM node:20-alpine as frontend-builder

WORKDIR /app

COPY package.json pnpm-lock.yaml* ./
RUN corepack enable
RUN pnpm install --frozen-lockfile

COPY astro.config.mjs svelte.config.js tailwind.config.mjs tsconfig.json ./
COPY src ./src
COPY public ./public

COPY --from=backend-builder /app/public/frames ./public/frames
COPY --from=backend-builder /app/src/data.g.json ./src/data.g.json

RUN pnpm build

# ? Runner
FROM base as runner

USER nobody
WORKDIR /app

ENV VIRTUAL_ENV=/app/.venv \
  PATH="/app/.venv/bin:$PATH"

COPY --from=backend-builder --chown=nobody:nobody ${VIRTUAL_ENV} ${VIRTUAL_ENV}

COPY --chown=nobody:nobody server ./server
COPY --from=frontend-builder --chown=nobody:nobody /app/dist ./dist

EXPOSE 3131
CMD ["python", "-u", "server/server.py"]
