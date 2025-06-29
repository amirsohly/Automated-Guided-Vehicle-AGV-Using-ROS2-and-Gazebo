## Automated-Guided-Vehicle-AGV-Using-ROS2-and-Gazebo
# Industrial AGV Simulation Project: Environment Setup & Troubleshooting on macOS (Apple Silicon)

## Project Overview

This repository documents the environment setup and troubleshooting process for an Industrial IoT (IIoT) project focused on designing and simulating an Automated Guided Vehicle (AGV) within a simplified industrial environment. The project aims to leverage ROS2 for control and communication, and Gazebo for simulation.

**Student:** Amirreza Soheiliarasi (Master's Student in Engineering in Computer Science, University of Messina, Italy)

**Course:** Industrial IoT (Academic Year 2024-2025)

**Professor:** Dr. Giovanni Merlino

**Teaching assistant:** Dr. Luca D'Agati

## Goal of this Documentation

This `README.md` serves as a detailed, chronological log of the significant challenges encountered and the extensive troubleshooting steps attempted during the setup of ROS2 (Humble) and Gazebo (Ignition series) on a macOS system with Apple Silicon (M4 chip). As per Professor Merlino's guidance, this documentation is a critical component of the final assignment, highlighting the complexities of packaging and environment configuration on this specific platform. It aims to provide a clear, reproducible record of the installation journey.

## System Specifications

* **Operating System:** macOS Sequoia Version 15.5 (24F74)
* **Processor:** Apple M4 (ARM64 architecture)
* **RAM:** 16 GB

## Installation Attempts & Troubleshooting Log

This section details the chronological order of installation attempts, the specific commands executed, and the errors encountered, along with the troubleshooting steps taken. Each step is meticulously logged to provide a comprehensive overview.

---

### **Attempt 1: Direct Homebrew Installation of ROS2 & Gazebo (Initial Standard Approach)**

**Objective:** Install `ros-humble-desktop` and `gz-garden` directly via Homebrew as per initial standard ROS2 documentation for macOS.

**Commands Executed & Issues:**

1.  **Homebrew Update & Upgrade:**
    ```bash
    amirsohly@Amirrezas-MacBook-Air ~ % brew update
    ==> Updating Homebrew...
    Updated 3 taps (osrf/simulation, homebrew/core and homebrew/cask).
    ==> New Casks
    font-libertinus-sans         font-nata-sans
    font-libertinus-serif
    ==> Outdated Formulae
    ignition-common4             ignition-physics5
    ignition-fuel-tools7         ignition-rendering6
    ignition-gazebo6             ignition-sensors6
    ignition-gui6                nettle
    ignition-launch5             pango

    You have 10 outdated formulae installed.
    You can upgrade them with brew upgrade
    or list them with brew outdated.
    amirsohly@Amirrezas-MacBook-Air ~ % brew upgrade
    ... a lot of Upgrading
    ```
    *Outcome:* Homebrew updated successfully.

2.  **Locale Configuration for ROS2:**
    ```bash
    amirsohly@Amirrezas-MacBook-Air ~ % echo "export LC_ALL=en_US.UTF-8" >> ~/.zshrc
    amirsohly@Amirrezas-MacBook-Air ~ % echo "export LANG=en_US.UTF-8" >> ~/.zshrc
    amirsohly@Amirrezas-MacBook-Air ~ % source ~/.zshrc
    ```
    *Outcome:* Locales configured.

3.  **Tapping `ros/ros` Homebrew Repository:**
    ```bash
    amirsohly@Amirrezas-MacBook-Air ~ % brew tap ros/ros
    ==> Tapping ros/ros
    Cloning into '/opt/homebrew/Library/Taps/ros/homebrew-ros'...
    Username for '[https://github.com](https://github.com)': amirsohly
    Password for '[https://amirsohly@github.com](https://amirsohly@github.com)':
    remote: Support for password authentication was removed on August 13, 2021.
    remote: Please see [https://docs.github.com/get-started/getting-started-with-git/about-remote-repositories#cloning-with-https-urls](https://docs.github.com/get-started/getting-started-with-git/about-remote-repositories#cloning-with-https-urls) for information on currently recommended modes of authentication.
    fatal: Authentication failed for '[https://github.com/ros/homebrew-ros/](https://github.com/ros/homebrew-ros/)'
    Error: Failure while executing; `git clone https://github.com/ros/homebrew-ros /opt/homebrew/Library/Taps/ros/homebrew-ros --origin=origin --template= --config core.fsmonitor=false` exited with 128.
    ```
    *Issue:* Authentication failed due to GitHub's deprecation of password-based authentication for Git operations.

    *Troubleshooting Steps:*
    * Generated a GitHub Personal Access Token (PAT) with `repo` scope.
    * Attempted to clear Git credential helper cache:
        ```bash
        amirsohly@Amirrezas-MacBook-Air ~ % git config --global --unset credential.helper
        ```
    * Attempted to configure Git to use `osxkeychain` for credentials:
        ```bash
        amirsohly@Amirrezas-MacBook-Air ~ % git config --global credential.helper osxkeychain
        ```
    * Retried `brew tap ros/ros` with PAT:
        ```bash
        amirsohly@Amirrezas-MacBook-Air ~ % brew tap ros/ros
        ==> Tapping ros/ros
        Cloning into '/opt/homebrew/Library/Taps/ros/homebrew-ros'...
        Username for '[https://github.com](https://github.com)': amirsohly
        Password for '[https://amirsohly@github.com](https://amirsohly@github.com)':
        remote: Repository not found.
        fatal: repository '[https://github.com/ros/homebrew-ros/](https://github.com/ros/homebrew-ros/)' not found
        Error: Failure while executing; `git clone https://github.com/ros/homebrew-ros /opt/homebrew/Library/Taps/ros/homebrew-ros --origin=origin --template= --config core.fsmonitor=false` exited with 128.
        ```
    *Outcome:* Authentication issue persisted and shifted to "Repository not found," suggesting `ros/homebrew-ros` might not be the correct tap or had visibility issues, or there was a deeper Git configuration problem.

4.  **Installing `ros-humble-desktop` & `gz-garden`:**
    *These commands were not fully attempted at this point due to the `brew tap` failures.*

---

### **Attempt 2: ROS2 Source Compilation & Manual CMake Installation (Addressing `rclpy` & `cmake` conflicts)**

**Objective:** Install ROS2 from source, targeting specific Python/CMake versions due to Homebrew tap issues and anticipated binary incompatibilities.

**Background:** The previous failures indicated that direct Homebrew installation might be problematic. Also, `rclpy` (ROS2's Python client library) binaries are often unavailable for newer Python versions (like Python 3.13 default on macOS) on ARM64 architectures via `pip`, necessitating a source build.

**Commands Executed & Issues:**

1.  **Creating Workspace & Python Virtual Environment:**
    ```bash
    amirsohly@Amirrezas-MacBook-Air ~ % mkdir -p ~/agv_project_ws/src
    amirsohly@Amirrezas-MacBook-Air ~ % cd ~/agv_project_ws
    amirsohly@Amirrezas-MacBook-Air agv_project_ws % python3 -m venv ~/agv_project_ws/venv
    amirsohly@Amirrezas-MacBook-Air agv_project_ws % source ~/agv_project_ws/venv/bin/activate
    (venv) amirsohly@Amirrezas-MacBook-Air agv_project_ws % pip3 install -U rosdep rosinstall_generator vcstool colcon-common-extensions
    # ... (successful installation of these packages in venv)
    (venv) amirsohly@Amirrezas-MacBook-Air agv_project_ws % pip3 install -U rclpy rosidl_default_generators geometry_msgs sensor_msgs nav_msgs std_msgs
    ERROR: Could not find a version that satisfies the requirement rclpy (from versions: none)
    ERROR: No matching distribution found for rclpy
    ```
    *Issue:* `rclpy` and related ROS2 Python packages could not be found as pre-built binaries for Python 3.13 on macOS ARM64 in PyPI. This confirmed the necessity of a source build.

2.  **Downloading ROS2 Source Repositories:**
    ```bash
    (venv) amirsohly@Amirrezas-MacBook-Air agv_project_ws % curl -o src/ros2.repos [https://raw.githubusercontent.com/ros2/ros2/humble/ros2.repos](https://raw.githubusercontent.com/ros2/ros2/humble/ros2.repos)
    Warning: Failed to open the file src/ros2.repos: No such file or directory
    curl: (56) Failure writing output to destination, passed 1369 returned 4294967295
    (venv) amirsohly@Amirrezas-MacBook-Air agv_project_ws % rm -f src/ros2.repos # to clean up partial download
    (venv) amirsohly@Amirrezas-MacBook-Air agv_project_ws % mkdir -p src # created src directory explicitly
    (venv) amirsohly@Amirrezas-MacBook-Air agv_project_ws % curl -o src/ros2.repos [https://raw.githubusercontent.com/ros2/ros2/humble/ros2.repos](https://raw.githubusercontent.com/ros2/ros2/humble/ros2.repos)
    # ... (successful download)
    (venv) amirsohly@Amirrezas-MacBook-Air agv_project_ws % vcs import src < src/ros2.repos
    # ... (successful long download of ROS2 source repositories)
    ```
    *Issue:* Initial `curl` failed because `src` directory was not explicitly created. Resolved by `mkdir -p src`. `vcs import` then proceeded successfully.

3.  **ROSDEP Initialization and Dependency Installation:**
    ```bash
    (venv) amirsohly@Amirrezas-MacBook-Air agv_project_ws % rosdep update
    ERROR: no sources directory exists on the system meaning rosdep has not yet been initialized.
    Please initialize your rosdep with sudo rosdep init
    (venv) amirsohly@Amirrezas-MacBook-Air agv_project_ws % sudo rosdep init
    # ... (password prompt and successful initialization)
    (venv) amirsohly@Amirrezas-MacBook-Air agv_project_ws % rosdep update
    # ... (successful update)
    (venv) amirsohly@Amirrezas-MacBook-Air agv_project_ws % rosdep install --from-paths src --ignore-src -y --rosdistro humble
    # ... (successful installation of system dependencies)
    ```
    *Outcome:* `rosdep` successfully initialized and installed all required system dependencies.

4.  **Colcon Build & Persistent CMake Issue:**
    ```bash
    (venv) amirsohly@Amirrezas-MacBook-Air agv_project_ws % colcon build --symlink-install
    # ... (initial output)
    --- stderr: fastcdr
    CMake Error at CMakeLists.txt:18 (cmake_minimum_required):
      Compatibility with CMake < 3.5 has been removed from CMake.
    # ... (rest of CMake error and packages aborted/failed)
    Summary: 0 packages finished [2.09s]
      1 package failed: fastcdr
      9 packages aborted: ament_cppcheck ament_lint ament_package ament_pycodestyle google_benchmark_vendor gtest_vendor iceoryx_hoofs osrf_pycommon osrf_testing_tools_cpp
      4 packages had stderr output: fastcdr google_benchmark_vendor gtest_vendor osrf_testing_tools_cpp
      337 packages not processed
    ```
    *Issue:* `colcon build` failed with a `CMake` version compatibility error, despite `cmake --version` showing `cmake version 4.0.3` (which is an incorrect version for ROS2 build requirements, expecting 3.x.x).

    *Troubleshooting Steps:*
    * **Diagnosed `cmake` version conflict:**
        ```bash
        amirsohly@Amirrezas-MacBook-Air ~ % which cmake
        /opt/homebrew/bin/cmake
        amirsohly@Amirrezas-MacBook-Air ~ % cmake --version
        cmake version 4.0.3
        ```
        This indicated that Homebrew's `cmake` formula was installing an unexpected `4.0.3` version, or `PATH` wasn't prioritizing it correctly.
    * **Attempted to reinstall correct CMake via Homebrew:**
        ```bash
        amirsohly@Amirrezas-MacBook-Air ~ % brew uninstall cmake
        # ... (successful uninstall of 4.0.3)
        amirsohly@Amirrezas-MacBook-Air ~ % brew install cmake
        # ... (Homebrew surprisingly installed 4.0.3 again)
        amirsohly@Amirrezas-MacBook-Air ~ % cmake --version
        cmake version 4.0.3
        ```
        This confirmed that Homebrew itself was providing the incorrect `cmake` version for this system.
    * **Manually installed CMake 3.31.0 for macOS Universal (Apple Silicon):**
        * Downloaded `cmake-3.31.0-macos-universal.dmg` from `cmake.org`.
        * Dragged `CMake.app` to `Applications`.
        * Confirmed executable path: `/Applications/CMake.app/Contents/bin/cmake`
    * **Attempted `colcon build` with explicit `CMAKE_COMMAND` path:**
        ```bash
        (venv) amirsohly@Amirrezas-MacBook-Air agv_project_ws % rm -rf build install log
        (venv) amirsohly@Amirrezas-MacBook-Air agv_project_ws % colcon build --cmake-args -DCMAKE_COMMAND=/Applications/CMake.app/Contents/bin/cmake --symlink-install
        # ... (output showed repeated failures of fastcdr and others with "RuntimeError: Could not find 'cmake' executable")
        ```
        *Issue:* Even with the explicit path to the correct CMake, `colcon` failed, leading to `RuntimeError: Could not find 'cmake' executable`. This pointed to a deeper issue, likely Python environment compatibility or `colcon`'s internal handling of external executables on macOS ARM64.

    * **Attempted Python 3.9 Downgrade for venv:**
        * `deactivate`
        * `rm -rf ~/agv_project_ws/venv` (deleted Python 3.13 venv)
        * `brew install python@3.9` (successful installation of Python 3.9)
        * `which python3.9` -> `/opt/homebrew/bin/python3.9` (confirmed path)
        * `~/opt/homebrew/bin/python3.9 -m venv ~/agv_project_ws/venv_py39` (created new venv with Python 3.9)
        * `source ~/agv_project_ws/venv_py39/bin/activate`
        * Re-ran `pip3 install -U rosdep ...` (successful)
        * Re-ran `pip3 install -U rclpy ...` (still failed, confirming `rclpy` only via source build for this platform)
        * Re-ran `colcon build --cmake-args -DCMAKE_COMMAND=/Applications/CMake.app/Contents/bin/cmake --symlink-install` in `venv_py39`.
        * **Outcome:** `colcon build` in Python 3.9 venv still failed with the identical `RuntimeError: Could not find 'cmake' executable`.

---

### **Attempt 3: Docker-based Environment Setup (Primary Current Approach)**

**Objective:** Utilize Docker to provide a pre-configured and isolated ROS2 + Gazebo environment, bypassing direct installation complexities, aiming for a stable working environment.

**Background:** Given the persistent and intractable failures with direct/source installations, Docker became the most viable path.

**Commands Executed & Issues:**

1.  **Docker Desktop & XQuartz Setup:**
    * Docker Desktop (Mac with Apple Chip) was installed and confirmed running.
    * XQuartz (`xquartz.org`) was installed and macOS restarted.
    * `xhost +` was executed successfully:
        ```bash
        amirsohly@Amirrezas-MacBook-Air ~ % xhost +
        access control disabled, clients can connect from any host
        ```
    * Confirmed XQuartz running from Dock icon.

2.  **Project Directory & Docker Network:**
    ```bash
    amirsohly@Amirrezas-MacBook-Air ~ % mkdir -p ~/agv_project_docker/src
    amirsohly@Amirrezas-MacBook-Air ~ % docker network create ros_gazebo_net
    Error response from daemon: network with name ros_gazebo_net already exists
    ```
    *Outcome:* Directory created, network confirmed existing.

3.  **ROS2 Container Execution (Successful):**
    * Downloaded `ros:humble-ros-core` Docker image.
        ```bash
        amirsohly@Amirrezas-MacBook-Air ~ % docker pull ros:humble-ros-core
        # ... (Pull complete output)
        Status: Downloaded newer image for ros:humble-ros-core
        ```
    * Executed ROS2 container:
        ```bash
        amirsohly@Amirrezas-MacBook-Air ~ % docker run -it --rm \
            --name ros_container \
            --network ros_gazebo_net \
            --env="DISPLAY" \
            --volume="/tmp/.X11-unix:/tmp/.X11-unix:rw" \
            --volume="$HOME/agv_project_docker:/ros_ws" \
            ros:humble-ros-core \
            /bin/bash
        root@7a6b49ff0740:/# ros2 topic list
        /parameter_events
        /rosout
        root@7a6b49ff0740:/#
        ```
    * **Outcome:** ROS2 Humble Core is fully operational within the `ros_container`.

4.  **Gazebo Container Execution (Persistent Docker Image Issues):**
    * **Attempted `docker pull ros:humble-ros-desktop`:**
        ```bash
        amirsohly@Amirrezas-MacBook-Air ~ % docker pull ros:humble-ros-desktop
        Error response from daemon: failed to resolve reference "docker.io/library/ros:humble-ros-desktop": docker.io/library/ros:humble-ros-desktop: not found
        ```
        *Issue:* Image not found.

    * **Attempted `docker pull osrf/ros:humble-desktop`:**
        * Successfully downloaded this image (`Status: Downloaded newer image`).
        * Executed container:
            ```bash
            amirsohly@Amirrezas-MacBook-Air ~ % docker run -it --rm \
                --name gazebo_container \
                --network ros_gazebo_net \
                --env="DISPLAY" \
                --volume="/tmp/.X11-unix:/tmp/.X11-unix:rw" \
                osrf/ros:humble-desktop \
                /bin/bash
            WARNING: The requested image's platform (linux/amd64) does not match the detected host platform (linux/arm64/v8) and no specific platform was requested
            root@169d3a12ad31:/# gazebo
            bash: gazebo: command not found
            root@169d3a12ad31:/# gz sim -s
            bash: gz: command not found
            ```
        *Issue:* Despite `osrf/ros:humble-desktop` being a comprehensive image, `gazebo` and `gz` executables were not found within the container's `PATH`. This was unexpected and indicates a configuration issue within the image or platform incompatibility affecting executable discovery.

    * **Attempted `docker pull gazebosim/gz-sim:fortress` (and `garden`):**
        ```bash
        amirsohly@Amirrezas-MacBook-Air ~ % docker pull gazebosim/gz-sim:fortress
        Error response from daemon: pull access denied for gazebosim/gz-sim, repository does not exist or may require 'docker login'
        amirsohly@Amirrezas-MacBook-Air ~ % docker pull gazebosim/gz-sim:garden
        Error response from daemon: pull access denied for gazebosim/gz-sim, repository does not exist or may require 'docker login'
        ```
        *Issue:* Unable to pull these dedicated Gazebo images, consistently receiving "pull access denied" or "repository does not exist" errors, preventing the use of official Gazebo Docker images.

---

## Conclusion & Path Forward

The extensive troubleshooting process has revealed significant and persistent technical challenges in establishing a fully functional Gazebo simulation environment on macOS Apple Silicon, whether through direct installation (Homebrew/source) or various Docker images. These issues, particularly the deep-seated CMake conflict and the consistent executable discovery failures for Gazebo across multiple methods, are beyond standard configuration adjustments.

**Current Operational Status:**
* **ROS2 Humble Core is fully operational within its own Docker container (`ros_container`).**
* **A functional Gazebo environment remains elusive.**

As per Professor Merlino's most recent guidance, the primary focus of this assignment has shifted to:
1.  **Successfully establishing the ROS2 and Gazebo environment on macOS Apple Silicon.**
2.  **Thoroughly documenting all troubleshooting efforts and solutions found (as presented in this README).**
3.  **Potentially reducing the scope of the AGV simulation itself based on the effort required for environment setup.**

I am committed to diligently pursuing the setup by building upon Professor Merlino's "half-baked attempt at Homebrewing the formulas for Ros2 + employing ready-made formulas for Gazebo." I believe that by combining my troubleshooting log with the Professor's contributions, we can collectively achieve a robust and clean environment.

I am actively awaiting the Professor's shared resources to continue this critical setup phase. My commitment remains to deliver a complete and high-quality assignment within the extended deadline.
