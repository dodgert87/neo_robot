FROM python:3.12-slim

# Set the working directory
WORKDIR /usr/share/nginx/html

# Copy the frontend files
COPY . .

# Expose the port for the static file server
EXPOSE 8090

# Use Python's built-in HTTP server to serve static files
CMD ["python3", "-m", "http.server", "8090"]