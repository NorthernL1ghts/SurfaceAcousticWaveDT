# Minimum CMake version required
cmake_minimum_required(VERSION 3.16)

project(SurfaceAcousticWaveDT VERSION 1.0 LANGUAGES CXX)

set(CMAKE_CXX_STANDARD 20)
set(CMAKE_CXX_STANDARD_REQUIRED ON)

set(CMAKE_CONFIGURATION_TYPES "Debug;Release;RelWithDebInfo;MinSizeRel" CACHE STRING "" FORCE)

# Platform-specific definitions
if(WIN32)
    add_definitions(-DSAW_DT_PLATFORM_WINDOWS)
elseif(APPLE)
    add_definitions(-DSAW_DT_PLATFORM_MACOS -DSAW_DT_PLATFORM_POSIX)
elseif(UNIX)
    add_definitions(-DSAW_DT_PLATFORM_LINUX -DSAW_DT_PLATFORM_POSIX)
endif()

# Vendor directory
set(VENDOR_DIR ${PROJECT_SOURCE_DIR}/vendor)

include(FetchContent)

# ---------------------------
# Fetch ImGui
# ---------------------------
FetchContent_Declare(
    ImGui
    GIT_REPOSITORY https://github.com/ocornut/imgui.git
    GIT_TAG docking  # or master
    SOURCE_DIR ${VENDOR_DIR}/imgui
)

# ---------------------------
# Fetch ImPlot
# ---------------------------
FetchContent_Declare(
    ImPlot
    GIT_REPOSITORY https://github.com/epezent/implot.git
    GIT_TAG master
    SOURCE_DIR ${VENDOR_DIR}/implot
)

# ---------------------------
# Fetch GLFW
# ---------------------------
FetchContent_Declare(
    GLFW
    GIT_REPOSITORY https://github.com/glfw/glfw.git
    GIT_TAG 3.4     # latest stable release
    SOURCE_DIR ${VENDOR_DIR}/glfw
)

# Make everything available
FetchContent_MakeAvailable(ImGui ImPlot GLFW)

# ---------------------------
# Gather project sources
# ---------------------------
file(GLOB_RECURSE SOURCES "src/*.cpp" "src/*.c" "src/*.hpp" "src/*.h")

if(NOT SOURCES)
    message(FATAL_ERROR "No source files found in the src/ directory!")
endif()

# ---------------------------
# ImGui sources
# ---------------------------
set(IMGUI_SOURCES
    ${VENDOR_DIR}/imgui/imgui.cpp
    ${VENDOR_DIR}/imgui/imgui_draw.cpp
    ${VENDOR_DIR}/imgui/imgui_widgets.cpp
    ${VENDOR_DIR}/imgui/imgui_tables.cpp
    ${VENDOR_DIR}/imgui/imgui_demo.cpp
    ${VENDOR_DIR}/imgui/backends/imgui_impl_glfw.cpp
    ${VENDOR_DIR}/imgui/backends/imgui_impl_opengl3.cpp
)

# ---------------------------
# ImPlot sources
# ---------------------------
set(IMPLOT_SOURCES
    ${VENDOR_DIR}/implot/implot.cpp
    ${VENDOR_DIR}/implot/implot_items.cpp
    ${VENDOR_DIR}/implot/implot_demo.cpp
)

# ---------------------------
# Executable
# ---------------------------
add_executable(SurfaceAcousticWaveDT
    ${SOURCES}
    ${IMGUI_SOURCES}
    ${IMPLOT_SOURCES}
)

# ---------------------------
# Include paths
# ---------------------------
target_include_directories(SurfaceAcousticWaveDT PRIVATE
    src
    ${VENDOR_DIR}/imgui
    ${VENDOR_DIR}/implot
    ${VENDOR_DIR}/glfw/include
)

# ---------------------------
# Link libraries
# ---------------------------
find_package(OpenGL REQUIRED)
target_link_libraries(SurfaceAcousticWaveDT PRIVATE OpenGL::GL glfw)

# ---------------------------
# Configurations
# ---------------------------
set_target_properties(SurfaceAcousticWaveDT PROPERTIES
    DEBUG_POSTFIX "_debug"
    RELEASE_POSTFIX "_release"
)

# Debug
target_compile_definitions(SurfaceAcousticWaveDT PRIVATE SAW_DT_DEBUG)
set_target_properties(SurfaceAcousticWaveDT PROPERTIES
    COMPILE_FLAGS "-g"
    CMAKE_BUILD_TYPE Debug
)

# Release
target_compile_definitions(SurfaceAcousticWaveDT PRIVATE SAW_DT_RELEASE)
set_target_properties(SurfaceAcousticWaveDT PROPERTIES
    COMPILE_FLAGS "-O3"
    CMAKE_BUILD_TYPE Release
)

# Distribution
target_compile_definitions(SurfaceAcousticWaveDT PRIVATE SAW_DT_DIST)
set_target_properties(SurfaceAcousticWaveDT PROPERTIES
    COMPILE_FLAGS "-O3 -DNDEBUG"
    CMAKE_BUILD_TYPE Release
)

# Platform-specific
if(WIN32)
    target_link_libraries(SurfaceAcousticWaveDT PRIVATE opengl32)
elseif(APPLE)
    find_library(COCOA_LIBRARY Cocoa)
    find_library(METAL_LIBRARY Metal)
    find_library(QUARTZCORE_LIBRARY QuartzCore)
    target_link_libraries(SurfaceAcousticWaveDT PRIVATE ${COCOA_LIBRARY} ${METAL_LIBRARY} ${QUARTZCORE_LIBRARY})
elseif(UNIX)
    find_package(Threads REQUIRED)
    target_link_libraries(SurfaceAcousticWaveDT PRIVATE Threads::Threads)
endif()
