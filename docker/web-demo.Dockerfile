FROM node:20-alpine AS base
WORKDIR /app

FROM base AS deps
COPY web-demo/package*.json ./
RUN npm ci

FROM base AS build
COPY web-demo/package*.json ./
RUN npm ci
COPY web-demo/tsconfig.json ./tsconfig.json 2>/dev/null || true
COPY web-demo/vite.config.ts ./vite.config.ts
COPY web-demo/index.html ./index.html
COPY web-demo/src ./src
RUN npm run build

FROM base AS runner
ENV NODE_ENV=production
WORKDIR /app
COPY --from=build /app/dist ./dist
COPY --from=deps /app/node_modules ./node_modules
COPY web-demo/package*.json ./
EXPOSE 5173
CMD ["npm", "run", "dev", "--", "--host", "0.0.0.0", "--port", "5173"]
