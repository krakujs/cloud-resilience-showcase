FROM golang:1.22-alpine AS builder

# Set working directory
WORKDIR /app

# Install git and necessary tools
RUN apk add --no-cache git

# Copy go mod and sum files
COPY go.mod go.sum ./

# Download dependencies
RUN go mod download

# Copy the source code
COPY . .

# Build the application
RUN CGO_ENABLED=0 GOOS=linux go build -a -installsuffix cgo -o chaos-engineering ./src/main.go

# Final stage
FROM alpine:latest

# Install CA certificates
RUN apk --no-cache add ca-certificates

WORKDIR /root/

# Copy the pre-built binary from the builder stage
COPY --from=builder /app/chaos-engineering .

# Expose the service port
EXPOSE 8080

# Command to run the executable
CMD ["./chaos-engineering"]