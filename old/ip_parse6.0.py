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
		self.adapters_status = {}

		
		for _line in self._lines:
			if "adapter" in _line:
				parsed_adapter = _line.split("adapter ")
				self.adapters.append(parsed_adapter[-1].replace(":",""))

		for self.adapter in self.adapters:
			try:
				_split_string = self._ip_readout.split(self.adapter,1)
				self.raw_interface = _split_string[1].split("adapter", 1)
				if "Media disconnected" in self.raw_interface[0]:
					self.adapters_status.update({self.adapter:"disconnected"})
				else:
					self.adapters_status.update({self.adapter:"connected"})
			except IndexError:
				break	

	def find_adapters_connected(self):
		self.connected_list = []
		for key in self.adapters_status.keys():
			if "disconnected" not in self.adapters_status[key]:
				self.connected_list.append(key)
		print(self.connected_list)

		for _parse in self.connected_list:
			print(_parse)
			self.parse_adapter(_parse)
			



	def parse_adapter(self, interface):
		self.interface = interface
		# current_adapter = self.adapters.index(self.adapter)
		self.previous_line = False
# 		current_adapter += 1	
# 		next_adapter = str(self.adapters[current_adapter])
		# raw_interface = ip_readout[ip_readout.find(self.adapter)+len(self.adapter):ip_readout.rfind(next_adapter)]
		_split_string = self._ip_readout.split(self.interface,1)
		self.raw_interface = _split_string[1].split("adapter", 1)
		interface_lines = self.raw_interface[0].splitlines()
		# print(interface_lines)
		for interface_line in interface_lines:
			if "IPv4" in interface_line:
				ip_address = interface_line.split(": ")
				self.ip_address = ip_address[-1]
				print(self.ip_address)
			elif "Subnet" in interface_line:
				subnet = interface_line.split(": ")
				self.subnet = subnet[-1]
				print(self.subnet)
			elif "Gateway" in interface_line:
				if "%" in interface_line:
					self.previous_line = True
			elif self.previous_line == True:
				self.gateway = str(interface_line.strip())
				print(self.gateway)
				self.previous_line = False

refresh = Interface()


# print(test.ip_address)
# print(test.adapters)
refresh.find_adapters()
# print(test.adapters_status)
refresh.find_adapters_connected()