# Frontend Dockerfile
FROM node:18-alpine

WORKDIR /app

# Copy package files
COPY package.json package-lock.json ./

# Install dependencies
RUN npm ci

# Copy source code
COPY . .

# Build application (optional, for production)
# RUN npm run build

# Expose port (Vite dev server)
EXPOSE 5173

# Start dev server
CMD ["npm", "run", "dev"]
