#include "Log.h"

int main(int argc, char** argv)
{
	// TODO: Move this to Application.
	SAW::Log::Init();
	SAW_CORE_WARN("Initialized Log!");
	int a = 5;
	SAW_INFO("Hello! Var={0}", a);

	SAW::Application app;
	app.Run();
	return 0;
}