FROM node:20-alpine AS base
WORKDIR /app

FROM base AS deps
COPY api-server/package*.json ./
RUN npm ci --omit=dev

FROM base AS build
COPY api-server/package*.json ./
RUN npm ci
COPY api-server/tsconfig.json ./tsconfig.json
COPY api-server/src ./src
RUN npm run build

FROM base AS runner
ENV NODE_ENV=production
WORKDIR /app
COPY --from=build /app/dist ./dist
COPY --from=deps /app/node_modules ./node_modules
COPY api-server/package*.json ./
EXPOSE 4000
CMD ["node", "dist/index.js"]
