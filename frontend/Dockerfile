# Use the official Node.js 18 image as a base
FROM node:18

# Set the working directory in the container
WORKDIR /app/frontend

# Copy the package.json and package-lock.json files
COPY package*.json ./
COPY . .

# Install pnpm
RUN npm install -g pnpm

# Install dependencies
RUN pnpm install
RUN npm install -g serve

# Expose port 3000
EXPOSE 3000

CMD [ "pnpm", "start" ]