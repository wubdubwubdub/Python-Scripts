import subprocess
import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
import psutil
import time

# Function to capture packets using tshark and display information
def capture_packets():
    command = ["tshark", "-i", "eth0", "-c", "10", "-T", "fields", "-e", "frame.number", "-e", "frame.len", "-e", "ip.src", "-e", "ip.dst"]
    
    try:
        result = subprocess.run(command, capture_output=True, text=True, check=True)
        packet_info = result.stdout.splitlines()
        
        # Display packet information in GUI
        for line in packet_info:
            packet_listbox.insert(tk.END, line)  # Insert each line into the listbox
    except subprocess.CalledProcessError as e:
        messagebox.showerror("Error", f"Error capturing packets: {e}")

# Function to kick a user off the network (simulated action)
def kick_user(user):
    messagebox.showinfo("Kick User", f"Simulated action: User '{user}' kicked off the network.")

# Function to update network statistics
def update_network_stats():
    # Get network statistics
    net_stats = psutil.net_io_counters()
    active_connections = len(psutil.net_connections())
    cpu_percent = psutil.cpu_percent(interval=1)
    
    # Update GUI labels with network information
    users_label.config(text=f"Number of Users: {len(psutil.users())}")
    data_label.config(text=f"Current Data Usage: {net_stats.bytes_sent + net_stats.bytes_recv} bytes")
    total_data_label.config(text=f"Total Data Usage: {net_stats.bytes_sent + net_stats.bytes_recv} bytes")
    interfaces_label.config(text=f"Network Interfaces: {', '.join([nic.name for nic in psutil.net_if_addrs().values()])}")
    connections_label.config(text=f"Active Connections: {active_connections}")
    cpu_label.config(text=f"CPU Utilization (Network): {cpu_percent}%")
    
    # Schedule the update every 5 seconds
    root.after(5000, update_network_stats)

# Main function to run the script
if __name__ == "__main__":
    # Initialize GUI
    root = tk.Tk()
    root.title("Network Monitor with User Management")
    root.geometry("800x600")
    
    # Frame for network statistics and controls
    stats_frame = ttk.Frame(root)
    stats_frame.pack(pady=10)
    
    # Labels for network statistics
    users_label = ttk.Label(stats_frame, text="Number of Users: ")
    users_label.grid(row=0, column=0, padx=5, pady=5, sticky="w")
    
    data_label = ttk.Label(stats_frame, text="Current Data Usage: ")
    data_label.grid(row=1, column=0, padx=5, pady=5, sticky="w")
    
    total_data_label = ttk.Label(stats_frame, text="Total Data Usage: ")
    total_data_label.grid(row=2, column=0, padx=5, pady=5, sticky="w")
    
    interfaces_label = ttk.Label(stats_frame, text="Network Interfaces: ")
    interfaces_label.grid(row=3, column=0, padx=5, pady=5, sticky="w")
    
    connections_label = ttk.Label(stats_frame, text="Active Connections: ")
    connections_label.grid(row=4, column=0, padx=5, pady=5, sticky="w")
    
    cpu_label = ttk.Label(stats_frame, text="CPU Utilization (Network): ")
    cpu_label.grid(row=5, column=0, padx=5, pady=5, sticky="w")
    
    # Listbox to display captured packets
    packet_listbox = tk.Listbox(root, width=100, height=15)
    packet_listbox.pack(pady=10)
    
    # Button to capture packets
    capture_button = ttk.Button(root, text="Capture Packets", command=capture_packets)
    capture_button.pack(pady=10)
    
    # Button to kick user (simulated action)
    def kick_user_gui():
        selected_user = users_listbox.get(tk.ACTIVE)
        if selected_user:
            kick_user(selected_user)
        else:
            messagebox.showwarning("Select User", "Please select a user to kick off the network.")

    kick_button = ttk.Button(root, text="Kick User", command=kick_user_gui)
    kick_button.pack(pady=10)
    
    # Function to update network statistics (simulated)
    def update_network_stats():
        # Simulated network statistics
        users_label.config(text="Number of Users: 10")
        data_label.config(text="Current Data Usage: 1000 bytes")
        total_data_label.config(text="Total Data Usage: 5000 bytes")
        interfaces_label.config(text="Network Interfaces: eth0, eth1")
        connections_label.config(text="Active Connections: 20")
        cpu_label.config(text="CPU Utilization (Network): 30%")
        
        # Schedule update every 5 seconds
        root.after(5000, update_network_stats)
    
    # Initial update of network statistics
    update_network_stats()
    
    # Start GUI main loop
    root.mainloop()
