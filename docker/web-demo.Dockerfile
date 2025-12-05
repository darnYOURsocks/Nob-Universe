FROM node:20-alpine AS build
WORKDIR /app
COPY web-demo/package.json web-demo/tsconfig.json web-demo/tsconfig.node.json web-demo/vite.config.ts ./
RUN npm install
COPY web-demo/src ./src
COPY web-demo/index.html ./
RUN npm run build

FROM node:20-alpine
WORKDIR /app
COPY --from=build /app/dist ./dist
COPY web-demo/package.json ./
RUN npm install --omit=dev
EXPOSE 5173
CMD ["npm", "run", "preview", "--", "--host", "0.0.0.0", "--port", "5173"]
