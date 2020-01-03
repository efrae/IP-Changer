import subprocess
import os

	
command = f"ipconfig"
ip_readout = subprocess.check_output(command)
ip_readout = ip_readout.decode("utf-8")
lines = ip_readout.splitlines()

class Interface:

	def __init__(self):
		self.ip_address = ""
		self.subnet = ""
		self.gateway = ""
		self.adapters = []
		self.find_adapters()
		self.parse_adapters()

	def find_adapters(self):
		for line in lines:
			if "adapter" in line:
				parsed_adapter = line.split("adapter ")
				self.adapters.append(parsed_adapter[-1].replace(":",""))		

	def parse_adapters(self):
		self.previous_line = False
		for self.adapter in self.adapters:
			current_adapter = self.adapters.index(self.adapter)
			try:
				current_adapter += 1	
				next_adapter = str(self.adapters[current_adapter])
				raw_interface = ip_readout[ip_readout.find(self.adapter)+len(self.adapter):ip_readout.rfind(next_adapter)]
				interface_lines = raw_interface.splitlines()
				for interface_line in interface_lines:
					if "IPv4" in interface_line:
						ip_address = interface_line.split(": ")
						self.ip_address = ip_address[-1]
					elif "Subnet" in interface_line:
						subnet = interface_line.split(": ")
						self.subnet = subnet[-1]
					elif "Gateway" in interface_line:
						if "%" in interface_line:
							previous_line = True
					elif self.previous_line == True:
							gateway = str(interface_line.strip())
							self.gateway = gateway
							previous_line = False
					else:
						pass
			except IndexError:
				break


test = Interface()


print(test.ip_address)
print(test.adapters)




