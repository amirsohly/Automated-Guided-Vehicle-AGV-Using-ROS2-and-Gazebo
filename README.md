# Industrial AGV Simulation Project: Environment Setup & Troubleshooting on macOS (Apple Silicon)

<img width="1199" height="920" alt="11" src="https://github.com/user-attachments/assets/62cd6eeb-5626-4592-8829-8e1fffd1cf28" />

## Project Overview

This repository documents the environment setup, architectural decisions, and troubleshooting process for an Industrial Internet of Things (IIoT) project focused on designing, controlling, and visualizing an Automated Guided Vehicle (AGV). The project leverages ROS 2 for communication and control while addressing the practical limitations of running robotics simulation tools on macOS Apple Silicon systems.

**Student:** Amirreza Soheiliarasi  
**Program:** Master's Degree in Engineering in Computer Science  
**University:** University of Messina, Italy  
**Course:** Industrial IoT (Academic Year 2024–2025)  
**Professor:** Dr. Giovanni Merlino  
**Teaching Assistant:** Dr. Luca D’Agati  

---

## Goal of This Documentation

This README serves as a **technical and chronological report** of the attempts, failures, and final architectural solution adopted to run a ROS2-based AGV system on macOS Apple Silicon.

The focus is intentionally placed on:
- Platform constraints
- Toolchain incompatibilities
- Engineering decisions
- Validation strategies
- Final working architecture

This approach follows the course guidance, emphasizing **engineering reasoning over simple installation success**.

---

## Installation Attempts & Troubleshooting Log

---

## Attempt 1: Direct Homebrew Installation of ROS2 & Gazebo

**Objective:**  
Install ROS2 Humble and Gazebo directly on macOS using Homebrew.

**Outcome:**  
This attempt failed due to:
- Authentication and repository access issues with `ros/homebrew-ros`
- Inconsistent or unavailable ROS2 and Gazebo formulas for Apple Silicon
- Dependency resolution failures

Despite multiple credential and configuration fixes, the ROS2 Homebrew tap could not be reliably accessed.

**Conclusion:**  
Homebrew-based installation was deemed unstable and unsuitable for this platform.

---

## Attempt 2: ROS2 Source Compilation on macOS

**Objective:**  
Build ROS2 Humble from source to bypass missing binaries and Homebrew limitations.

**Key Issues Encountered:**
- `rclpy` unavailable for Python ≥ 3.13 on ARM64
- Persistent CMake version conflicts (Homebrew enforcing CMake 4.x)
- Colcon build failures even when forcing a compatible CMake version
- Identical failures reproduced across Python 3.13 and Python 3.9 environments

**Conclusion:**  
Source compilation on macOS Apple Silicon proved impractical due to deep toolchain incompatibilities.

---

## Attempt 3: Docker-Based ROS2 and Gazebo Environment

**Objective:**  
Run ROS2 and Gazebo inside Docker containers to isolate the environment from macOS constraints.

**Results:**
- ROS2 Humble core ran successfully inside Docker
- Gazebo and Ignition-based simulators were missing or unusable
- Official images showed platform mismatch warnings (`amd64` vs `arm64`)
- GUI-based simulators were inaccessible

**Conclusion:**  
Docker resolved ROS2 runtime issues but failed to provide a reliable Gazebo environment on macOS.

---

## Attempt 4: University VM (Gazebo Working Validation Environment)

**Objective:**  
Validate the AGV ROS2 stack in a fully supported Linux environment to distinguish platform issues from project-level issues.

**Environment:**
- **OS:** Ubuntu (x86_64)
- **ROS 2 Distribution:** Jazzy
- **Simulation Tool:** Gazebo
- **Access:** Remote via University VM (Tailscale)

**Results:**
1. ROS2 sourced correctly
2. Gazebo launched successfully
3. AGV URDF model spawned correctly
4. TF tree published and visualized
5. Velocity commands on `/cmd_vel` resulted in real simulated motion
6. Full ROS2–Gazebo integration confirmed

**Conclusion:**  
The project is **functionally correct**.  
All previous failures were confirmed to be **platform-specific**, not conceptual or architectural.

---

## Attempt 5: Remote Docker + Foxglove (Final Working Architecture)

**Objective:**  
Provide a fully functional AGV visualization and control setup on macOS **without requiring Gazebo or RViz locally**.

**Approach:**
- ROS2 runs inside a Docker container (Ubuntu 24.04)
- Visualization handled via Foxglove Studio on macOS
- Communication via `foxglove_bridge` (WebSocket)

---

## Final Architecture

- **Host OS:** macOS Sequoia (Apple Silicon)
- **Container OS:** Ubuntu 24.04
- **ROS Distribution:** ROS 2 Jazzy
- **Visualization:** Foxglove Studio (macOS)
- **Bridge:** `foxglove_bridge` (port 8765)
- **Simulation Scope:** URDF-based kinematic AGV model

No Gazebo or RViz installation is required on macOS.

---

## Functional Components

### 1. Dockerized ROS2 Workspace
- ROS2 Jazzy correctly sourced
- Custom packages built with `colcon`
- Active topics:
  - `/cmd_vel`
  - `/tf`
  - `/tf_static`
  - `/robot_description`
  - `/joint_states`

### 2. AGV Model (URDF)
- Simplified AGV geometry
- Published via `robot_state_publisher`
- Root frame: `base_link`
- Static transform between `map` and `base_link`

### 3. Foxglove Integration
- `ros-jazzy-foxglove-bridge` installed
- WebSocket reachable from macOS
- 3D model rendered correctly
- TF tree visualized in real time

### 4. Motion Control Validation
Velocity commands correctly affect the AGV state:

```bash
ros2 topic pub /cmd_vel geometry_msgs/msg/Twist \
"{linear: {x: 0.3}, angular: {z: 0.0}}"
