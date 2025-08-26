#include "Application.h"
#include "EntryPoint.h"

#include <iostream>
#include <cmath>

#ifndef M_PI
#define M_PI 3.1415926535897932384626433
#endif

namespace SAW {

	Application::Application()
		: m_Running(true)
	{

	}

	Application::~Application()
	{

	}

	std::vector<Point3D> Application::GenerateWave(int xSize, int ySize, float frequency, float amplitude, float pitch, float decayFactor)
	{
		std::vector<Point3D> wave;
		wave.reserve(xSize * ySize);

		const float waveSpeed = 3000.0f; // m/s, typical Rayleigh speed in solids
		const float wavelength = waveSpeed / frequency;
		const float k = 2.0f * M_PI / wavelength; // wavenumber

		for (int x = 0; x < xSize; ++x) {
			for (int y = 0; y < ySize; ++y) {
				float distance = x * pitch;

				// Rayleigh wave vertical displacement
				float height = amplitude * std::exp(-decayFactor * distance) * std::sin(k * distance);

				// Exponential decay for Z to simulate surface decay into depth
				float decay = std::exp(-decayFactor * distance);

				wave.push_back({ static_cast<float>(x), height, decay });
			}
		}

		return wave;
	}

	void Application::Run()
	{
		// Example wave parameters
		int xSize = 200;  // more points for better resolution
		int ySize = 50;
		float frequency = 20000.0f;  // 20 kHz
		float amplitude = 1.0f;
		float pitch = 0.0005f;       // smaller step for 20 kHz surface wave
		float decayFactor = 10.0f;   // stronger decay into depth

		// Generate the Rayleigh wave
		m_WaveData = GenerateWave(xSize, ySize, frequency, amplitude, pitch, decayFactor);

		// Print a sample point
		std::cout << "Rayleigh Wave generated. Sample point (10,5): "
			<< "X=" << m_WaveData[10 * ySize + 5].x
			<< ", Y=" << m_WaveData[10 * ySize + 5].y
			<< ", Z=" << m_WaveData[10 * ySize + 5].z
			<< std::endl;

		while (m_Running) {
			m_Running = false;
		}
	}
}
