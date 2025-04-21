import os
import json
import ctypes
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
dll_path = os.path.join(os.path.dirname(__file__), "libs", "qoe_core.dll")
sim = ctypes.CDLL(dll_path)

# FFI Function Signature
sim.simulate_and_get_json.argtypes = [SimConfig]
sim.simulate_and_get_json.restype = ctypes.c_void_p

sim.free_simulation_string.argtypes = [ctypes.c_void_p]
sim.free_simulation_string.restype = None

sim.simulate_with_config_and_get_score.argtypes = [SimConfig]
sim.simulate_with_config_and_get_score.restype = ctypes.c_float

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
json_str = ctypes.string_at(json_ptr).decode("utf-8")
sim.free_simulation_string(json_ptr)

# Parse data
try:
    data = json.loads(json_str)
except Exception as e:
    print("Failed to parse JSON:")
    print("Error:", e)

# Get Score
qoe_score = sim.simulate_with_config_and_get_score(config)

# Plot data
timestamps = [frame["timestamp"] for frame in data]
bitrates = [frame["bitrate_kbps"] for frame in data]
buffer = [frame["buffer_level_secs"] for frame in data]
stalls = [i for i, frame in enumerate(data) if frame["stalled"]]

plt.figure()
plt.subplot(2, 1, 1)
plt.plot(timestamps, bitrates, label="bitrate (kbps)")
plt.scatter([timestamps[i] for i in stalls], [bitrates[i] for i in stalls], label="bitrate (kbps)")
plt.legend()
plt.title(f"Bitrate & Stalls Over Time (QoE: {qoe_score:.1f}/100)")

plt.subplot(2, 1, 2)
plt.plot(timestamps, buffer, label="buffer (s)", color="orange")
plt.axhline(0.5, color="red", linestyle="--", label="Stall Threshold")
plt.legend()
plt.title("Buffer Level")

plt.tight_layout()
plt.show()