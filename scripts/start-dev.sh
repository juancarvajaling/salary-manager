#!/bin/bash

# Start development environment script - Production-Parity Setup

echo "🚀 Starting Salary Manager development environment..."
echo ""

# Function to handle cleanup on exit
cleanup() {
    echo ""
    echo "🛑 Stopping development environment..."
    docker-compose down
    
    # Check if SAM Local is running and offer to stop it
    if pgrep -f "sam local start-api" > /dev/null; then
        echo "⚠️  SAM Local is still running. To stop it, run:"
        echo "   pkill -f 'sam local start-api'"
    fi
    exit 0
}

# Set up trap for cleanup
trap cleanup SIGINT SIGTERM

# Check if Docker is running
if ! docker info > /dev/null 2>&1; then
    echo "❌ Docker is not running. Please start Docker and try again."
    exit 1
fi

# Check if SAM CLI is installed
if ! command -v sam > /dev/null 2>&1; then
    echo "❌ SAM CLI is not installed. Please install it first:"
    echo "   pip install aws-sam-cli"
    exit 1
fi

echo "✅ Prerequisites check passed"
echo ""

# Start containers in background
echo "🐳 Starting Docker containers (gateway + static)..."
docker-compose up gateway static -d

if [ $? -ne 0 ]; then
    echo "❌ Failed to start Docker containers"
    exit 1
fi

echo "✅ Docker containers started successfully"
echo ""

# Check if SAM Local is already running
if pgrep -f "sam local start-api" > /dev/null; then
    echo "✅ SAM Local is already running"
else
    echo "🔧 Starting SAM Local..."
    echo "   Building SAM project..."
    
    if sam build; then
        echo "✅ SAM build successful"
        echo "🚀 Starting SAM Local API..."
        
        # Start SAM Local in background
        nohup sam local start-api --port 3000 --host 0.0.0.0 > sam-local.log 2>&1 &
        SAM_PID=$!
        
        # Wait a moment for SAM Local to start
        sleep 3
        
        # Check if SAM Local started successfully
        if kill -0 $SAM_PID 2>/dev/null; then
            echo "✅ SAM Local started successfully (PID: $SAM_PID)"
        else
            echo "❌ Failed to start SAM Local. Check sam-local.log for details."
            docker-compose down
            exit 1
        fi
    else
        echo "❌ SAM build failed"
        docker-compose down
        exit 1
    fi
fi

echo ""
echo "🎉 Development environment is ready!"
echo ""
echo "📍 Access Points:"
echo "  🌐 Main App (production-like): http://localhost:8000"
echo "  📄 Static files only:         http://localhost:8080"
echo "  🔧 SAM Local API:             http://localhost:3000"
echo ""
echo "📋 What's Running:"
echo "  ✅ nginx gateway (routes like API Gateway)"
echo "  ✅ Static file server (simulates S3)"
echo "  ✅ SAM Local (real Lambda execution)"
echo ""
echo "💡 Tips:"
echo "  • Upload Excel files at http://localhost:8000"
echo "  • Edit files in salary_manager/ or web_site/ - changes auto-reload"
echo "  • Check sam-local.log for Lambda function logs"
echo ""
echo "Press Ctrl+C to stop all services"

# Keep the script running and show logs
echo ""
echo "📊 Monitoring container logs (Ctrl+C to stop):"
docker-compose logs -f gateway static 