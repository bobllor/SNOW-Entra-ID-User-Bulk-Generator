import string, random

def gen_pwd() -> str:
    '''
    Generates a random password.
    '''
    return "".join(gen_random_char())

def gen_random_char() -> list:
    # the password MUST contain at least 1 upper and 1 lower, although the random generator has a very high chance
    # to generate both, this is a safeguard to ensure it is 100%.
    min_letters = [random.choice(string.ascii_uppercase), random.choice(string.ascii_lowercase)]

    random_letters = random.choices(string.ascii_letters, k=4)
    random_punctuations = random.choices(string.punctuation, k=6)
    # remove - % ' $ from the list of choices.
    random_punctuations = [c for c in random_punctuations if c not in '-%\'$']

    random_numbers = [str(random.randint(0, 9)) for _ in range(10)]

    combined_list = random_letters + random_punctuations + random_numbers
    temp = -1
    for c in min_letters:
        while True:
            index = random.randint(0, len(combined_list) - 1)
            # ensures that the random index is not the same index.
            if index != temp:
                temp = index
                break

        combined_list[index] = c

    random.shuffle(combined_list)
    char_list = combined_list[:20]
    
    return char_list