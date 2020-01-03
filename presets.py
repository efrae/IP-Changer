import json

class Preset:

	def __init__(self, presetname, presetip, presetsubnet, presetgateway):
		self.presetname = presetname
		self.presetname = {self.presetname:{"ip":presetip, 
			"subnet":presetsubnet, "gateway":presetgateway}}

	def add_preset_json(self, presetname):	
		filename = f'preset_{presetname.replace(" ","_")}.json'
		with open(f"./presets/{filename}", 'w') as f:
			try:
				data = json.load(f)
				print(data)
			except:
				json.dump(self.presetname, f)
			