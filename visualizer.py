import ctypes
import json
import matplotlib.pyplot as plt
from ctypes import Structure, c_uint, c_float

class SimConfig(Structure):
    _fields_ = [
        ("abr_type", c_uint),
        ("abr_window_size", c_uint),
        ("buffer_size_max", c_float),
        ("segment_duration", c_float),
        ("stall_threshold", c_float),
    ]

# Load DLL
sim = ctypes.CDLL("/qoe_simulator.dll")

# FFI Function Signature
sim.simulate_and_get_json.argtypes = [SimConfig]
sim.simulate_and_get_json.restype = ctypes.c_char_p

sim.free_simulation_string.argtypes = [ctypes.c_char_p]
sim.free_simulation_string.restype = None

# Set Config
config = SimConfig(
    abr_type=2,
    abr_window_size=3,
    buffer_size_max=10.0,
    segment_duration=1.0,
    stall_threshold=0.5
)

# Call simulation
json_ptr = sim.simulate_and_get_json(config)
json_str = ctypes.cast(json_ptr, ctypes.c_char_p).value.decode("utf-8")
sim.free_simulation_string(json_ptr)

# Parse data
data = json.loads(json_ptr)

# Plot data
timestamps = [frame["timestamp"] for frame in data]
bitrates = [frame["bitrate_kbps"] for frame in data]
buffer = [frame["buffer_level_secs"] for frame in data]
stalls = [i for i, frame in enumerate(data) if frame["stalled"]]

plt.figure()
plt.subplot(2, 1, 1)
plt.plot(timestamps, bitrates, label="bitrate (kbps)")
plt.scatter(timestamps, [bitrates[i] for i in stalls], label="bitrate (kbps)")
plt.legend()
plt.title("Bitrate & Stalls Over Time")

plt.subplot(2, 1, 2)
plt.plot(timestamps, buffer, label="buffer (s)", color="orange")
plt.axhline(0.5, color="red", linestyle="--", lavel="Stall Threshold")
plt.legend()
plt.title("Buffer Level")

plt.tight_layout()
plt.show()