from pandas import DataFrame
from time import strftime, localtime
from datetime import datetime

'''
Creates the CSV for the bulk Azure process.
'''

class CSVMaker:
    '''
    Class File that creates the output files for the csv and email text.
    '''
    def __init__(self, df: DataFrame, path: str):
        self.path = path
        self.df = df

    def create_csv(self):
        date = datetime.now().strftime('%Y-%m-%dT%H-%M-%S')
        csv_file_path = f'{self.path}/Azure_Emails/'
        file_name = f'csv_bulk-{date}.csv'
        
        with open(csv_file_path + file_name, 'w') as file:
            version = 'version:v1.0\n'
            file.write(version)

        self.df.to_csv(path_or_buf=csv_file_path + f'csv_bulk-{date}.csv', index=False, mode='a')