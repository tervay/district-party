# Use the official Node.js 18 image as a base
FROM node:18

# Set the working directory in the container
WORKDIR /app/frontend

# Copy the package.json and package-lock.json files
COPY package*.json ./

# Install pnpm
RUN npm install -g pnpm

# Install dependencies
RUN pnpm install

# Copy the remaining files to the working directory
COPY . .

# Expose port 3000
EXPOSE 3000

CMD ["pnpm", "start"]
