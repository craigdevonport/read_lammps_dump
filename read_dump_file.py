import numpy as np

def read_dump(filename):
	dump_file = open(filename,'r')
	mode = ''
	atom_headers=[]
	data = []
	step_data = {}
	for line in dump_file:
		if 'TIMESTEP' in line:
			mode = 'TIMESTEP'
			if step_data != {}:
				data.append(step_data)
			step_data = {}
		elif 'NUMBER OF ATOMS' in line:
			mode = 'NATOMS'
		elif 'BOX BOUNDS' in line:
			mode = 'BBOX'
		elif 'ITEM: ATOMS' in line:
			mode = 'ATOMS'
			line_parts = line.split(' ')
			atom_headers = line_parts[2:-1]
			step_data['ATOMS'] = []
		elif mode == 'TIMESTEP':
			step_data['TIMESTEP'] = int(line)
		elif mode == 'NATOMS':
			step_data['NATOMS'] = int(line)
		elif mode == 'ATOMS':
			atom_info = {}
			line_parts = line.split(' ')
			for i in range(len(atom_headers)):
				atom_info[atom_headers[i]] = line_parts[i]
			step_data['ATOMS'].append(atom_info)

	if step_data != {}:
		data.append(step_data)

	return data

def convert_to_ndarray(dump_data):
	timesteps = len(dump_data)
	natoms = dump_data[0]['NATOMS']
	atom_headers = list(dump_data[0]['ATOMS'][0].keys())

	array = np.empty((timesteps, natoms, len(atom_headers)))

	for t in range(timesteps):
		for i in range(natoms):
			for h in range(len(atom_headers)):
				array[t][i][h] = dump_data[t]['ATOMS'][i][atom_headers[h]]

	return array, {'timesteps':timesteps, 'natoms':natoms, 'atom_headers':atom_headers}
