#pragma once

#include <vector>

namespace SAW {

	struct Point3D {
		float x;  // Distance
		float y;  // Height
		float z;  // Decay
	};

	class Application
	{
	public:
		Application();
		virtual ~Application();

		void Run();
	private:
		std::vector<Point3D> m_WaveData;
		std::vector<Point3D> GenerateWave(int xSize, int ySize, float frequency, float amplitude, float pitch, float decayFactor);
	private:
		bool m_Running = true;
	};
}
