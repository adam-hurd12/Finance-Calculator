from datetime import datetime as dt
import constants


# function to return user input within a given table of correct inputs; will always return a value within the correct table
def string(prompt, correct, numbered=False):
    while True:
        choice = str(input(f'\n{prompt}     ')).lower()
        # check if input is in the correct table, regardless of whether the input can be a number
        if choice in correct: return choice
        # check for number user inputs that can be integer <= table length
        if numbered and choice.isnumeric() and int(choice) <= len(correct) and int(choice) > 0: return correct[int(choice)-1]

        print(constants.NOT_VALID)


# function to return only int user input, within an optional range
def number(prompt, inclusive=True, mini=0, maxi=1000000):
    while True:
        choice = str(input(f'\n{prompt}     ')).lower()

        if choice.isnumeric():
            # check for inclusive values (choice can be equal to bounds)
            if inclusive and mini <= int(choice) and int(choice) <= maxi: return int(choice)
            # check for exclusive values (choice cannot be equal to bounds)
            elif mini < int(choice) and int(choice) < maxi: return int(choice)
            
        print(constants.NOT_VALID)


# function to return a validated user inputted date
def date(prompt):
    while True:
        choice = str(input(f'\n{prompt}     ')).lower()

        try: return dt.strptime(choice, constants.DATE_FORMAT)
        except: print(contsants.NOT_VALID)