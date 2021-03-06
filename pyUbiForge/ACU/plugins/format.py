import os
from pyUbiForge.misc.plugins import BasePlugin
from typing import Union, List


class Plugin(BasePlugin):
	plugin_name = 'Format'
	plugin_level = 4
	file_type = '*'

	def run(self, py_ubi_forge, file_id: Union[str, int], forge_file_name: str, datafile_id: int, options: Union[List[dict], None] = None):
		data = py_ubi_forge.temp_files(file_id, forge_file_name, datafile_id)
		if data is None:
			py_ubi_forge.log.warn(__name__, f"Failed to find file {file_id:016X}")
			return
		if not os.path.isdir(py_ubi_forge.CONFIG.get('dumpFolder', 'output')):
			os.makedirs(py_ubi_forge.CONFIG.get('dumpFolder', 'output'))
		out_file = open(
			os.path.join(
				py_ubi_forge.CONFIG.get('dumpFolder', 'output'),
				f'{py_ubi_forge.game_functions.game_identifier}_{data.file_name}_{file_id:016X}.format'
			), 'w'
		)
		py_ubi_forge.read_file(data.file, out_file)
		py_ubi_forge.log.info(__name__, "Finished Formatting")
