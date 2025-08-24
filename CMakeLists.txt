# Minimum CMake version required
cmake_minimum_required(VERSION 3.16)

# Project name and language
project(SurfaceAcousticWaveDT VERSION 1.0 LANGUAGES CXX)

# Set the C++ standard to C++20
set(CMAKE_CXX_STANDARD 20)
set(CMAKE_CXX_STANDARD_REQUIRED ON)

# Define build types
set(CMAKE_CONFIGURATION_TYPES "Debug;Release;RelWithDebInfo;MinSizeRel" CACHE STRING "" FORCE)

# Platform-specific definitions (Windows, Linux, macOS, POSIX)
if(WIN32)
    add_definitions(-DSAW_DT_PLATFORM_WINDOWS)
elseif(APPLE)
    add_definitions(-DSAW_DT_PLATFORM_MACOS -DSAW_DT_PLATFORM_POSIX)
elseif(UNIX)
    add_definitions(-DSAW_DT_PLATFORM_LINUX -DSAW_DT_PLATFORM_POSIX)
endif()

# Define the project source files by globbing the src directory
file(GLOB_RECURSE SOURCES "src/*.cpp" "src/*.c" "src/*.hpp" "src/*.h")

# Check if any sources were found
if(NOT SOURCES)
    message(FATAL_ERROR "No source files found in the src/ directory!")
endif()

# Define the output directories
set(CMAKE_RUNTIME_OUTPUT_DIRECTORY ${CMAKE_BINARY_DIR}/Binaries)
set(CMAKE_ARCHIVE_OUTPUT_DIRECTORY ${CMAKE_BINARY_DIR}/Binaries)
set(CMAKE_LIBRARY_OUTPUT_DIRECTORY ${CMAKE_BINARY_DIR}/Binaries)
set(CMAKE_BINARY_DIR ${PROJECT_SOURCE_DIR}/Intermediates)

# Create the executable
add_executable(SurfaceAcousticWaveDT ${SOURCES})

# Include the source directory for header files
target_include_directories(SurfaceAcousticWaveDT PRIVATE src)

# Define the configurations (Debug, Release, Dist)
set_target_properties(SurfaceAcousticWaveDT PROPERTIES
    DEBUG_POSTFIX "_debug"
    RELEASE_POSTFIX "_release"
)

# Debug configuration
target_compile_definitions(SurfaceAcousticWaveDT PRIVATE SAW_DT_DEBUG)
set_target_properties(SurfaceAcousticWaveDT PROPERTIES
    COMPILE_FLAGS "-g"
    CMAKE_BUILD_TYPE Debug
)

# Release configuration
target_compile_definitions(SurfaceAcousticWaveDT PRIVATE SAW_DT_RELEASE)
set_target_properties(SurfaceAcousticWaveDT PROPERTIES
    COMPILE_FLAGS "-O3"
    CMAKE_BUILD_TYPE Release
)

# Distribution configuration
target_compile_definitions(SurfaceAcousticWaveDT PRIVATE SAW_DT_DIST)
set_target_properties(SurfaceAcousticWaveDT PROPERTIES
    COMPILE_FLAGS "-O3 -DNDEBUG"
    CMAKE_BUILD_TYPE Release
)

# Optional: Add platform-specific libraries or settings if needed
if(WIN32)
    # Windows-specific settings (e.g., link with a Windows library)
elseif(APPLE)
    # macOS-specific settings
elseif(UNIX)
    # Linux-specific settings
endif()
