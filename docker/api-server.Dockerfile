FROM node:20-alpine AS build
WORKDIR /app
COPY api-server/package.json api-server/tsconfig.json ./
RUN npm install
COPY api-server/src ./src
RUN npm run build

FROM node:20-alpine
WORKDIR /app
COPY --from=build /app/dist ./dist
COPY api-server/package.json ./
RUN npm install --omit=dev
EXPOSE 4000
CMD ["node", "dist/index.js"]
