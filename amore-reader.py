import os

# TODO: test clusters

class AmoreReader:
    
    def __init__(self, data_directory):
        self.data_directory = data_directory

    def get_set_a_ids(self, dataset_id):
        """
        Example: print('Three IDs of dataset 1, set A:', AmoreReader('./').get_set_a_ids('1')[:3])
        """
        return self.read_file(os.path.join(self.data_directory, 'amore-' + dataset_id + '-a.txt'), as_integer=True)

    def get_set_b_ids(self, dataset_id):
        """
        Example: print('Three IDs of dataset 2, set B:', AmoreReader('./').get_set_b_ids('2')[:3])
        """
        return self.read_file(os.path.join(self.data_directory, 'amore-' + dataset_id + '-b.txt'), as_integer=True)

    def get_drift_ids(self, dataset_id, subset=None):
        """
        Example: print('Three IDs with drift of dataset 1:', AmoreReader('./').get_drift_ids('1')[:3])
        """
        if subset:
            return self.read_file(os.path.join(self.data_directory, 'amore-' + dataset_id + '-drift-' + subset + '.txt'), as_integer=True)
        else:
            return self.read_file(os.path.join(self.data_directory, 'amore-' + dataset_id + '-drift.txt'), as_integer=True)

    def get_drift_tokens(self, dataset_id, subset=None):
        """
        Example: print('Drift-related tokens of dataset 1:', AmoreReader('./').get_drift_tokens('1'))
        """
        if subset:
            return self.read_file(os.path.join(self.data_directory, 'amore-' + dataset_id + '-tokens-' + subset + '.txt'))
        else:
            return self.read_file(os.path.join(self.data_directory, 'amore-' + dataset_id + '-tokens.txt'))

    def get_files(self):
        """
        Example: print('Benchmark files:', AmoreReader('./').get_files())
        """
        files = []
        for file in os.listdir(self.data_directory):
            if file.endswith('.txt'):
                files.append(file)
        return files
    
    def read_file(self, file, as_integer=False):
        data = []
        with open(file) as f:
            for line in f:
                if as_integer:
                    data.append(int(line.strip()))
                else:
                    data.append(line.strip())
        return data
