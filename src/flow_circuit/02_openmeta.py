import openmeta.designer as D
import openmeta.openroad as O
import math

# Read in the .cir file
with open('EMiTS_2976.cir', 'r') as f:
    content = f.readlines()

def process_line(line):
    parts = line.strip().split()
    name = parts[0]
    node1 = int(parts[1])
    node2 = int(parts[2])
    value = float(parts[3])

    if name[0] == 'R':
        resistance = value
        return f"{name} {node1} {node2} {resistance:.10f}ohm"
    elif name[0] == 'C':
        #capacitance = 1 / (value * (2 * math.pi * 1e6))
        capacitance = value
        return f"{name} {node1} {node2} {capacitance:.10f}F"
    elif name[0] == 'L':
        inductance = value
        return f"{name} {node1} {node2} {inductance:.10f}H"


# Process the content into a format that can be read by OpenROAD
processed_content = []
for line in content:
    # Here you would parse the line to extract the necessary information
    # and convert it into the appropriate format for OpenROAD
    processed_line = process_line(line)
    processed_content.append(processed_line)

# Create a new OpenMETA designer
designer = D.Designer()

# Create a new OpenROAD module
module = O.Module('EMiTS_2976_Module')

# Add the processed content to the OpenROAD module
module.add_netlist(processed_content)

# Add the OpenROAD module to the OpenMETA designer
designer.add_module(module)

# Generate the OpenMETA output file
output_file = designer.generate_output_file()

# Save the OpenMETA output file
with open('EMiTS_2976.omd', 'w') as f:
    f.write(output_file)
