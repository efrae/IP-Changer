import subprocess
import os

	
# command = f"ipconfig"
# ip_readout = subprocess.check_output(command)
# ip_readout = ip_readout.decode("utf-8")
# lines = ip_readout.splitlines()

class Interface:

	# def __init__(self):
	# 	self.find_adapters()

	def _send_command (self):
		command = f"ipconfig"
		self._ip_readout = subprocess.check_output(command)
		self._ip_readout = self._ip_readout.decode("utf-8")
		self._lines = self._ip_readout.splitlines()

	def find_adapters(self):
		self._send_command()
		self.adapters = []
		
		for _line in self._lines:
			if "adapter" in _line:
				parsed_adapter = _line.split("adapter ")
				self.adapters.append(parsed_adapter[-1].replace(":",""))

		for self.adapter in self.adapters:
			try:
				split_string = self._ip_readout.split(self.adapter,1)
				split_string_again = split_string[1].split("adapter", 1)
				if "Media disconnected" in split_string_again[0]:
					print(f"{self.adapter} is disconnected")
				else:
					print(f"{self.adapter} is connected")
				# print(f"\n\n\n\n{split_string_again[0]}\n\n\n\n")
				# self._current_adapter = self.adapters.index(self.adapter)
				# # print(f"current is {self.adapters[self._current_adapter]}")
				# self._next_adapter = self.adapters[self._current_adapter + 1]		
				# raw_interface = self._ip_readout[self._ip_readout.find(self.adapter)
				# 	+len(self.adapter):self._ip_readout.find(self._next_adapter)] 
				# # print(f'\n\n\n\n\nRAW_START{raw_interface}\n\n\nRAW_END \n\n\n\n')
				# if "Media disconnected" in raw_interface:
				# 	print(f"{self.adapters[self._current_adapter]} is disconnected")
				# else:
				# 	print(f"{self.adapter} is connected")
				# print(f"next adapter is '{self._next_adapter}'")
			except IndexError:
				break	

# 	def parse_adapters(self, adapter):
# 		self.previous_line = False
# 			current_adapter = self.adapters.index(self.adapter)
	
# 		current_adapter += 1	
# 		next_adapter = str(self.adapters[current_adapter])
# 		raw_interface = ip_readout[ip_readout.find(self.adapter)+len(self.adapter):ip_readout.rfind(next_adapter)]
# 			interface_lines = raw_interface.splitlines()
# 			for interface_line in interface_lines:
# 				if "IPv4" in interface_line:
# 					ip_address = interface_line.split(": ")
# 					self.ip_address = ip_address[-1]
# 				elif "Subnet" in interface_line:
# 					subnet = interface_line.split(": ")
# 					self.subnet = subnet[-1]
# 				elif "Gateway" in interface_line:
# 					if "%" in interface_line:
# 						previous_line = True
# 				elif self.previous_line == True:
# 						gateway = str(interface_line.strip())
# 						self.gateway = gateway
# 						previous_line = False

test = Interface()


# print(test.ip_address)
# print(test.adapters)
test.find_adapters()
print(test.adapters)


