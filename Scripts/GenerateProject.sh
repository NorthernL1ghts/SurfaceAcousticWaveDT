#!/bin/bash

echo "Generating project files with CMake..."

# Set the build directory (can be set to any directory you like)
BUILD_DIR="build"

# Create the build directory if it doesn't exist
if [ ! -d "$BUILD_DIR" ]; then
    mkdir "$BUILD_DIR"
fi

# Navigate to the build directory
cd "$BUILD_DIR"

# Run CMake to generate the build files
cmake ..

# Check if the CMake command was successful
if [ $? -ne 0 ]; then
    echo "Error: CMake generation failed."
    exit 1
fi

echo "Generation complete. You can now build the project."
