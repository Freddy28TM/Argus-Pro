# Stage 1: Build/Compile
FROM python:3.11-slim as builder
RUN apt-get update && apt-get install -y clang make

WORKDIR /build
COPY . .
# Compile the Clang engine
RUN clang src/native/reverser.c -o modules/reversing/reverser

# Stage 2: Production
FROM python:3.11-slim
WORKDIR /app

# Copy only what we need
COPY --from=builder /build /app
RUN pip install --no-cache-dir -r requirements.txt

# Run as non-root user for security
RUN useradd -m argususer
USER argususer

ENTRYPOINT ["python", "main.py"]
