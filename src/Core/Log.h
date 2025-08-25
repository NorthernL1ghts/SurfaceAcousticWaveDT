#pragma once

#include <memory>

#include <spdlog/spdlog.h>

namespace SAW {

	class Log
	{
	public:
		static void Init();

		inline static std::shared_ptr<spdlog::logger>& GetCoreLogger() { return s_CoreLogger; }
		inline static std::shared_ptr<spdlog::logger>& GetClientLogger() { return s_ClientLogger; }
	private:
		static std::shared_ptr<spdlog::logger> s_CoreLogger;
		static std::shared_ptr<spdlog::logger> s_ClientLogger;
	};

}

// Core log macros
#define SAW_CORE_TRACE(...)    ::SAW::Log::GetCoreLogger()->trace(__VA_ARGS__)
#define SAW_CORE_INFO(...)     ::SAW::Log::GetCoreLogger()->info(__VA_ARGS__)
#define SAW_CORE_WARN(...)     ::SAW::Log::GetCoreLogger()->warn(__VA_ARGS__)
#define SAW_CORE_ERROR(...)    ::SAW::Log::GetCoreLogger()->error(__VA_ARGS__)
#define SAW_CORE_FATAL(...)    ::SAW::Log::GetCoreLogger()->fatal(__VA_ARGS__)

// Client log macros
#define SAW_TRACE(...)	      ::SAW::Log::GetClientLogger()->trace(__VA_ARGS__)
#define SAW_INFO(...)	      ::SAW::Log::GetClientLogger()->info(__VA_ARGS__)
#define SAW_WARN(...)	      ::SAW::Log::GetClientLogger()->warn(__VA_ARGS__)
#define SAW_ERROR(...)	      ::SAW::Log::GetClientLogger()->error(__VA_ARGS__)
#define SAW_FATAL(...)	      ::SAW::Log::GetClientLogger()->fatal(__VA_ARGS__)