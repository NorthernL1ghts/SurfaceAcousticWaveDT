#include "imgui.h"
#include "backends/imgui_impl_glfw.h"
#include "backends/imgui_impl_opengl3.h"
#include <GLFW/glfw3.h>
#include <cmath>
#include <vector>
#include <chrono>
#include <algorithm>
#include <ranges>

constexpr double PI = 3.14159265358979323846;

// Physical constants
struct PhysicalConstants {
	static constexpr double speedOfLight = 299792458.0; // m/s
	static constexpr double speedOfSound = 343.0;       // m/s
	static constexpr double speedOfTime = 1.0;          // arbitrary scaling
};

// Material properties for Lithium Niobate Y-cut 128
struct MaterialProperties {
	double density = 4650.0;        // kg/m^3
	double elasticModulus = 2.05e11; // Pa
	double poissonRatio = 0.27;
	double decayCoefficientZ = 0.2; // exponential decay factor in z
};

// Simulation context
struct SimulationContext {
	int numPointsX = 150;
	int numPointsY = 150;
	double domainLengthX = 4.0 * PI;
	double domainLengthY = 4.0 * PI;

	double amplitude = 0.5;
	double frequency = 20000.0;
	double pitch = 1.0;
	double wavelength = 0.1;

	std::vector<double> vertices; // x,y,z,amplitude,frequency,pitch,wavelength
	double decayZ = 0.2; // decay along y
};

enum class WaveType { Single, CounterPropagating };

// Propagate wave (single or counter-propagating)
void PropagateWave(SimulationContext& context, double time, WaveType waveType)
{
	const int nx = context.numPointsX;
	const int ny = context.numPointsY;
	const double k = 2.0 * PI / context.wavelength;
	const double omega = 2.0 * PI * context.frequency * context.pitch;

	if (context.vertices.size() != nx * ny * 7)
		context.vertices.resize(nx * ny * 7);

	for (int ix : std::views::iota(0, nx)) {
		for (int iy : std::views::iota(0, ny)) {
			double x = static_cast<double>(ix) / nx * context.domainLengthX;
			double y = static_cast<double>(iy) / ny * context.domainLengthY;

			double z = 0.0;
			if (waveType == WaveType::Single)
				z = context.amplitude * std::sin(k * x - omega * time);
			else {
				double forwardZ = context.amplitude * std::sin(k * x - omega * time);
				double backwardZ = context.amplitude * std::sin(k * x + omega * time);
				z = forwardZ + backwardZ;
			}

			z *= std::exp(-context.decayZ * y);

			int idx = 7 * (iy * nx + ix);
			context.vertices[idx + 0] = x;
			context.vertices[idx + 1] = y;
			context.vertices[idx + 2] = z;
			context.vertices[idx + 3] = context.amplitude;
			context.vertices[idx + 4] = context.frequency;
			context.vertices[idx + 5] = context.pitch;
			context.vertices[idx + 6] = context.wavelength;
		}
	}
}

// Draw the mesh as wireframe lines
void DrawMesh(const SimulationContext& context)
{
	int nx = context.numPointsX;
	int ny = context.numPointsY;

	glBegin(GL_LINES);
	for (int ix : std::views::iota(0, nx - 1)) {
		for (int iy : std::views::iota(0, ny - 1)) {
			int idx = iy * nx + ix;
			int nextX = iy * nx + (ix + 1);
			int nextY = (iy + 1) * nx + ix;

			glVertex3d(context.vertices[7 * idx + 0], context.vertices[7 * idx + 1], context.vertices[7 * idx + 2]);
			glVertex3d(context.vertices[7 * nextX + 0], context.vertices[7 * nextX + 1], context.vertices[7 * nextX + 2]);

			glVertex3d(context.vertices[7 * idx + 0], context.vertices[7 * idx + 1], context.vertices[7 * idx + 2]);
			glVertex3d(context.vertices[7 * nextY + 0], context.vertices[7 * nextY + 1], context.vertices[7 * nextY + 2]);
		}
	}
	glEnd();
}

int main() {
	if (!glfwInit()) return -1;

	glfwWindowHint(GLFW_CONTEXT_VERSION_MAJOR, 3);
	glfwWindowHint(GLFW_CONTEXT_VERSION_MINOR, 3);

	GLFWwindow* window = glfwCreateWindow(1280, 720, "3D Rayleigh SAW POC – 20 kHz", NULL, NULL);
	if (!window) { glfwTerminate(); return -1; }
	glfwMakeContextCurrent(window);
	glfwSwapInterval(1);

	// ImGui
	IMGUI_CHECKVERSION();
	ImGui::CreateContext();
	ImGui::StyleColorsDark();
	ImGui_ImplGlfw_InitForOpenGL(window, true);
	ImGui_ImplOpenGL3_Init("#version 330");

	SimulationContext context;

	struct WaveGUI {
		float amplitude = 0.5f;
		float wavelength = 0.1f;
		float frequency = 20000.0f;
		float pitch = 1.0f;
	} gui;

	auto startTime = std::chrono::steady_clock::now();

	while (!glfwWindowShouldClose(window)) {
		glfwPollEvents();

		auto currentTime = std::chrono::steady_clock::now();
		double elapsedTime = std::chrono::duration<double>(currentTime - startTime).count();

		context.amplitude = gui.amplitude;
		context.wavelength = gui.wavelength;
		context.frequency = gui.frequency;
		context.pitch = gui.pitch;

		PropagateWave(context, elapsedTime, WaveType::CounterPropagating);

		// ImGui frame
		ImGui_ImplOpenGL3_NewFrame();
		ImGui_ImplGlfw_NewFrame();
		ImGui::NewFrame();
		ImGui::Begin("Wave Controls");
		ImGui::SliderFloat("Amplitude", &gui.amplitude, 0.01f, 1.0f);
		ImGui::SliderFloat("Wavelength", &gui.wavelength, 0.01f, 0.5f);
		ImGui::SliderFloat("Frequency", &gui.frequency, 1000.0f, 50000.0f);
		ImGui::SliderFloat("Pitch", &gui.pitch, 0.1f, 5.0f);
		ImGui::End();

		int framebufferWidth, framebufferHeight;
		glfwGetFramebufferSize(window, &framebufferWidth, &framebufferHeight);
		float aspectRatio = static_cast<float>(framebufferWidth) / framebufferHeight;

		glViewport(0, 0, framebufferWidth, framebufferHeight);
		glClearColor(0.1f, 0.1f, 0.1f, 1.0f);
		glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT);
		glEnable(GL_DEPTH_TEST);

		// Projection
		glMatrixMode(GL_PROJECTION);
		glLoadIdentity();
		double fov = 45.0 * PI / 180.0;
		double nearPlane = 0.1;
		double farPlane = 50.0;
		double top = std::tan(fov / 2.0) * nearPlane;
		double right = top * aspectRatio;
		glFrustum(-right, right, -top, top, nearPlane, farPlane);

		glMatrixMode(GL_MODELVIEW);
		glLoadIdentity();
		glTranslated(-context.domainLengthX / 2.0, -context.domainLengthY / 2.0, -20.0);
		glRotated(30.0, 1, 0, 0);

		DrawMesh(context);

		ImGui::Render();
		ImGui_ImplOpenGL3_RenderDrawData(ImGui::GetDrawData());

		glfwSwapBuffers(window);
	}

	ImGui_ImplOpenGL3_Shutdown();
	ImGui_ImplGlfw_Shutdown();
	ImGui::DestroyContext();
	glfwDestroyWindow(window);
	glfwTerminate();

	return 0;
}
