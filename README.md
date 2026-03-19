# ProgettoSmartWalker

This repository contains a thesis project developed as part of a national university initiative. The project leverages **ROS2 Humble**, the **Nav2 stack**, and a **Turtlebot3** to create an assistive environment for gait rehabilitation.

## Project Overview

The primary goal of this project is to develop an autonomous robotic walker capable of assisting post-stroke patients during their recovery. 

**Key Objectives:**
* **Autonomous Navigation:** Validating the navigation system within a controlled environment.
* **Rehabilitation Algorithm:** Implementing an exercise routine where the robot acts as a guide.
* **Objective Metrics:** Providing a quantitative assessment of the patient's walking quality by measuring how accurately they follow the predefined guide.

---

## Prerequisites

Before running the project, ensure your system meets the following requirements:

* **Operating System:** Ubuntu 22.04 LTS
* **ROS2 Version:** [ROS2 Humble Hawksbill](https://docs.ros.org/en/humble/Installation.html)
* **Navigation Stack:** Navigation2 (Nav2)
* **Python Libraries:**
    ```bash
    pip install numpy matplotlib
    ```

*Note: For detailed ROS2 or Nav2 installation guides, please refer to the official documentation.*

---

## Configuration & Setup

To streamline your workflow, it is highly recommended to automate the sourcing of your environment by modifying the `.bashrc` file.

1.  **Open a terminal** (`CTRL+ALT+T`) and ensure you are in the home directory:
    ```bash
    cd ~/
    ```
2.  **Open the `.bashrc` file** with a text editor:
    ```bash
    nano .bashrc
    # or
    gedit .bashrc
    ```
    *(Use `sudo` if you encounter permission issues).*

3.  **Append the following lines** to the end of the file:

```bash
# ROS2 & Project Workspace Setup
source /opt/ros/humble/setup.bash
source ~/smartwalker_ws/install/setup.bash
source /usr/share/gazebo/setup.sh

# Gazebo & Turtlebot3 Configuration
export GAZEBO_MODEL_PATH=$GAZEBO_MODEL_PATH:/opt/ros/humble/share/turtlebot3_gazebo/models
export TURTLEBOT3_MODEL=burger
```
---
