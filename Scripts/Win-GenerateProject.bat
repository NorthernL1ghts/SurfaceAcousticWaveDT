@echo off
echo Generating Visual Studio project files with CMake...

:: Set the build directory (can be set to any directory you like)
set BUILD_DIR=build

:: Create the build directory if it doesn't exist
if not exist "%BUILD_DIR%" mkdir "%BUILD_DIR%"

:: Navigate to the build directory
cd "%BUILD_DIR%"

:: Run CMake to generate the Visual Studio solution
cmake -G "Visual Studio 17 2022" ..

:: Check if the CMake command was successful
if %errorlevel% neq 0 (
    echo Error: CMake generation failed.
    exit /b %errorlevel%
)

echo Generation complete. You can open the solution in Visual Studio now.
pause
