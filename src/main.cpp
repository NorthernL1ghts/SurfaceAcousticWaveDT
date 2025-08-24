#include "imgui.h"
#include "backends/imgui_impl_glfw.h"
#include "backends/imgui_impl_opengl3.h"
#include <GLFW/glfw3.h>
#include <cmath>
#include <vector>
#include <chrono>
#include <algorithm>

constexpr double PI = 3.14159265358979323846;

// Physical constants
struct PhysicalConstants {
	static constexpr double speedOfLight = 299792458.0;      // m/s
	static constexpr double speedOfSound = 343.0;            // m/s in air
	static constexpr double speedOfTime = 1.0;               // arbitrary scaling
};

// Material properties for Lithium Niobate
struct MaterialProperties {
	double density = 4650.0;          // kg/m^3
	double elasticModulus = 2.05e11;  // Pa
	double poissonRatio = 0.27;
};

// SAW properties
struct SAWProperties {
	double amplitude = 0.5;
	double wavelength = 0.1;       // meters
	double frequency = 20000.0;    // Hz
	double rotationAngle = 0.0;    // degrees
};

// Grid properties
struct GridProperties {
	int numPointsX = 150;
	int numPointsY = 150;
	double domainLengthX = 4.0 * PI;
	double domainLengthY = 4.0 * PI;
};

// Generate the displacement field for a Rayleigh SAW
void generateRayleighSAWMesh(const SAWProperties& sawProps,
	const GridProperties& gridProps,
	std::vector<double>& vertices,
	double time)
{
	int numPointsX = gridProps.numPointsX;
	int numPointsY = gridProps.numPointsY;
	double k = 2.0 * PI / sawProps.wavelength;
	double omega = 2.0 * PI * sawProps.frequency;

	vertices.resize(numPointsX * numPointsY * 3);

	for (int ix = 0; ix < numPointsX; ++ix) {
		for (int iy = 0; iy < numPointsY; ++iy) {
			double x = static_cast<double>(ix) / numPointsX * gridProps.domainLengthX;
			double y = static_cast<double>(iy) / numPointsY * gridProps.domainLengthY;

			// Rayleigh wave: decaying exponential in depth (z)
			double z = sawProps.amplitude * std::sin(k * x - omega * time) * std::exp(-0.2 * y);

			vertices[3 * (iy * numPointsX + ix) + 0] = x;
			vertices[3 * (iy * numPointsX + ix) + 1] = y;
			vertices[3 * (iy * numPointsX + ix) + 2] = z;
		}
	}
}

// Draw the mesh as wireframe lines
void drawMesh(const std::vector<double>& vertices, const GridProperties& gridProps)
{
	int numPointsX = gridProps.numPointsX;
	int numPointsY = gridProps.numPointsY;

	glBegin(GL_LINES);
	for (int ix = 0; ix < numPointsX - 1; ++ix) {
		for (int iy = 0; iy < numPointsY - 1; ++iy) {
			int currentIndex = iy * numPointsX + ix;
			int nextXIndex = iy * numPointsX + (ix + 1);
			int nextYIndex = (iy + 1) * numPointsX + ix;

			// Horizontal line
			glVertex3d(vertices[3 * currentIndex], vertices[3 * currentIndex + 1], vertices[3 * currentIndex + 2]);
			glVertex3d(vertices[3 * nextXIndex], vertices[3 * nextXIndex + 1], vertices[3 * nextXIndex + 2]);

			// Vertical line
			glVertex3d(vertices[3 * currentIndex], vertices[3 * currentIndex + 1], vertices[3 * currentIndex + 2]);
			glVertex3d(vertices[3 * nextYIndex], vertices[3 * nextYIndex + 1], vertices[3 * nextYIndex + 2]);
		}
	}
	glEnd();
}

int main() {
	// Initialize GLFW
	if (!glfwInit()) return -1;

	glfwWindowHint(GLFW_CONTEXT_VERSION_MAJOR, 3);
	glfwWindowHint(GLFW_CONTEXT_VERSION_MINOR, 3);

	GLFWwindow* window = glfwCreateWindow(1280, 720, "3D Rayleigh SAW 20kHz", NULL, NULL);
	if (!window) { glfwTerminate(); return -1; }
	glfwMakeContextCurrent(window);
	glfwSwapInterval(1);

	// Setup ImGui
	IMGUI_CHECKVERSION();
	ImGui::CreateContext();
	ImGui::StyleColorsDark();
	ImGui_ImplGlfw_InitForOpenGL(window, true);
	ImGui_ImplOpenGL3_Init("#version 330");

	// Properties
	PhysicalConstants constants;
	MaterialProperties lithiumNiobate;
	SAWProperties sawProps;
	GridProperties gridProps;

	// GUI-friendly floats
	struct SAWPropertiesGUI {
		float amplitude = 0.5f;
		float wavelength = 0.1f;
		float frequency = 20000.0f;
		float rotationAngle = 0.0f;
	} sawGUI;

	std::vector<double> vertices;
	auto startTime = std::chrono::steady_clock::now();

	while (!glfwWindowShouldClose(window)) {
		glfwPollEvents();

		// Time in seconds
		auto currentTime = std::chrono::steady_clock::now();
		double elapsedTime = std::chrono::duration<double>(currentTime - startTime).count();

		// Copy GUI values into physics properties
		sawProps.amplitude = static_cast<double>(sawGUI.amplitude);
		sawProps.wavelength = static_cast<double>(sawGUI.wavelength);
		sawProps.frequency = static_cast<double>(sawGUI.frequency);
		sawProps.rotationAngle = static_cast<double>(sawGUI.rotationAngle);

		// Generate mesh
		generateRayleighSAWMesh(sawProps, gridProps, vertices, elapsedTime);

		// ImGui frame
		ImGui_ImplOpenGL3_NewFrame();
		ImGui_ImplGlfw_NewFrame();
		ImGui::NewFrame();
		ImGui::Begin("SAW Controls");
		ImGui::SliderFloat("Rotation Angle", &sawGUI.rotationAngle, 0.0f, 360.0f);
		ImGui::SliderFloat("Amplitude", &sawGUI.amplitude, 0.01f, 1.0f);
		ImGui::SliderFloat("Wavelength", &sawGUI.wavelength, 0.01f, 0.5f);
		ImGui::SliderFloat("Frequency (Hz)", &sawGUI.frequency, 1000.0f, 50000.0f);
		ImGui::End();

		// OpenGL render
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
		double fieldOfViewRadians = 45.0 * PI / 180.0;
		double nearPlane = 0.1;
		double farPlane = 50.0;
		double top = std::tan(fieldOfViewRadians / 2.0) * nearPlane;
		double right = top * aspectRatio;
		glFrustum(-right, right, -top, top, nearPlane, farPlane);

		// Modelview
		glMatrixMode(GL_MODELVIEW);
		glLoadIdentity();
		glTranslated(-gridProps.domainLengthX / 2.0, -gridProps.domainLengthY / 2.0, -20.0);
		glRotated(30.0, 1, 0, 0);
		glRotated(sawProps.rotationAngle, 0, 0, 1);

		glColor3d(0.2, 0.7, 1.0);
		drawMesh(vertices, gridProps);

		// Render ImGui
		ImGui::Render();
		ImGui_ImplOpenGL3_RenderDrawData(ImGui::GetDrawData());

		glfwSwapBuffers(window);
	}

	// Cleanup
	ImGui_ImplOpenGL3_Shutdown();
	ImGui_ImplGlfw_Shutdown();
	ImGui::DestroyContext();
	glfwDestroyWindow(window);
	glfwTerminate();

	return 0;
}
