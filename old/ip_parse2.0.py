import subprocess
import os





command = f"ipconfig"
ip_readout = subprocess.check_output(command)
ip_readout = ip_readout.decode("utf-8")

# bad_chars = {ord("'"): None, ord("b"): None}

lines = ip_readout.splitlines()

adapters = []
previous_line = False


# Find Adapters
for line in lines:
	if "adapter" in line:
		parsed_adapter = line.split("adapter ")
		adapters.append(parsed_adapter[-1].replace(":",""))
# Work on adapters
for adapter in adapters:
	print(f"THIS IS THE : --------{adapter}")
	current_adapter = adapters.index(adapter)
	try:
		current_adapter += 1
		next_adapter = str(adapters[current_adapter])
	except IndexError:
   		break
	raw_interface = ip_readout[ip_readout.find(adapter)+len(adapter):ip_readout.rfind(next_adapter)]
	print(f"THIS_IS_THE_NEXT_{next_adapter}")
	# print(raw_interface)
	
	interface_lines = raw_interface.splitlines()
	for interface_line in interface_lines:
		if "IPv4" in interface_line:
			ip_address = interface_line.split(": ")
			ip_address = ip_address[-1]
		elif "Subnet" in interface_line:
			subnet = interface_line.split(": ")
			subnet = subnet[-1]
		elif "Gateway" in interface_line:
			if "%" in interface_line:
				previous_line = True
		else:
			if previous_line == True:
				gateway = str(interface_line.strip())
				previous_line = False	
	print(ip_address)
	print(subnet)
	print(gateway)