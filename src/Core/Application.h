#pragma once

namespace SAW  {
	class Application
	{
	public:
		Application();
		virtual ~Application();

		void Run();
	private:
        bool m_Running = true;
    };
}