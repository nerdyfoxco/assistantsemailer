# Stage 1: Build
FROM node:20-alpine AS builder

WORKDIR /app

# Copy Foundation (Shared)
COPY foundation ./foundation

# Copy Brain Source
COPY chapters/brain/topic-orchestration ./chapters/brain/topic-orchestration

WORKDIR /app/chapters/brain/topic-orchestration

RUN npm install
RUN npx tsc -p tsconfig.build.json

# Stage 2: Runner
FROM node:20-alpine AS runner

WORKDIR /app

# Copy manifest for production install
COPY chapters/brain/topic-orchestration/package.json ./package.json
RUN npm install --only=production

# Copy compiled artifacts
# Note: tsc with relative imports above rootDir will output the full structure
COPY --from=builder /app/chapters/brain/topic-orchestration/dist ./dist

ENV PORT=3000
EXPOSE 3000

# The path logic:
# Common root is /app.
# Source is /app/chapters/brain/topic-orchestration/src/index.ts
# Output is /app/chapters/brain/topic-orchestration/dist/chapters/brain/topic-orchestration/src/index.js
# Wait, if output is ./dist relative to /app/chapters/brain/topic-orchestration
# Then inside dist we have:
#   foundation/...
#   chapters/brain/topic-orchestration/src/...
#
# So we need to be careful with the CMD.
# Let's inspect the structure in the builder or just try the deep path.
# A safer bet is to copy *everything* from dist.

CMD ["node", "dist/chapters/brain/topic-orchestration/src/index.js"]
