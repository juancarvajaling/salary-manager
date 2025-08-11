# Development Environment Setup

This document explains how to set up the **production-parity development environment** for the Salary Manager project using **host-based development** with containerized runtime services.

## Prerequisites

- **Docker** and **Docker Compose** installed on your machine
- **SAM CLI** installed (`pip install aws-sam-cli`)
- **Python 3.12+** and **Poetry** for dependency management
- **AWS CLI** configured with your credentials (optional for local development)

## Quick Start

### Option 1: One-Command Setup (Recommended)

```bash
# Setup once (installs dependencies, builds containers)
./scripts/dev-setup.sh

# Start everything automatically
./scripts/start-dev.sh
```

✅ **That's it!** The script will:
- Start Docker containers (gateway + static server)
- Build and start SAM Local automatically
- Show you all access URLs
- Monitor logs in real-time

### Option 2: Manual Setup (Advanced)

```bash
# Build the development containers
docker-compose -f docker/docker-compose.yml build

# Terminal 1: Start containers (frontend + routing)
docker-compose -f docker/docker-compose.yml up gateway static

# Terminal 2: Start SAM Local on host (Lambda functions)
sam build -t infrastructure/template.yaml && sam local start-api --port 3000 --host 0.0.0.0 --profile my-own --region us-east-1
```

> **⚠️ Important**: Both options maintain **production parity** by using the nginx gateway to route requests exactly like AWS API Gateway does in production. This ensures your development environment mirrors your production architecture perfectly.

## Development Workflow

> **📝 Important SAM Local Note**: Always run `sam build -t infrastructure/template.yaml` before starting `sam local start-api`. The build step installs Python dependencies (openpyxl, workalendar) that are required for the Lambda function to work. The start-api command should **NOT** use the `-t` flag to ensure it uses the built version with dependencies.

### Available Services

| Service | Port | Purpose | URL |
|---------|------|---------|-----|
| `gateway` | 8000 | **Main App** - Nginx reverse proxy (simulates API Gateway) | **http://localhost:8000** |
| SAM Local (host) | 3000 | Real SAM Local API with dependencies | http://localhost:3000 |
| `static` | 8080 | Static file server (simulates S3) | http://localhost:8080 |

### Starting Services

```bash
# Start all services (recommended)
docker-compose -f docker/docker-compose.yml up

# Start containers (frontend + routing)
docker-compose -f docker/docker-compose.yml up gateway static

# In separate terminal: Start SAM Local on host
sam build -t infrastructure/template.yaml && sam local start-api --port 3000 --profile my-own --region us-east-1

# Start only the frontend
docker-compose -f docker/docker-compose.yml up static

# For development tools, use host machine directly
poetry shell  # Activate Python environment
```

### Working with the Application

**🚀 Streamlined Development Experience:**

1. **Start Development Environment**:
   ```bash
   ./scripts/start-dev.sh
   ```
   
   The script automatically:
   - ✅ Checks prerequisites (Docker, SAM CLI)
   - ✅ Starts Docker containers (gateway + static)
   - ✅ Builds and starts SAM Local
   - ✅ Shows access URLs and status
   - ✅ Monitors logs in real-time

2. **Access Your Application**:
   - 🌐 **Main App**: http://localhost:8000 (exactly like production)
   - 📄 **Static files**: http://localhost:8080 (for development)
   - 🔧 **SAM Local API**: http://localhost:3000 (direct Lambda access)

**📝 Development Workflow:**

1. **Frontend Development**:
   - Edit files in `frontend/` directory
   - Changes are reflected immediately at http://localhost:8000

2. **Backend Development**:
   - Edit Python files in `backend/` directory  
   - Edit `infrastructure/template.yaml` for infrastructure changes
   - SAM Local automatically reloads when files change
   - Check `sam-local.log` for detailed Lambda logs

3. **Single Source of Truth**:
   - ✅ Only `infrastructure/template.yaml` defines your architecture
   - ✅ No separate development configuration to maintain
   - ✅ Guaranteed production parity
   - ✅ Automatic sync with infrastructure changes

## Development Commands

All development happens on your **host machine**:

```bash
# SAM Local operations
sam build -t infrastructure/template.yaml  # Build Lambda function
sam validate -t infrastructure/template.yaml  # Validate template
sam local invoke SalaryManagerFunction  # Test function directly

# Python development (host machine)
poetry add <package-name>    # Add Python dependencies
poetry run pytest           # Run tests (if you have them)
poetry run black backend/  # Format code
poetry run flake8 backend/ # Lint code

# Direct Lambda testing
python backend/lambda_function.py  # Test Lambda locally

# Container management
docker-compose -f docker/docker-compose.yml up gateway static -d  # Start services
docker-compose -f docker/docker-compose.yml logs -f              # Monitor logs
docker-compose -f docker/docker-compose.yml down                  # Stop services
```

**📝 Development Notes:**
- ✅ **Host-based development**: No container complexity for coding
- ✅ **Containers for runtime**: Only nginx gateway and static server
- ✅ **SAM Local on host**: Direct Lambda execution without Docker-in-Docker
- ✅ **Native tooling**: Use your preferred IDE and tools directly

## File Structure

```
salary-manager/
├── backend/                 # Lambda function code
│   ├── lambda_function.py   # Main handler
│   ├── requirements.txt     # Lambda dependencies
│   └── utils/              # Utility modules
├── frontend/               # Frontend files
│   ├── index.html
│   └── script.js
├── infrastructure/         # AWS CloudFormation/SAM
│   ├── template.yaml       # SAM template
│   └── samconfig.toml      # SAM configuration
├── docker/                 # Container configurations
│   ├── docker-compose.yml  # Container orchestration
│   ├── Dockerfile          # Static server image
│   └── nginx.conf          # Reverse proxy config
├── docs/                   # Documentation
├── scripts/                # Development tools
└── .vscode/               # Editor settings
```

## Development Tips

### 1. Live Reloading
- **Frontend**: Changes to HTML/CSS/JS files are immediately visible
- **Backend**: SAM CLI automatically detects changes to Python files

### 2. Debugging
```bash
# View all container logs
docker-compose -f docker/docker-compose.yml logs

# View gateway logs (nginx reverse proxy)
docker-compose -f docker/docker-compose.yml logs gateway

# View static server logs
docker-compose -f docker/docker-compose.yml logs static

# View SAM Local logs (Lambda execution)
tail -f sam-local.log

# Real-time log monitoring (automatic with start-dev.sh)
docker-compose -f docker/docker-compose.yml logs -f gateway static
```

### 3. AWS Configuration
- Uses the "my-own" AWS profile with your credentials
- Default region is set to `us-east-1` for SAM Local
- Profile-based authentication avoids SSO token issues

### 4. Adding Dependencies

**Python Dependencies (for Lambda)**:
```bash
# Inside container
poetry add <package-name>

# Update requirements.txt for Lambda
poetry export --without-hashes --format=requirements.txt > backend/requirements.txt
```

## Testing Excel File Processing

To test the salary calculation functionality:

1. Create an Excel file with two sheets:
   - **"empleados"** sheet: columns A (ID), B (Name), C (Salary)
   - **"horas"** sheet: columns A (Employee ID), B (Date), C (Hours)

2. Upload through the web interface at http://localhost:8000

3. The application will process the file and return a salary calculation

## Troubleshooting

### Common Issues

**🔧 "Port already in use" errors:**
```bash
# Check what's using the ports
lsof -i :3000  # SAM Local
lsof -i :8000  # Gateway
lsof -i :8080  # Static server

# Stop existing SAM Local process
pkill -f "sam local start-api"

# Stop Docker containers
docker-compose -f docker/docker-compose.yml down
```

**🐳 Container issues:**
```bash
# Clean rebuild
docker-compose -f docker/docker-compose.yml down
docker-compose -f docker/docker-compose.yml build --no-cache

# Remove orphaned containers
docker-compose -f docker/docker-compose.yml down --remove-orphans
```

**🔧 SAM Local issues:**
```bash
# Check SAM Local logs
tail -f sam-local.log

# Restart SAM Local manually
pkill -f "sam local start-api"
sam build -t infrastructure/template.yaml && sam local start-api --port 3000 --host 0.0.0.0 --profile my-own --region us-east-1

# Check if SAM Local is responding
curl http://localhost:3000/calculate-salary -X OPTIONS
```

**🔑 AWS credentials (optional for local development):**
```bash
# Configure AWS on host machine
aws configure

# Check AWS configuration
aws sts get-caller-identity
```

**🐍 Python environment issues:**
```bash
# Reset Python environment
poetry env remove python
poetry install --no-root
pip install -r backend/requirements.txt
```

## VS Code Setup (Host-Based)

**Recommended Extensions:**
```bash
# Install VS Code extensions
code --install-extension ms-python.python
code --install-extension amazonwebservices.aws-toolkit-vscode
code --install-extension ms-python.black-formatter
code --install-extension ms-python.flake8
```

**Workspace Settings** (`.vscode/settings.json`):
```json
{
  "python.defaultInterpreterPath": "poetry env info -p",
  "python.linting.enabled": true,
  "python.linting.flake8Enabled": true,
  "python.formatting.provider": "black"
}
```

**Benefits of Host Development:**
- ✅ **Native performance**: No container overhead
- ✅ **Full IDE support**: Complete IntelliSense and debugging
- ✅ **Direct file access**: No sync delays
- ✅ **Simplified setup**: Standard Python development workflow

## Deployment Testing

To test deployment without actually deploying:

```bash
# Validate your template (should always pass)
sam validate -t infrastructure/template.yaml

# Package for deployment (dry run - requires S3 bucket)
sam package --s3-bucket your-deployment-bucket --output-template-file packaged.yaml

# Test deployment template (dry run)
sam deploy --template-file packaged.yaml --stack-name test-stack --no-execute-changeset

# Direct Lambda testing (bypass API Gateway)
sam local invoke SalaryManagerFunction --event test-event.json
```

**📋 Deployment Checklist:**
- ✅ `sam validate` passes
- ✅ All Lambda functions work in SAM Local  
- ✅ Frontend uploads Excel files successfully
- ✅ End-to-end workflow works at http://localhost:8000
- ✅ No errors in `sam-local.log`

## Next Steps

- Set up CI/CD pipeline for automatic testing
- Add unit tests for salary calculation logic
- Implement integration tests for the full workflow
- Set up monitoring and logging for production deployment 