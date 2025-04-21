# 🎥 QoE Python Visualizer

A Python-based visualizer for adaptive bitrate (ABR) streaming simulations.  
This project interfaces with a Rust-based core simulation engine (`qoe_core.dll`) to:

- Simulate streaming playback with configurable ABR strategies
- Collect and plot metrics such as:
  - Bitrate over time
  - Buffer levels
  - Playback stalls
- Calculate and display a Quality of Experience (QoE) score

---

## 📦 Project Structure

```
qoe_python_visualizer/
├── libs/                         # Rust-built DLL goes here
│   └── qoe_core.dll              # Windows DLL (or .so/.dylib)
├── visualize.py                  # Main Python visualizer script
├── requirements.txt              # Python dependencies (optional)
└── README.md                     # You're reading this!
```

---

## ⚙️ Prerequisites

- **Python 3.10+** (recommended)
- Rust `qoe-core` project built (`cargo build --release`)
  - https://github.com/mrjaywilson/QOE-Core
- `qoe_core.dll` placed inside `libs/` folder

Install required packages:

```bash
pip install matplotlib numpy
```

Or use `requirements.txt`:

```bash
pip install -r requirements.txt
```

---

## 🚀 Usage

### 1. Build the Rust Core

From the `qoe-core` project:

```bash
cargo build --release
```

Then copy the built DLL to this project’s `libs/` folder:

```bash
# From Rust project root
cp ./target/release/qoe_core.dll ../qoe_python_visualizer/libs/
```

### 2. Run the Visualizer

```bash
python visualize.py
```

You will see:
- A line graph of bitrate with red dots where stalls occurred
- A buffer level plot with a stall threshold line
- QoE score printed and shown in the title

---

## 🧠 What is QoE?

**QoE (Quality of Experience)** is a heuristic score (0–100) that reflects:
- Bitrate stability
- Stall frequency
- Switching frequency
- Buffer health

Used to evaluate ABR strategy effectiveness across devices or sessions.

---

## 🛠 Config Customization

You can adjust playback settings inside `visualize.py`:

```python
config = SimConfig(
    abr_type=2,              # 0=Fixed, 1=Buffer, 2=Throughput
    abr_window_size=3,
    buffer_size_max=10.0,
    segment_duration=1.0,
    stall_threshold=0.5
)
```

---

## 🧼 Troubleshooting

### `DLL not found`
Make sure `qoe_core.dll` exists inside the `libs/` folder and that you're using the correct path in `visualize.py`.

### `Heap corruption` or `exit code 0xC0000374`
Ensure you're calling `free_simulation_string()` **after** copying the returned string into Python memory.

---

## 📄 License

MIT

---

## ✨ Credits

- Rust core developed in [`qoe-core`](https://github.com/yourname/qoe-core)
- Python visualization by [@mrjaywilson](https://github.com/mrjaywilson)
