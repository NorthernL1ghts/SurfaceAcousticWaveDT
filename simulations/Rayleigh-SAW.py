import math
import time
import numpy as np

PI = 3.14159265358979323846

# Physical constants
class PhysicalConstants:
    speedOfLight = 299792458.0  # m/s
    speedOfSound = 343.0        # m/s
    speedOfTime = 1.0           # arbitrary scaling

# Material properties for Lithium Niobate Y-cut 128
class MaterialProperties:
    def __init__(self):
        self.density = 4650.0         # kg/m^3
        self.elasticModulus = 2.05e11 # Pa
        self.poissonRatio = 0.27
        self.decayCoefficientZ = 0.2  # exponential decay factor in z

# Simulation context
class SimulationContext:
    def __init__(self):
        self.numPointsX = 20   # smaller for printing; set back to 150 if needed
        self.numPointsY = 20
        self.domainLengthX = 4.0 * PI
        self.domainLengthY = 4.0 * PI

        self.amplitude = 0.5
        self.frequency = 20000.0
        self.pitch = 1.0
        self.wavelength = 0.1

        # x,y,z,amplitude,frequency,pitch,wavelength
        self.vertices = np.zeros(self.numPointsX * self.numPointsY * 7)
        self.decayZ = 0.2  # decay along y

# Wave type enum equivalent
class WaveType:
    Single = 1
    CounterPropagating = 2

# Propagate wave (single or counter-propagating)
def PropagateWave(context: SimulationContext, time_val: float, waveType: int):
    nx = context.numPointsX
    ny = context.numPointsY
    k = 2.0 * PI / context.wavelength
    omega = 2.0 * PI * context.frequency * context.pitch

    if context.vertices.size != nx * ny * 7:
        context.vertices = np.zeros(nx * ny * 7)

    for ix in range(nx):
        for iy in range(ny):
            x = float(ix) / nx * context.domainLengthX
            y = float(iy) / ny * context.domainLengthY

            if waveType == WaveType.Single:
                z = context.amplitude * math.sin(k * x - omega * time_val)
            else:
                forwardZ = context.amplitude * math.sin(k * x - omega * time_val)
                backwardZ = context.amplitude * math.sin(k * x + omega * time_val)
                z = forwardZ + backwardZ

            z *= math.exp(-context.decayZ * y)

            idx = 7 * (iy * nx + ix)
            context.vertices[idx + 0] = x
            context.vertices[idx + 1] = y
            context.vertices[idx + 2] = z
            context.vertices[idx + 3] = context.amplitude
            context.vertices[idx + 4] = context.frequency
            context.vertices[idx + 5] = context.pitch
            context.vertices[idx + 6] = context.wavelength

# Example run (no graphics, just compute values)
if __name__ == "__main__":
    context = SimulationContext()

    start_time = time.time()

    # Run only a few iterations to avoid flooding console
    for step in range(3):
        elapsed_time = time.time() - start_time

        context.amplitude = 0.5
        context.wavelength = 0.1
        context.frequency = 20000.0
        context.pitch = 1.0

        PropagateWave(context, elapsed_time, WaveType.CounterPropagating)

        print(f"\n--- Time step {step}, elapsed {elapsed_time:.4f} s ---")
        nx, ny = context.numPointsX, context.numPointsY

        for iy in range(ny):
            for ix in range(nx):
                idx = 7 * (iy * nx + ix)
                x, y, z, amp, freq, pitch, wl = context.vertices[idx:idx+7]
                print(f"x={x:.3f}, y={y:.3f}, z={z:.6f}, "
                      f"amp={amp}, freq={freq}, pitch={pitch}, wl={wl}")

        time.sleep(0.5)  # pause between steps
