import grSim_commands_pb2
import socket
import time
import numpy as np

# Import your RRT implementation
# from rrt import rrt, Environment  # Uncomment and adjust as needed

# Define grSim's IP and Port
GRSIM_IP = "127.0.0.1"  # Change if grSim is on a different machine
GRSIM_PORT = 20011

# Initialize UDP socket
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

def send_command(robot_id, vx, vy, omega):
    # Create a new packet
    packet = grSim_Commands_pb2.grSim_Packet()

    # Create a command for the specific robot
    
    robot_command = packet.commands.add()
    robot_command.id = robot_id  # Robot ID (0-15)
    robot_command.enable = True  # Enable the robot's movement

    # Set velocities
    robot_command.cmd.vx = vx      # X velocity (m/s)
    robot_command.cmd.vy = vy      # Y velocity (m/s)
    robot_command.cmd.vw = omega   # Angular velocity (rad/s)

    # Serialize the packet to a binary string
    binary_data = packet.SerializeToString()

    # Send the binary data via UDP
    sock.sendto(binary_data, (GRSIM_IP, GRSIM_PORT))

# Placeholder for getting the robot's current position
def get_robot_position(robot_id=0):
    # Implement a method to retrieve the robot's current position
    # This might involve parsing sensor data or maintaining state internally
    return [0, 0]  # Replace with actual position

# RRT Implementation (Ensure your RRT code is accessible here)
# from rrt import rrt, Environment, start, goal, plot_rrt

def main():
    # Define environment (match grSim's field dimensions and obstacles)
    width, height = 20, 20  # Example dimensions
    obstacles = [
        (5, 5, 2),
        (12, 12, 3),
        (7, 14, 2),
        (15, 5, 2)
    ]
    env = Environment(width, height, obstacles)

    # Define start and goal positions
    start = [0, 0]
    goal = [19, 19]

    # Run RRT to find a path
    path = rrt(start, goal, env, step_size=0.5, max_iter=10000, goal_threshold=0.5)

    if path:
        print("Path found:")
        print(path)
        # Optionally, plot the path
        # plot_rrt(path, env)

        robot_id = 0  # First robot

        for waypoint in path:
            current_pos = get_robot_position()  # Implement actual position retrieval
            direction = np.array(waypoint) - np.array(current_pos)
            distance = np.linalg.norm(direction)
            if distance == 0:
                continue
            direction = direction / distance
            speed = 1.0  # m/s, adjust as needed
            vx = direction[0] * speed
            vy = direction[1] * speed
            omega = 0.0  # rad/s, adjust for rotation if needed

            send_command(robot_id, vx, vy, omega)
            print(f"Moving towards waypoint: {waypoint} with velocities vx={vx}, vy={vy}")
            time.sleep(0.5)  # Adjust timing based on step_size and speed

        # Stop the robot after reaching the goal
        send_command(robot_id, vx=0.0, vy=0.0, omega=0.0)
        print("Reached the goal. Stopping the robot.")
    else:
        print("No path found.")

if __name__ == "__main__":
    main()
