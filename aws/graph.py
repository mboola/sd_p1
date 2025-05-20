import matplotlib.pyplot as plt

def generate_graph(backlog, current_nodes, desired_nodes, name_file):
	time = [i * 5 for i in range(len(backlog))]

	# Create the figure and axis objects
	fig, ax1 = plt.subplots(figsize=(10, 6))

	# Plotting current_petitions on the left y-axis
	line1, = ax1.plot(time, backlog, 'g-', label='Current Petitions')
	ax1.set_xlabel('Time (seconds)')
	ax1.set_ylabel('Current Petitions', color='g')
	ax1.tick_params(axis='y', labelcolor='g')

	ax2 = ax1.twinx()
	line2, = ax2.plot(time, current_nodes, 'b-', label='Current Nodes')
	ax2.set_ylabel('Nodes', color='b')
	ax2.tick_params(axis='y', labelcolor='b')

	ax2.set_ylim(0, 32)

	ax3 = ax1.twinx()
	ax3.spines['right'].set_position(('outward', 60))  # offset in pixels
	line3, = ax3.plot(time, desired_nodes, 'r--', label='Theoretical Nodes')
	ax3.set_ylabel('Theoretical Nodes', color='r')
	ax3.tick_params(axis='y', labelcolor='r')

	lines = [line1, line2, line3]
	labels = [line.get_label() for line in lines]
	ax1.legend(lines, labels, loc='upper left')

	# Add a title and grid
	plt.title('Autoscaler Overview: Petitions and Nodes over Time')
	ax1.grid(True)

	# Improve layout
	fig.tight_layout()

	plt.savefig(name_file, dpi=300)  # Change filename/format as needed
