FROM node:18-alpine
WORKDIR /app
COPY package.json package-lock.json ./
RUN npm ci --omit=dev
COPY mock-bff.cjs ./
COPY batches.json ./
EXPOSE 8000
CMD ["node", "mock-bff.cjs"]
