#!/bin/bash

# Development setup script for Salary Manager

set -e

echo "🚀 Setting up Salary Manager development environment..."

# Function to check if command exists
command_exists() {
    command -v "$1" >/dev/null 2>&1
}

# Check Docker installation
if ! command_exists docker; then
    echo "❌ Docker is not installed. Please install Docker first."
    echo "Visit: https://docs.docker.com/get-docker/"
    exit 1
fi

# Check Docker Compose installation
if ! command_exists docker-compose; then
    echo "❌ Docker Compose is not installed. Please install Docker Compose first."
    echo "Visit: https://docs.docker.com/compose/install/"
    exit 1
fi

echo "✅ Docker and Docker Compose are installed"

# Build the development container
echo "🔨 Building development container..."
docker-compose -f docker/docker-compose.yml build

echo "✅ Development container built successfully"

# Create AWS credentials directory if it doesn't exist
if [ ! -d "$HOME/.aws" ]; then
    echo "📁 Creating AWS credentials directory..."
    mkdir -p "$HOME/.aws"
    echo "⚠️  Don't forget to configure your AWS credentials:"
    echo "   - AWS Access Key ID"
    echo "   - AWS Secret Access Key"
    echo "   - Default region (us-east-2)"
fi

echo "✅ Development environment setup complete!"
echo ""
echo "🎉 You can now start developing with:"
echo "   ./scripts/start-dev.sh         # Recommended: Start containers + instructions"
echo "   docker-compose up gateway static  # Start containers only"
echo "   docker-compose up dev          # Interactive development shell"
echo ""
echo "⚠️  IMPORTANT: For full development, you need to run SAM Local separately:"
echo "   In another terminal: sam build && sam local start-api --port 3000"
echo ""
echo "🌐 Access points:"
echo "   🌐 Main App (like production): http://localhost:8000"
echo "   📄 Static files only:         http://localhost:8080"
echo "   🔧 SAM Local (host):          http://localhost:3000"
echo ""
echo "📝 For VS Code users: Install Python and AWS Toolkit extensions for the best experience" 