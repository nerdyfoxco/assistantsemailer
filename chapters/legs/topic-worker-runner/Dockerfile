# Stage 1: Build
FROM node:20-alpine AS builder

WORKDIR /app

# Copy Foundation (Shared)
COPY foundation ./foundation

# Copy Legs Source
COPY chapters/legs/topic-worker-runner ./chapters/legs/topic-worker-runner

WORKDIR /app/chapters/legs/topic-worker-runner

RUN npm install
RUN npm run build

# Stage 2: Runner
FROM node:20-alpine AS runner

WORKDIR /app

COPY chapters/legs/topic-worker-runner/package.json ./package.json
RUN npm install --only=production

COPY --from=builder /app/chapters/legs/topic-worker-runner/dist ./dist

ENV PORT=3001
EXPOSE 3001

CMD ["node", "dist/chapters/legs/topic-worker-runner/src/index.js"]
