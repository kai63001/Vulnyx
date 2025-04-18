#!/bin/bash

# Vulnyx Scanner Build Script
# This script builds the Vulnyx Scanner Go application

set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

echo -e "${BLUE}Building Vulnyx Scanner...${NC}"

# Check Go installation
if ! command -v go &> /dev/null; then
    echo -e "${RED}Error: Go is not installed or not in PATH.${NC}"
    echo "Please install Go from https://golang.org/dl/"
    exit 1
fi

# Make sure dependencies are installed
echo -e "${BLUE}Installing dependencies...${NC}"
go mod download

# Build the application
echo -e "${BLUE}Compiling...${NC}"
go build -o vulnyx main.go

if [ $? -eq 0 ]; then
    echo -e "${GREEN}Build successful!${NC}"
    echo -e "${GREEN}You can now run the application with ./vulnyx${NC}"
else
    echo -e "${RED}Build failed!${NC}"
    exit 1
fi
