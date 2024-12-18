import pandas as pd
import support.menu as menu
import os
from getpass import getpass
from core.csv_maker import CSVMaker
from core.email_maker import EmailMaker
from tkinter import filedialog
from pathlib import Path
from support.validation import name_validation, get_name, check_columns
from support.pwd_gen import gen_pwd
from support.mapping import sc_keys
from support.menu import format_text as ft

down_path = str(Path.home() / 'Downloads')
with open('./templates/email_template.txt', 'r') as file:
    template = file.read()

clear = lambda: os.system('cls' if os.name == 'nt' else 'clear')
pause = lambda: getpass('\t\nPress "Enter" to continue.')

def select_file(*, vtb: bool = True) -> str:
    '''Prompts a dialog to select a file of csv.

    If no file is given or a non-csv file is used, then `FileNotFoundError` is raised.
    '''
    ft('\nSelecting a file...')

    title = 'Select a sc_req_item file' if vtb else 'Select a u_hardware_support file'

    selected_file = filedialog.askopenfilename(initialdir=down_path, filetypes=[('CSV Files', '*.csv')]
                                               , title=title)

    if not selected_file or Path(selected_file).suffix != '.csv':
        raise FileNotFoundError
    
    return selected_file

def make_new_df(full_names:list, username: list, generated_pwds: list, f_names: list, l_names: list, countries):
    '''
    Parameters
    -----
    `full_names`: A `list` of `str` of the full names of a user.
    
    `username`: A `list` of `str` of the username of a user. The domain name is either @teksystemsgs.com or @ext.aerotek.com.

    `generated_pwds`: A `list` of `str` that contains the randomly generated passwords for the user.

    `f_names`: A `list` of `str` containing the first name of the users.

    `l_names`: A `list` of `str` containing the last name of the users.
    '''

    df = pd.DataFrame({'Name [displayName] Required': full_names, 'User name [userPrincipalName] Required': username,
            'Initial password [passwordProfile] Required': generated_pwds, 'Block sign in (Yes/No) [accountEnabled] Required': 'No', 
            'First name [givenName]': f_names, 'Last name [surname]': l_names,
            'Usage location [usageLocation]': countries})
    
    return df

if __name__ == '__main__':
    while True:
        clear()

        option = menu.choice(valid_options={'m', 's', 'q', 'i'})

        try:
            if option == 'm':
                csv_file_vtb = select_file()
                csv_file_builds = select_file(vtb=False)

                # VTB CSV file, this should start with "sc_req_item"
                df_vtb = pd.read_csv(csv_file_vtb)

                # BUILDS CSV file, this should start with "u_hardware_support"
                df_builds = pd.read_csv(csv_file_builds)
                
                if check_columns(list(df_vtb.columns), multi_file=True, second_columns=list(df_builds.columns)):
                    df = df_vtb[df_vtb['number'].isin(df_builds['u_ritm_number'])]
                else:
                    raise FileNotFoundError
                
            elif option == 's':
                csv_file = select_file()

                df = pd.read_csv(csv_file)

                if not check_columns(df):
                    raise FileNotFoundError
                
            elif option == 'i':
                ritm = input('Enter the RITM: ')
                name = input('Enter their name: ')

                first = get_name(name)
                last = get_name(name, position='last')

                is_actalent = input('Is the user an Actalent employee (Y/N): ').upper()
                
                while is_actalent not in ['Y', 'N']:
                    is_actalent = input('Is the user an Actalent employee (Y/N): ').upper()

                flag = False if is_actalent == 'N' else True
                domain = '@teksystemsgs.com' if not flag else '@ext.aerotek.com'

                user = f'{first}.{last}{domain}'

                country = input('Enter the country (US/CA): ').upper()

                if country not in ['US', 'CA']:
                    country = 'US'

                pwd = gen_pwd()

                df = make_new_df([name], [user], [pwd], [first], [last], [country])

                em = EmailMaker(down_path, template, [name], [pwd], [user], [ritm])
                em.generate_email()

                csvm = CSVMaker(df, down_path)
                csvm.create_csv()

                ft(f'\nFinished generating accounts in {down_path + r"\Azure_Emails"}.')
                pause()
                
            else:
                break
            
            if option != 'i':
                full_f_names = df.loc[:, sc_keys['first_name']].apply(name_validation)
                full_l_names = df.loc[:, sc_keys['last_name']].apply(name_validation)

                f_names = full_f_names.apply(get_name, args=('first',))
                l_names = full_l_names.apply(get_name, args=('last',))
                full_names = f_names + ' ' + l_names

                countries = df.iloc[:, 6]
                generated_pwds = []
                for _ in range(df['number'].size):
                    generated_pwds.append(gen_pwd())

                # generate the usernames in the dataframe based on the organization value.
                org_key = sc_keys['org']

                # why does this happen... thanks pandas.
                df = df.copy()
                df.loc[df[org_key].isin(['GS', 'Staffing']), 'Username'] = f_names + '.' + l_names + '@teksystemsgs.com'
                df.loc[df[org_key].isin(['Actalent', 'Aerotek', 'Aston Carter', 'MLA']), 'Username'] = f_names + '.' + l_names + '@ext.aerotek.com'

                usernames = df['Username'].to_list()

                new_df = make_new_df(full_names.tolist(), usernames, generated_pwds, f_names.to_list(), l_names.to_list(), countries.to_list())

                em = EmailMaker(down_path, template, full_names.to_list(), generated_pwds, usernames, df['number'].tolist())
                em.generate_email()

                csvm = CSVMaker(new_df, down_path)
                csvm.create_csv()

                ft(f'\nFinished generating accounts in {down_path + r"\Azure_Emails"}.')
                pause()

        except FileNotFoundError:
            clear()

            print(ft('\n\tWARNING: An incorrect file type was detected.'))
            print(ft('Only .csv files are allowed in the program.'))
            pause()