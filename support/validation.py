from .mapping import sc_keys, u_hard_keys

def get_name(name: str, position: str) -> str:
    name = name.title().strip()

    # if there are multiple names.
    if '-' in name:
        names = name.split('-')
    else:
        names = name.split()

    if position == 'first':
        if len(names) > 1:
            return names[0]
    else:
        if len(names) > 1:
            suffixes = {'jr', 'sr', '1st', '2nd', '3rd', '4th', 'I', 'II', 'III', 'IV'}
            
            # ensures that suffixes to a last name are not used.
            if name[-1].lower().strip('.') in suffixes:
                return name[-2]

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
    # single file, used to create accounts with orders that is requesting an azure account.
    base_columns_sc = [sc_keys['number'], sc_keys['opened_at'], sc_keys['active'], sc_keys['opened_by'],    
        sc_keys['first_name'], sc_keys['last_name'], sc_keys['country'], sc_keys['short_description'], sc_keys['org']]
    
    # multi file, used to filter out the VTB columns.
    base_columns_builds = [u_hard_keys['ritm'], u_hard_keys['build'], u_hard_keys['state'],
                           u_hard_keys['opened_on'], u_hard_keys['user'], u_hard_keys['built_by'],
                           u_hard_keys['verified_by']]
    
    if not multi_file:
        result = match_columns(columns, base_columns_sc)

        if not result:
            return False
    else:
        # iterate over the base columns to compare to.
        iterator_one = [base_columns_sc, base_columns_builds]
        # iterate over the columns for comparing to.
        iterator_two = [columns, second_columns]

        for i in range(2):
            result = match_columns(iterator_two[i], iterator_one[i])

            if not result:
                return False
    
    return True

def match_columns(columns: list, base_columns: list) -> bool:
    for i, column in enumerate(columns):
        if column != base_columns[i]:
            return False
    
    return True