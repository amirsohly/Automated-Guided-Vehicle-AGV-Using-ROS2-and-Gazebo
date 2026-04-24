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

---

# 🚗 Automated Guided Vehicle (AGV) Simulation using ROS 2

This project presents a simplified **Automated Guided Vehicle (AGV)** simulation developed using **ROS 2 (Jazzy)**, designed with an **Industrial Internet of Things (IIoT)** perspective.

The system demonstrates modular robot architecture, real-time communication, and basic sensor simulation, including LIDAR and camera integration.

---

## 📌 Features

* ✅ ROS 2-based modular architecture
* ✅ AGV modeling using URDF
* ✅ Velocity-based control via `/cmd_vel`
* ✅ Simulated LIDAR sensor (`/scan`)
* ✅ Simulated camera (`/image`)
* ✅ Static warehouse map (`/map`)
* ✅ TF-based coordinate system
* ✅ Real-time visualization with Foxglove

---

## 🏗️ System Architecture

The project is organized into the following ROS 2 packages:

* **agv_description** → Robot model (URDF)
* **agv_controller** → Motion control
* **agv_sensors** → LIDAR & camera simulation
* **agv_map** → Static occupancy grid map

Communication is handled through:

* **ROS 2 Topics**
* **DDS middleware**
* **Publisher / Subscriber model**

---

## ⚙️ Technologies Used

* ROS 2 Jazzy
* Python (`rclpy`)
* URDF (Robot modeling)
* Foxglove Studio (Visualization)
* DDS (Communication middleware)

---

## 🤖 AGV Model

The robot is defined using URDF and consists of:

* `base_link` → Main body
* `laser_link` → LIDAR sensor
* `camera_link` → Camera sensor

The robot structure is published via:

```
/robot_description
```

---

## 🎮 Control

The AGV is controlled using:

```
/cmd_vel → geometry_msgs/Twist
```

Example:

```bash
ros2 topic pub /cmd_vel geometry_msgs/msg/Twist \
"{linear: {x: 0.5}, angular: {z: 0.2}}"
```

---

## 📡 Sensors

### 🔹 LIDAR

* Topic: `/scan`
* Type: `sensor_msgs/LaserScan`
* Function: Measures distance to obstacles

Example:

```bash
ros2 topic echo /scan
```

---

### 🔹 Camera

* Topic: `/image`
* Type: `sensor_msgs/Image`
* Function: Simulates forward visual perception

---

## 🗺️ Map

* Topic: `/map`
* Type: `nav_msgs/OccupancyGrid`
* Represents a static warehouse environment

---

## 📍 TF (Coordinate Frames)

TF manages spatial relationships between:

* `map`
* `base_link`
* `laser_link`
* `camera_link`

---

## 🌐 IIoT Perspective

This AGV acts as an **edge device**:

* Generates sensor data locally
* Communicates in real time via ROS 2
* Can be extended to cloud-based monitoring systems

---

## 🖥️ Visualization (Foxglove)

To visualize the system:

1. Run `foxglove_bridge`
2. Connect to:

```
ws://<your-ip>:8765
```

Visualize:

* TF tree
* LIDAR scan
* Camera feed
* Map

---

## ▶️ How to Run

### 1. Setup

```bash
source /opt/ros/jazzy/setup.bash
cd ~/agv_project
colcon build
source install/setup.bash
```

---

### 2. Run core nodes (separate terminals)

**Terminal 1**

```bash
ros2 run robot_state_publisher robot_state_publisher \
src/agv_description/urdf/agv.urdf
```

**Terminal 2**

```bash
ros2 run agv_controller <controller_node>
```

**Terminal 3**

```bash
ros2 run agv_sensors lidar_node
```

**Terminal 4**

```bash
ros2 run agv_sensors camera_node
```

**Terminal 5**

```bash
ros2 run agv_map map_node
```

---

### 3. Move the AGV

```bash
ros2 topic pub /cmd_vel geometry_msgs/msg/Twist \
"{linear: {x: 0.5}, angular: {z: 0.0}}"
```

---

## 📊 Key Topics

| Topic      | Description           |
| ---------- | --------------------- |
| `/cmd_vel` | Velocity control      |
| `/scan`    | LIDAR data            |
| `/image`   | Camera data           |
| `/tf`      | Coordinate transforms |
| `/map`     | Environment map       |

---

## ⚠️ Notes

* This project uses **kinematic simulation** (no physics engine like Gazebo)
* Movement is represented through **TF updates**, not physical displacement
* Sensors are **logical simulations**, not physics-based

---

## 🚀 Future Work

* Obstacle avoidance using LIDAR
* Autonomous navigation
* Integration with cloud (MQTT / Edge computing)
* Multi-robot coordination

---

## 📄 License

This project is for educational purposes.

---

## 🙌 Acknowledgments

Developed as part of the **Industrial Internet of Things (IIoT)** course at the University of Messina.

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
