import platform

SAW_VERSION = "2025.0.1"

# Build Configuration
import os

if os.getenv("SAW_DEBUG"):
    SAW_BUILD_CONFIG_NAME = "Debug"
elif os.getenv("SAW_RELEASE"):
    SAW_BUILD_CONFIG_NAME = "Release"
elif os.getenv("SAW_DIST"):
    SAW_BUILD_CONFIG_NAME = "Dist"
else:
    raise RuntimeError("Undefined build configuration")


system_platform = platform.system()
if system_platform == "Windows":
    SAW_BUILD_PLATFORM_NAME = "Windows x64"
elif system_platform == "Linux":
    SAW_BUILD_PLATFORM_NAME = "Linux"
else:
    SAW_BUILD_PLATFORM_NAME = "Unknown"

SAW_VERSION_LONG = f"SAW {SAW_VERSION} ({SAW_BUILD_PLATFORM_NAME} {SAW_BUILD_CONFIG_NAME})"


# Example usage
if __name__ == "__main__":
    print(SAW_VERSION_LONG)
