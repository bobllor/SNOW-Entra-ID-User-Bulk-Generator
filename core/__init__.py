from pathlib import Path

def file_checker(path: str, *, text_file: str = None, contents: str = None) -> bool:
    '''
    Checks if the directory exists with the given path.

    Parameters
    ----------
    `text_file`

    (OPTIONAL) Checks if the text file exists in the given directory. Default is None.
    '''
    file = Path(path)

    if not Path.exists(file):
        file.mkdir(parents=True, exist_ok=True)
    
    if text_file:
        new_path = path + f'/{text_file}'
        file = Path(new_path)

        if not Path.exists(file):
            with open(new_path, 'w') as f:
                f.write(contents)

azure_template_folder = str(Path.home() / 'Downloads' / 'Azure Emails')

template_path = './templates'
email_file = 'email_template.txt'

# checks if the azure emails folder exists inside the downloads folder.
file_checker(azure_template_folder)

text = '''Hello,

A user account has been created for [FULLNAME].
A welcome email with credentials is shown below.
We appreciate your support as we continue to improve our Services.

Thank you

Subject: Welcome to TEKsystems - Microsoft Office 365 account.

Welcome to TEKsystems, [FULLNAME].

We are excited to welcome you to the team. As a team member, you have been issued a Microsoft Office 365 account.

Username: [GS_EMAIL]
PW/Credentials: [PASSWORD]

Before you can access your new user account, you will need to change your login credentials.

Changing Your Login Credentials:
    1. Go to Login.microsoftonline.com
    2. Enter your username (full email address) and the temporary credential provided.
    3. Update your credentials and confirm the change.
    4. After this change, you can access the requested applications.

If you need assistance accessing this account or have questions, please contact the Support Team via email at TGS_Hardware@Teksystems.com. or by calling (855) 698-3549.

Thank you,
TGS (TEK GLOBAL SERVICES) HARDWARE DEPOT'''

# checks if the email template folder exists inside the source folder.
file_checker(template_path, text_file=email_file, contents=text)