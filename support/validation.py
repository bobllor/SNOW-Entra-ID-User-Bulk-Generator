from .mapping import sc_keys, u_hard_keys, custom_sc_keys

def get_name(name: str, position: str = 'first') -> str:
    name = name.title().strip() if '-' not in name else name.replace('-', ' ').title().strip()
    
    names = name.split()

    if position == 'first':
        if len(names) > 1:
            return names[0]
    else:
        if len(names) > 1:
            suffixes = {'jr', 'sr', '1st', '2nd', '3rd', '4th', 'i', 'ii', 'iii', 'iv'}
            
            # ensures that suffixes to a last name are not used.
            if names[-1].lower().strip('.') in suffixes or names[-1].lower().strip('.').isdigit():
                return names[-2]

            return names[-1]

    return name

def name_validation(string: str) -> str:
    '''
    Checks for any invalid characters existing at the head of a string.
    '''
    string_list = string.split()
    for i in range(len(string_list)):
        string_list[i] = string_list[i].title().strip()

    return " ".join(string_list)

def check_columns(columns: list, *, multi_file: bool = False, second_columns: list = None) -> bool:
    '''Used to check if the files read from the selections are correct.

    Returns `False` if at least one column does not match with the base columns.

    Returns `True` if all columns matches with the base columns.

    Parameters
    ----------
    `multi_file`

    (OPTIONAL) Default `False`. Indicates whether or not this is a multi-file selection, which compares the base columns
    with additional columns.
    '''
    r_sc_keys = {value: key for key, value in sc_keys.items()}

    if not multi_file:
        if not match_columns(columns, r_sc_keys):
            return False
    else:
        r_u_hard_keys = {value: key for key, value in u_hard_keys.items()}

        # iterate over the base columns to compare to.
        iterator_one = [r_sc_keys, r_u_hard_keys]
        # iterate over the columns for comparing to.
        iterator_two = [columns, second_columns]

        for i in range(2):
            if not match_columns(iterator_two[i], iterator_one[i]):
                return False
    
    return True

def match_columns(columns: list, base_columns: dict) -> bool:
    for column in columns:
        if column not in base_columns:
            # i am sorry. for this.
            for key in custom_sc_keys:
                if key not in columns:
                    return False
    
    return True