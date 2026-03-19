# ProgettoSmartWalker

This repository contains a thesis project developed as part of a national university initiative. The project leverages **ROS2 Humble**, the **Nav2 stack**, and a **Turtlebot3** to create an assistive environment for gait rehabilitation.

## Project Overview

The primary goal of this project is to develop an autonomous robotic walker capable of assisting post-stroke patients during their recovery. 

**Key Objectives:**
* **Autonomous Navigation:** Validating the navigation system within a controlled environment.
* **Rehabilitation Algorithm:** Implementing an exercise routine.
* **Objective Metrics:** Providing a quantitative assessment of the patient's walking quality by measuring how accurately they follow the predefined guide.

---

## Prerequisites

Before running the project, ensure your system meets the following requirements:

* **Operating System:** Ubuntu 22.04 LTS
* **ROS2 Version:** [ROS2 Humble Hawksbill](https://docs.ros.org/en/humble/Installation/Ubuntu-Install-Debs.html)
* **Navigation Stack:** [Navigation2 (Nav2)](https://docs.nav2.org/getting_started/index.html)
* **Turtlebot3 Packages:** Install the simulation packages:
    ```bash
    sudo apt update
    sudo apt install ros-humble-turtlebot3-gazebo
    ```
* **Python Libraries:**
    ```bash
    pip install numpy matplotlib
    ```

*Note: For detailed ROS2 or Nav2 installation guides, please refer to the official documentation.
If you intend to use a physical Turtlebot3, please refer to the [official documentation](https://emanual.robotis.com/docs/en/platform/turtlebot3/quick-start/) for the specific installation and setup guide.*

---

##  Project Import

Clone the GitHub repository:
```bash
git clone https://github.com/Creesteean99/ProgettoSmartWalker.git
```

---

## Configuration & Setup

To streamline your workflow, it is highly recommended to automate the sourcing of your environment by modifying the `.bashrc` file.

*Note: this step should be done AFTER everything is installed*

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

## Launching the Simulation

1.  **Build the workspace**:
    ```bash
    cd ~/smartwalker_ws
    colcon build --symlink-install
    source install/setup.bash
    ```

2.  **Start the simulation**:
    ```bash
    ros2 launch smartwalker_pkg simulation.launch.py
    ```
> **Note on Workflow:** > Step 1 (Building) is **not required** every time you launch the simulation. Thanks to the `--symlink-install` flag, once the workspace is built the first time, any changes made to Python scripts or launch files will be applied immediately. You can skip the build step and proceed directly to Step 2 unless you add new files, dependencies, or change C++ code.

---

> **Pro Tip (Optional):** You can automate this entire process by adding an **alias** at the end of your `.bashrc` file. 
> Add the following line:
> `alias startsim='cd ~/smartwalker_ws && colcon build --symlink-install && source install/setup.bash && ros2 launch smartwalker_pkg simulation.launch.py'`
>
> After saving, you will only need to type `startsim` in a new terminal to build and launch everything at once.

---

## What to Expect

Upon launching, the simulation will open **Rviz**, **Gazebo**, and a custom **GUI**. 

Through the GUI, you can:
* **Data Recording:** Start/stop data logging.
* **Navigation Parameters:** Save new data for Start and End points, guide thickness, and sinusoidal amplitude.
* **Custom Guides:** Record data for custom trajectories.
* **Autonomous Movement:** Use the side buttons to move the robot to four predefined positions.
* **Manual Goals:** You can also set a target using the **2D Goal Pose** tool in Rviz.

> **Important:** Every time a parameter is modified in the GUI, you **must** click the **'Update Parameters'** button at the bottom to transmit the new values to the ROS2 nodes.

**NOTE on Manual Set:** The *Manual Set* buttons next to the Start and End points will save the robot's current position. If text is entered into the adjacent input fields, it will **overwrite** the Manual Set data. Ensure these fields are empty if you intend to capture the robot's coordinates.

---

## How the Rehabilitation Test Works

1.  **Preparation:** Press the **Record Data** button (ensure it is **ON**), select the guide type and parameters, then click **'Update Parameters'**. The selected guide will appear in Rviz.
2.  **Initial Positioning:** Move the robot toward the starting point (default is `x: 1.0`, `y: -2.0`). 
3.  **Data Logging:** As you approach the starting point, a terminal message will confirm the creation of the **CSV files**.
4.  **Execution:** Move the robot to the end point. 
5.  **Results:** If completed correctly, the final graph will appear in the terminal. A copy is saved automatically, but it is recommended to manually save the open window for better resolution.

**NOTE:** For rehabilitation exercises, the robot is moved using the teleop command:
```bash
ros2 run turtlebot3_teleop teleop_keyboard
```

---

## Advanced Configuration

### Launch Arguments
The main launch file includes several arguments to customize the system execution. You can override these defaults in the command line:

| Argument | Default Value | Description |
| :--- | :--- | :--- |
| `use_sim_time` | `true` | Uses simulation clock (Gazebo) instead of system clock. |
| `send_initial_pose` | `true` | Automatically sends the initial pose to the navigation stack. |
| `map_yaml_file` | `'planimetria.yaml'` | The map file used for navigation. |
| `which_locator` | `'AMCL'` | Selects the localization method. |
| `rviz_config` | `'sim_config.rviz'` | The Rviz configuration profile to load. |

For more detailed information, please refer to the specific README located in: 
`~/smartwalker_ws/src/smartwalker_pkg/launch`

### Localization Systems
The project supports both **Robot Localization** and **AMCL**. 
** Important:** Before switching or configuring localization methods, make sure to read the documentation inside: 
`~/smartwalker_ws/src/smartwalker_pkg/param`

---

## Internal Documentation
Most folders within this workspace contain their own `README.md` files with specific clarifications regarding their content and internal logic.

## 🚀 Future Developments

* **Methodical EKF Calibration:** Implementing a more rigorous tuning of the `robot_localization` filters, especially for physical robot deployment.
* **Enhanced Custom Guides:** Adding the ability to save, archive, and reload multiple custom trajectories, as well as saving new autonomous navigation waypoints.
* **Gazebo Visualization:** Implementing visual rendering for various guide types within the Gazebo environment.
* **Controller Server Optimization:** Validating different Controller Server plugins and implementing advanced filters for the Costmaps.

---

## Author & Contact

For further information or to report issues, please contact the development team:

* **Cristian Savoldi** – [https://github.com/Creesteean99]
