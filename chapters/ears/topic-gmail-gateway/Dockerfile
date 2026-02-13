# Stage 1: Build
FROM node:20-alpine AS builder

WORKDIR /app

# Copy Foundation (Shared)
COPY foundation ./foundation

# Copy Ears Source
COPY chapters/ears/topic-gmail-gateway ./chapters/ears/topic-gmail-gateway

WORKDIR /app/chapters/ears/topic-gmail-gateway

RUN npm install
RUN npm run build

# Stage 2: Runner
FROM node:20-alpine AS runner

WORKDIR /app

COPY chapters/ears/topic-gmail-gateway/package.json ./package.json
RUN npm install --only=production

COPY --from=builder /app/chapters/ears/topic-gmail-gateway/dist ./dist

ENV PORT=3002
EXPOSE 3002

CMD ["node", "dist/chapters/ears/topic-gmail-gateway/src/index.js"]
