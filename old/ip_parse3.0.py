import subprocess
import os





command = f"ipconfig"
ip_readout = subprocess.check_output(command)
ip_readout = ip_readout.decode("utf-8")

# bad_chars = {ord("'"): None, ord("b"): None}

lines = ip_readout.splitlines()

adapters = []
previous_line = False
interfaces = {}

# Find Adapters
for line in lines:
	if "adapter" in line:
		parsed_adapter = line.split("adapter ")
		adapters.append(parsed_adapter[-1].replace(":",""))
# Work on adapters
for adapter in adapters:
	current_adapter = adapters.index(adapter)
	try:
		current_adapter += 1	
		next_adapter = str(adapters[current_adapter])
		raw_interface = ip_readout[ip_readout.find(adapter)+len(adapter):ip_readout.rfind(next_adapter)]
		interface_lines = raw_interface.splitlines()
		for interface_line in interface_lines:
			if "IPv4" in interface_line:
				ip_address = interface_line.split(": ")
				interfaces[adapter+"_ip_address"] = ip_address[-1]
			elif "Subnet" in interface_line:
				subnet = interface_line.split(": ")
				interfaces[adapter+"_subnet"] = subnet[-1]
			elif "Gateway" in interface_line:
				if "%" in interface_line:
					previous_line = True
			elif previous_line == True:
					gateway = str(interface_line.strip())
					interfaces[adapter+"_gateway"] = gateway
					previous_line = False
			else:
				pass
	except IndexError:
		break
	
print(interfaces)