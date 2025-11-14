<p align="center">
  <a href="https://github.com/hugou74130/farm_render" rel="noopener">
    <img width="300px" height="300px" src="https://image.noelshack.com/fichiers/2025/46/5/1763132331-gemini-generated-image-2pmc2u2pmc2u2pmc-1.jpg" alt="Farm Render Logo">
  </a>
</p>

<h1 align="center">🚜 Farm Render</h1>

<p align="center">
  <strong>A distributed rendering farm solution for Blender</strong><br>
  Accelerate your render times by leveraging multiple devices working in parallel.
</p>

<div align="center">

[![Status](https://img.shields.io/badge/status-active-success.svg)](https://github.com/hugou74130/farm_render)
[![GitHub Issues](https://img.shields.io/github/issues/hugou74130/farm_render.svg)](https://github.com/hugou74130/farm_render/issues)
[![GitHub Pull Requests](https://img.shields.io/github/issues-pr/hugou74130/farm_render.svg)](https://github.com/hugou74130/farm_render/pulls)
[![License](https://img.shields.io/badge/license-MIT-blue.svg)](LICENSE)

</div>

---

## Table of Contents

- [About](#about)
- [Features](#features)
- [Getting Started](#getting-started)
- [Installation](#installation)
- [Usage](#usage)
- [Architecture](#architecture)
- [Contributing](#contributing)
- [License](#license)

---

## About <a name="about"></a>

**Farm Render** is a Blender addon designed to create a distributed rendering farm that maximizes and optimizes rendering times. Instead of rendering complex scenes on a single workstation, Farm Render allows multiple devices to connect to the same project and distribute rendering tasks across the network, significantly reducing total render time.

### Why Farm Render?

Rendering in Blender can be extremely time-consuming, especially for high-quality scenes that require substantial GPU or CPU processing power. Even with powerful hardware, complex projects can take hours or days to complete. **Farm Render** solves this problem by enabling:

- **Parallel Processing**: Distribute rendering tasks across multiple computers simultaneously
- **Resource Optimization**: Utilize all available computing power in your network
- **Faster Turnaround**: Complete projects in a fraction of the time
- **Scalability**: Add more devices to your farm as needed

---

## Features <a name="features"></a>

✨ **Key Highlights:**

- 🔗 **Seamless Network Integration**: Easy setup for distributed rendering across multiple machines
- ⚡ **Optimized Performance**: Intelligent task distribution for maximum efficiency
- 🎛️ **Simple Blender Integration**: Addon-based solution that integrates directly into Blender's interface
- 🔄 **Automatic Task Management**: Handles frame distribution and collection automatically
- 💻 **Cross-Platform Support**: Works on Windows, Linux, and macOS
- 🎨 **Non-Intrusive**: Minimal changes to your existing Blender workflow

---

## Getting Started <a name="getting-started"></a>

### Prerequisites

Before you begin, ensure you have the following installed:

**Blender** (version 3.0 or higher recommended)

- **Linux (Arch)**: `sudo pacman -S blender`
- **Windows**: Download from [blender.org](https://www.blender.org/)
- **macOS**: Download from [blender.org](https://www.blender.org/)

**Git** (for cloning the repository)

### System Requirements

- **Network**: All machines should be on the same local network
- **Storage**: Sufficient disk space for project files and rendered output
- **Hardware**: Multi-core processor and dedicated GPU (optional but recommended for faster rendering)

---

## Installation <a name="installation"></a>

### Step 1: Clone the Repository

```bash
git clone https://github.com/hugou74130/farm_render.git
cd farm_render
```

### Step 2: Add the Addon to Blender

1. Open **Blender**
2. Go to **Edit** → **Preferences**
3. Navigate to the **Add-ons** tab
4. Click **Install...** and select the `farm_render.py` file from the cloned repository
5. Search for "Farm Render" and enable the addon by checking the checkbox

The addon will now appear in your Blender interface as a new panel on the right sidebar.

### Step 3: Configure Your Farm

1. In the Farm Render panel, configure the **Network Settings**:
   - Set the **Master Node** (the primary machine coordinating renders)
   - Add **Worker Nodes** (machines that will perform rendering)
   - Configure the **Network Port** (default: 9999)

2. Test the connection between nodes to ensure proper communication

---

## Usage <a name="usage"></a>

### Basic Workflow

#### 1. **Prepare Your Project**
   - Open your Blender project
   - Ensure all assets are saved locally or accessible from all farm machines

#### 2. **Set Render Settings**
   - Configure your render settings as usual (resolution, samples, etc.)
   - Choose your output location

#### 3. **Launch the Farm**
   - Open the Farm Render panel in the right sidebar
   - Click **Start Farm**
   - Select frames to render (or leave for automatic distribution)

#### 4. **Monitor Progress**
   - Watch real-time updates on rendering progress
   - View which machine is rendering which frame
   - Check performance statistics

#### 5. **Collect Results**
   - Once complete, rendered frames are automatically compiled
   - Output is saved to your specified location

---

## Architecture <a name="architecture"></a>

```
┌─────────────────┐
│  Master Node    │ (Coordinates tasks)
│  (Blender)      │
└────────┬────────┘
         │
    ┌────┴──────┬─────────────┐
    │            │             │
┌───▼──┐   ┌────▼──┐   ┌─────▼───┐
│Worker│   │Worker │   │ Worker  │
│ 1    │   │  2    │   │   3     │
└──────┘   └───────┘   └─────────┘

All machines communicate over local network
```

---

## Contributing <a name="contributing"></a>

We welcome contributions! To help improve Farm Render:

1. **Fork** the repository
2. **Create** a feature branch (`git checkout -b feature/amazing-feature`)
3. **Commit** your changes (`git commit -m 'Add amazing feature'`)
4. **Push** to your branch (`git push origin feature/amazing-feature`)
5. **Open** a Pull Request

Please ensure your code follows the project's style guidelines and includes appropriate documentation.

---

## License <a name="license"></a>

This project is licensed under the **MIT License** - see the [LICENSE](LICENSE) file for details.

---

## Support & Issues

Encountered a problem? Have a suggestion?

- 📝 [Open an Issue](https://github.com/hugou74130/farm_render/issues)
- 💬 [Start a Discussion](https://github.com/hugou74130/farm_render/discussions)

---

<div align="center">

