import tkinter as tk
import subprocess
import os
import time
from ip_parse import Interface

class Application(tk.Frame):
	def __init__(self, master=None):
	    super().__init__(master)
	    self.interface_list = []
	    self.master = master
	    self.interface = Interface()
	    self._listbox_index = 0
	    self.pack()
	    self.create_listbox()
	    self.interface_listbox.select_set(0)
	    self.create_labels()
	    self.create_entrys()
	    self.create_apply_btn()
	    self.create_dhcp_checkbox()
	    self.check_events()
	    self.create_refresh_btn()
	    self.create_show_disabled_checkbox()
	    self.refresh_values()

	def create_listbox(self):
		self.interface_listbox = tk.Listbox(self)
		self.interface_listbox["exportselection"] = False
		self.interface_listbox.grid(row=1, column=0, rowspan=4, columnspan=2)
		self.interface._send_command()
		for item in self.interface.connected_list:
			self.interface_listbox.insert(tk.END ,item)

	def check_events(self):
		self.interface_listbox.bind("<<ListboxSelect>>", self.report_listbox)

	def report_listbox(self, event):
		
		try:
			self._listbox_index = int(self.interface_listbox.curselection()[0])
		except IndexError:
			pass 
		self.refresh_values()

	def refresh_values(self):
		print("Fresh!")
		self.interface._send_command()
		self.interface_text = (self.interface.connected_list[self._listbox_index])
		self.current_interface.configure(text=self.interface_text)
		# Parse IP
		self.interface.parse_adapter(self.interface_text)
		# Pass Pared IP to Widgets
		self.current_ip_address = self.interface.ip_address
		# self.current_ip_label.configure(text=self.current_ip_address)
		self.entry_ip.delete(0, tk.END)
		self.entry_ip.insert(0, self.current_ip_address)
		# Subnet
		self.current_subnet = self.interface.subnet
		# self.current_subnet_label.configure(text=self.current_subnet)
		self.entry_subnet.delete(0, tk.END)
		self.entry_subnet.insert(0, self.current_subnet)
		# Gateway
		self.current_gateway = self.interface.gateway
		# self.current_gateway_label.configure(text=self.current_gateway)
		self.entry_gateway.delete(0, tk.END)
		self.entry_gateway.insert(0, self.current_gateway)

	def create_labels(self):
	    # Create Text for IP
	    self.enter_ip_label = tk.Label(self)
	    self.enter_ip_label["text"] = "IP Address:"
	    self.enter_ip_label.grid(row=2, column=2)
	    self.enter_ip_label.grid(sticky="E")

	    # Create Text for Subnet
	    self.enter_subnet_label = tk.Label(self)
	    self.enter_subnet_label["text"] = "Subnet:"
	    self.enter_subnet_label.grid(row=3, column=2)
	    self.enter_subnet_label.grid(sticky="E")

	     # Create Text for Gateway
	    self.enter_gateway_label = tk.Label(self)
	    self.enter_gateway_label["text"] = "Gateway:"
	    self.enter_gateway_label.grid(row=4, column=2)
	    self.enter_gateway_label.grid(sticky="E")

	    # Create Text for IP header
	    self.current_interface = tk.Label(self)
	    self.current_interface["text"] = "Select an Interface"
	    self.current_interface.grid(row=1, column=3)

	#       # Create Text for IP readout
	#       self.current_ip_label = tk.Label(self)
	#      	self.current_ip_address = ""
	#       self.current_ip_label["text"] = self.current_ip_address
	#       self.current_ip_label.grid(row=2, column=4, padx=100)

		# # Create Text for Subnet readout
	#       self.current_subnet_label = tk.Label(self)
	#       self.current_subnet = ""
	#       self.current_subnet_label["text"] = self.current_subnet
	#       self.current_subnet_label.grid(row=3, column=4, padx=100)

	#       # Create Text for Gateway readout
	#       self.current_gateway_label = tk.Label(self)
	#       self.current_gateway = ""
	#       self.current_gateway_label["text"] = self.current_gateway
	#       self.current_gateway_label.grid(row=4, column=4, padx=100)

	def create_entrys(self):
	    # Create IP Entry Field
	    self.entry_ip = tk.Entry(self)
	    self.entry_ip.grid(row=2, column=3, 
	    	columnspan=2, padx=5)

	    # Create Subnet Entry Field
	    self.entry_subnet = tk.Entry(self)
	    self.entry_subnet.grid(row=3, column=3, 
	    	columnspan=2, padx=5)

	    # Create Gateway Entry Field
	    self.entry_gateway = tk.Entry(self)
	    self.entry_gateway.grid(row=4, column=3, 
	    	columnspan=2, padx=5)

	def create_apply_btn(self):
	    self.apply_btn = tk.Button(self)
	    self.apply_btn["text"] = "Apply"
	    self.apply_btn["command"] = self.apply_settings
	    self.apply_btn.grid(row=5, column=3, padx=10, pady=10)

	def create_refresh_btn(self):
	    self.refresh_btn = tk.Button(self)
	    self.refresh_btn["text"] = "Refresh"
	    self.refresh_btn["command"] = self.create_listbox
	    self.refresh_btn.grid(row=5, column=1, padx=10, pady=10)

	def create_dhcp_checkbox(self):
		self.set_dhcp_on = tk.IntVar()
		self.dhcp_btn = tk.Checkbutton(self)
		self.dhcp_btn["text"] = "Set DHCP"
		self.dhcp_btn["variable"] = self.set_dhcp_on
		self.dhcp_btn.grid(row=5, column=2, padx=10, pady=10)

	def create_show_disabled_checkbox(self):
		self.set_show_disabled = tk.IntVar()
		self.show_disabled_btn = tk.Checkbutton(self)
		self.show_disabled_btn["text"] = "Show Disabled"
		self.show_disabled_btn["variable"] = self.set_show_disabled
		self.show_disabled_btn.grid(row=5, column=0, padx=10, pady=10)

	def get_ip(self):
	    #Get IP
	    self.ip_address = self.entry_ip.get()
	    #Get IP
	    self.subnet = self.entry_subnet.get()
	    #Get IP
	    self.gateway = self.entry_gateway.get()

	def apply_settings(self):
		if self.set_dhcp_on.get() == 1:
			self.set_dhcp()
			self.after(1000, self.refresh_values)
			
		else:
			self.set_static()
			self.after(4000, self.refresh_values)
			
			

	def set_static(self):
	    self.get_ip()
	    time.sleep(.1)
	    self.ipset_command = f"netsh int ip set address {self.interface_text} static {self.ip_address} {self.subnet} {self.gateway} 1"
	    subprocess.call(self.ipset_command, shell=True,)

	def set_dhcp(self):
	    self.dhcpset_command = f"netsh interface ip set address {self.interface_text} dhcp"
	    subprocess.call(self.dhcpset_command, shell=True,)



root = tk.Tk()

app = Application(master=root)
app.master.title("IP Changer")
# app.master.geometry("300x100")
app.master.resizable(False, False)
app.check_events()
app.mainloop()
