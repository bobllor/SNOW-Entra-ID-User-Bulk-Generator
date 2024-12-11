from pathlib import Path
from datetime import datetime

class EmailMaker:
    '''
    Generate the "Welcome" emails to send for Azure accounts.

    Requires the path, email template, full name, password, username, and RITM.
    '''
    def __init__(self, path: str, email_template, name: list, password: list, username: list, ritms: list):
        self.email_template = email_template
        self.down_path = path
        self.keys = {'FULLNAME': name, 'GS_EMAIL': username, 'PASSWORD': password}
        self.ritms = ritms
    
    def generate_email(self) -> None:
        # used to reset the template after every loop
        base_template = self.email_template
        date = datetime.now().strftime('%Y-%m-%dT%H-%M-%S')

        file_path = self.down_path + f'/Azure_Emails/{date}'
        if not Path.exists(Path(file_path)):
            Path(file_path).mkdir(parents=True, exist_ok=True)

        for i, ritm in enumerate(self.ritms):
            for key, value in self.keys.items():
                self.email_template = self.email_template.replace(f'[{key}]', value[i])
            
            with open(f'{file_path}/{self.keys['FULLNAME'][i]} {ritm}.txt', 'w') as file:
                file.write(self.email_template)
            
            self.email_template = base_template