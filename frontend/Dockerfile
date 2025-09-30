# Frontend Dockerfile for development
FROM node:18-alpine

# Create app directory
WORKDIR /app

# Install dependencies first for better cache
COPY package.json package-lock.json* ./
RUN npm install --silent

# Copy rest of the sources
COPY . .

EXPOSE 5173

# Start dev server and listen on all interfaces
CMD ["npm", "run", "dev", "--", "--host", "0.0.0.0", "--port", "5173"]
