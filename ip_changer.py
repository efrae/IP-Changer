import tkinter as tk
import subprocess
import os
import time
import json
from ip_parse import Interface
from presets import Preset

class Application(tk.Frame):
	def __init__(self, master=None):
		super().__init__(master)
		self.create_path()
		self.interface_list = []
		self.master = master
		self.master.title("IP Changer")
		self.master.resizable(False, False)
		self.menubar = tk.Menu(master) 
		self.master.config(menu=self.menubar)
		self.return_text = ''
		self.interface = Interface()
		self.create_labels()
		self.create_entrys()
		self.create_apply_btn()
		self.create_dhcp_checkbox()
		self.create_refresh_btn()
		self.create_menu()
		self.pack()
		self.center()
		self.create_show_disabled_checkbox()
		self.check_list()
		self.refresh_values()
		self.refresh_presets()

	def create_path(self):
		_current_directory = os.getcwd()
		self.preset_directory = os.path.join(_current_directory, r'presets')
		if not os.path.exists(self.preset_directory):
			os.makedirs(self.preset_directory)

	def check_list(self):
		self.interface._send_command()
		if self.set_show_disabled.get() == 1:
			self.interface_list = self.interface.adapters
		else:
			self.interface_list = self.interface.connected_list
		self.create_listbox()

	def center(self):
		w = self.master.winfo_reqwidth()
		h = self.master.winfo_reqheight()
		ws = self.master.winfo_screenwidth()
		hs = self.master.winfo_screenheight()
		x = (ws/2) - (w)
		y = (hs/2) - (h)
		self.master.geometry('+%d+%d' % (x, y)) ## this part allows you to only change the location

	def create_listbox(self):
		self._listbox_index = 0
		self.interface_listbox = tk.Listbox(self, exportselection=False, width=40)
		self.interface_listbox.grid(row=1, column=0, rowspan=8, columnspan=3, 
			pady=15, padx=10)
		for item in self.interface_list:
			self.interface_listbox.insert(tk.END ,item)
		self.interface_listbox.select_set(0)
		self.interface_listbox.bind("<<ListboxSelect>>", self.report_listbox)

	def report_listbox(self, event):
		self._listbox_index = int(self.interface_listbox.curselection()[0])
		self.refresh_values()

	def refresh_values(self):
		self.interface._send_command()
		
		self.interface_text = (self.interface_list[self._listbox_index])
		self.current_interface.configure(text=self.interface_text)
		# Parse IP
		self.interface.parse_adapter(self.interface_text)
		self.check_dhcp()
		self.enable_fields()
		# Pass Pared IP to Widgets

		###### Unnecassary Vars

		self.current_ip_address = self.interface.ip_address
		self.entry_ip.delete(0, tk.END)
		self.entry_ip.insert(0, self.current_ip_address)
		# Subnet
		self.current_subnet = self.interface.subnet
		self.entry_subnet.delete(0, tk.END)
		self.entry_subnet.insert(0, self.current_subnet)
		# Gateway
		self.current_gateway = self.interface.gateway
		self.entry_gateway.delete(0, tk.END)
		self.entry_gateway.insert(0, self.current_gateway)
		# Check DHCP
		if self.read_dhcp == True:
			self.disable_fields()
		self.error_text["text"] = ''

	def checkbtn_dhcp(self):
		if self.set_dhcp_on.get() == 1:
			self.read_dhcp = True
			self.disable_fields()
		else:
			self.read_dhcp = False
			self.enable_fields()

	def check_dhcp(self):
		# if DHCP then Grey out text
		
		if self.interface.dhcp_status == True:
			self.read_dhcp = True
			self.set_dhcp_on.set(1)
		else:
			self.read_dhcp = False
			self.set_dhcp_on.set(0)

	def create_labels(self):
		# Create Text for IP
		_enter_ip_label = tk.Label(self, text="IP Address:")
		_enter_ip_label.grid(row=5, column=3, sticky="E")

		# Create Text for Subnet
		_enter_subnet_label = tk.Label(self, text="Subnet:")
		_enter_subnet_label.grid(row=6, column=3, sticky="E")

		 # Create Text for Gateway
		_enter_gateway_label = tk.Label(self, text="Gateway:")
		_enter_gateway_label.grid(row=7, column=3, sticky="E")

		# Create Text for IP header
		self.current_interface = tk.Label(self, text="Select an Interface", font=8)
		self.current_interface.grid(row=1, column=3, columnspan=4, sticky="W", padx=5)

		self.error_text = tk.Label(self, text='', wraplength=225)
		self.error_text.grid(row=2, column=3, columnspan=4, rowspan=2)

	def create_entrys(self):
	    # Create IP Entry Field
	    self.entry_ip = tk.Entry(self, width=25)
	    self.entry_ip.grid(row=5, column=4, 
	    	columnspan=2, padx=10)

	    # Create Subnet Entry Field
	    self.entry_subnet = tk.Entry(self, width=25)
	    self.entry_subnet.grid(row=6, column=4, 
	    	columnspan=2, padx=10)

	    # Create Gateway Entry Field
	    self.entry_gateway = tk.Entry(self, width=25)
	    self.entry_gateway.grid(row=7, column=4, 
	    	columnspan=2, padx=10)

	def create_apply_btn(self):
	    self.apply_btn = tk.Button(self, text="Apply", 
	    	width=15, command=self.apply_settings)
	    self.apply_btn.grid(row=9, column=4, padx=10, pady=10)

	def create_refresh_btn(self):
	    _refresh_btn = tk.Button(self, text="Refresh", 
	    	command=self.check_list)
	    _refresh_btn.grid(row=9, column=1, padx=10, pady=10)

	def create_dhcp_checkbox(self):
		self.set_dhcp_on = tk.IntVar()
		_dhcp_btn = tk.Checkbutton(self, text="Set DHCP", 
			variable=self.set_dhcp_on, command=self.checkbtn_dhcp)
		_dhcp_btn.grid(row=9, column=3, padx=10, pady=10)

	def create_menu(self):
		_file_menu = tk.Menu(self.menubar, tearoff=0)
		_file_menu.add_command(label="Exit", command=root.quit)
		self.menubar.add_cascade(label="File", menu=_file_menu)

		_presets_menu = tk.Menu(self.menubar, tearoff=0)
		self.menubar.add_cascade(label="Presets", menu=_presets_menu)
		# Create Presets Submenu
		_presets_menu.add_command(label="Save Preset", command=self.save_preset_pop)

		self.load_presets_menu = tk.Menu(_presets_menu, tearoff=0)

		_presets_menu.add_cascade(label="Load Preset", menu=self.load_presets_menu)

		_presets_menu.add_command(label="Manage Presets", command=self.manage_pop)

	def manage_pop(self):
		self._manage_pop = tk.Toplevel(takefocus=True)
		self.win_position_x = self.master.winfo_x()
		self.win_position_y = self.master.winfo_y()
		self._manage_pop.geometry("+%d+%d" % (self.win_position_x + 20, self.win_position_y + 50))
		_del_msg = tk.Message(self._manage_pop,
			text="Select Presets below to delete.", width=250)
		_del_msg.grid(column=0, row=1, columnspan=3, padx=10, pady=10)

		self.manage_close = tk.Button(self._manage_pop, text="Close", command=self._manage_pop.destroy)
		self.manage_close.grid(row=12, column=0, padx=10, pady=10)

		self.manage_delete = tk.Button(self._manage_pop, text="Delete", command=self.delete_preset)
		self.manage_delete.grid(row=12, column=2, padx=10, pady=10)

		self.manage_listbox()


	def manage_listbox(self):

		self._manage_listbox = tk.Listbox(self._manage_pop, exportselection=False, width=40)
		self._manage_listbox.grid(row=2, column=0, rowspan=8, columnspan=3, 
			pady=15, padx=10)

		self.refresh_manage()

		self._manage_listbox_index = 0
		self._manage_listbox.select_set(0)
		self._manage_listbox.bind("<<ListboxSelect>>", self.report_manage_listbox)

	def refresh_manage(self):
		self.refresh_presets()
		for _managed_presets in self.saved_presets:
			self._manage_listbox.insert(tk.END , _managed_presets)

		
	def report_manage_listbox(self, event):
		self.manage_listbox_index = int(self._manage_listbox.curselection()[0])

	def delete_preset(self):
		manage_selected = ("preset_"+self.saved_presets[self.manage_listbox_index]+".json")
		manage_selected = manage_selected.replace(" ","_")
		print(manage_selected)
		os.path.join(self.preset_directory, manage_selected)
		os.remove(self.preset_directory+"\\"+manage_selected)
		self._manage_listbox.delete(tk.ACTIVE)
		self.refresh_presets()


	def save_preset_pop(self):
		self._save_preset_pop = tk.Toplevel(takefocus=True)

		_msg = tk.Message(self._save_preset_pop, 
			text="What would you like to name this preset?", width=250)
		_msg.grid(column=1, row=1, columnspan=3, padx=10, pady=10)
		self.win_position_x = self.master.winfo_x()
		self.win_position_y = self.master.winfo_y()
		self._save_preset_pop.geometry("+%d+%d" % (self.win_position_x + 50, self.win_position_y + 50))

		# Create Entry Field
		self.preset_entry = tk.Entry(self._save_preset_pop, 
			width=25)
		self.preset_entry.grid(row=2, column=1, 
			columnspan=3, padx=10)

		_cancel = tk.Button(self._save_preset_pop, text="Cancel", 
			command=self._save_preset_pop.destroy)
		_cancel.grid(column=1, row=3, padx=10, pady=10)

		_save = tk.Button(self._save_preset_pop, text="Save", 
			command=self.save_preset)
		_save.grid(column=3, row=3, padx=10, pady=10)

	def save_preset(self):
		_preset_name = self.preset_entry.get()
		_preset_ip = self.entry_ip.get()
		_preset_subnet = self.entry_subnet.get()
		_preset_gateway = self.entry_gateway.get()
		_preset = Preset(_preset_name, _preset_ip, _preset_subnet, _preset_gateway)
		if len(self.saved_presets) <= 10:
			_preset.add_preset_json(_preset_name)
		else:
			self.error = tk.Toplevel(takefocus=True)
			self.error.attributes("-topmost", True)
			self.too_many_presets = tk.Message(self.error, width=200, text="Cannot Save!\n\nMore then 10 presets exist, please delete some!")
			self.too_many_presets.grid(column=1, row=1, columnspan=3, padx=10, pady=10)
			self.okay_error = tk.Button(self.error, text="Okay", width=50, command=self.error.destroy)
			self.win_position_x = self.master.winfo_x()
			self.win_position_y = self.master.winfo_y()
			self.error.geometry("+%d+%d" % (self.win_position_x + 50, self.win_position_y + 50))
			self.okay_error.grid(column=1, row=2, columnspan=3, padx=10, pady=10)
		self._save_preset_pop.destroy()
		self.refresh_presets()

	def refresh_presets(self):
		self.saved_presets = []
		_presets = []
		self.load_presets_menu.delete(0, [10])
		for (root,dirs,files) in os.walk(self.preset_directory):
			_presets = files
		for _preset in _presets:
			if _preset.endswith('.json'):
				_load_preset_name = _preset.replace(".json", "")
				_load_preset_name = _load_preset_name.replace("preset_", "")
				_load_preset_name = _load_preset_name.replace("_", " ")
				self.load_presets_menu.add_command(label=_load_preset_name.title(),
					 command=lambda arg=_preset : self.load_preset(arg))
				self.saved_presets.append(_load_preset_name)


	def load_preset(self, present_filename):
		self.read_dhcp = False
		self.enable_fields()
		self.set_dhcp_on.set(0)
		with open(f"./presets/{present_filename}", 'r') as f:
			data = json.load(f)
			for preset_dict in data.values():
				self.entry_ip.delete(0, tk.END)
				self.entry_ip.insert(0, preset_dict['ip'])
				self.entry_subnet.delete(0, tk.END)
				self.entry_subnet.insert(0, preset_dict['subnet'])
				self.entry_gateway.delete(0, tk.END)
				self.entry_gateway.insert(0, preset_dict['gateway'])

	def disable_fields(self): 
		self.entry_ip.config(state=tk.DISABLED)
		self.entry_subnet.config(state=tk.DISABLED)
		self.entry_gateway.config(state=tk.DISABLED)

	def enable_fields(self):
		self.entry_ip.config(state=tk.NORMAL)
		self.entry_subnet.config(state=tk.NORMAL)
		self.entry_gateway.config(state=tk.NORMAL)

	def create_show_disabled_checkbox(self):
		self.set_show_disabled = tk.IntVar()
		self.show_disabled_btn = tk.Checkbutton(self, text="Show Disabled",
			 variable=self.set_show_disabled, command=self.check_list)
		self.show_disabled_btn.grid(row=9, column=0, padx=10, pady=10)

	###### Unnecassary Def
	def get_ip(self):
	    #Get IP
	    self.ip_address = self.entry_ip.get()
	    #Get IP
	    self.subnet = self.entry_subnet.get()
	    #Get IP
	    self.gateway = self.entry_gateway.get()

	def apply_settings(self):
		self.error = ""
		if self.set_dhcp_on.get() == 1:
			self.set_dhcp()
			self.after(4000, self.refresh_values)
		else:
			self.set_static()
			self.after(4000, self.refresh_values)

	def set_static(self):
		self.get_ip()
		time.sleep(.1)
		###### Unnecassary Vars
		self.ipset_command = f"netsh int ip set address {self.interface_text} static {self.ip_address} {self.subnet} {self.gateway} 1"
		self.cmd = subprocess.Popen(self.ipset_command, shell=True, 
			stdout=subprocess.PIPE)
		self.check_errors()
  
	def set_dhcp(self):
		self.dhcpset_command = f"netsh interface ip set address {self.interface_text} dhcp"
		self.cmd = subprocess.Popen(self.dhcpset_command, shell=True, 
			stdout=subprocess.PIPE, stderr=subprocess.PIPE)
		self.check_errors()

	def check_errors(self):
		_return_text = self.cmd.communicate()[0]
		_return_text = _return_text.decode("utf-8")
		_return_text = _return_text.strip()
		if str(_return_text) == "":
			self.error_text.config(text="Success!", foreground="green")
		else:
			self.error_text.config(text=_return_text, foreground="red")


root = tk.Tk()
if __name__ == '__main__':
	app = Application(master=root)
	app.mainloop()
