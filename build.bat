@echo off
REM Optimized Docker build script for production (Windows)

setlocal enabledelayedexpansion

REM Configuration
set IMAGE_NAME=ghcr.io/sznaskme/microservice-a/orders
set VERSION=%1
if "%VERSION%"=="" set VERSION=latest
set DOCKERFILE_PATH=services/orders/Dockerfile
set BUILD_CONTEXT=services/orders

echo [INFO] Starting optimized Docker build...
echo [INFO] Image: %IMAGE_NAME%:%VERSION%
echo [INFO] Context: %BUILD_CONTEXT%

REM Validate environment
if not exist "%DOCKERFILE_PATH%" (
    echo [ERROR] Dockerfile not found at %DOCKERFILE_PATH%
    exit /b 1
)

if not exist "%BUILD_CONTEXT%\requirements.txt" (
    echo [ERROR] requirements.txt not found in %BUILD_CONTEXT%
    exit /b 1
)

REM Create buildx builder if not exists
echo [INFO] Setting up buildx builder...
docker buildx create --name microservice-builder --use 2>nul || echo Builder already exists

REM Build multi-platform image
echo [INFO] Building multi-platform image...
docker buildx build ^
    --platform linux/amd64,linux/arm64 ^
    --cache-from type=registry,ref=%IMAGE_NAME%:cache ^
    --cache-to type=registry,ref=%IMAGE_NAME%:cache,mode=max ^
    -f %DOCKERFILE_PATH% ^
    -t %IMAGE_NAME%:%VERSION% ^
    -t %IMAGE_NAME%:latest ^
    --push ^
    %BUILD_CONTEXT%

if %errorlevel% equ 0 (
    echo [INFO] ✅ Build completed successfully!
    echo [INFO] Images pushed:
    echo [INFO]   - %IMAGE_NAME%:%VERSION%
    echo [INFO]   - %IMAGE_NAME%:latest
) else (
    echo [ERROR] ❌ Build failed!
    exit /b 1
)
