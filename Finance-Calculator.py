# program to calculate different stats for finances


from datetime import datetime as dt, timedelta
from dateutil.relativedelta import relativedelta


# constant values
NOT_VALID = '\nPlease enter a valid value.'
pay_frequency = ['weekly', 'bi-weekly', 'monthly']
num_paychecks = [52, 26, 12]
weeks_between = [1, 2, 4]
days_in_month = 365 // 12
YES = ['yes', 'y']
NO = ['no', 'n']
QUIT = ['quit', 'q']
PRE = ['pre', 'pre-tax']
POST = ['post', 'post-tax']
DATE_FORMAT = '%d/%m/%y'



# main
def main():
    print('Welcome to finance calculator. Let\'s start with calculating your take-home pay.')

    today = dt.now()

    already_earnt = get_int_input(f'\nHow much have you earnt this tax year so far, since April {today.year}?')

    is_pre_tax = get_input('\nWill you be inputting pay pre-tax or post-tax? (pre/post)', PRE + POST)

    # calculate all data needed for annual wage
    freq = get_input('\nHow often do you get paid?\n1. Weekly\n2. Bi-weekly\n3. Monthly\nChoice:', pay_frequency, True)
    avg_wage = get_int_input(f'\nWhat is the average pay per {freq} paycheck?')
    weeks_to_next_paycheck = weeks_between[pay_frequency.index(freq)]

    # calculate closest paycheck dates
    last_paycheck_date = get_date_input('\nWhen was your last paycheck (dd/mm/yy)?')
    next_paycheck_date = timedelta(weeks=weeks_to_next_paycheck) + last_paycheck_date

    # calculate saving deadline
    deadline_date = get_date_input('\nWhen are you trying to save money by? (dd/mm/yy)')
    weeks_to_deadline = (deadline_date - dt.now()).days // 7
    # calculate wage between next paycheck and saving deadline
    wage = (weeks_to_deadline / weeks_between[pay_frequency.index(freq)]) * avg_wage
    total_earnt = wage + already_earnt
    
    print(f'\nYour next paycheck will be on {next_paycheck_date.strftime(DATE_FORMAT)}.')
    print(f'\nOn average, you will earn {wage} in {weeks_to_deadline} weeks from now until your saving deadline, for a total of £{total_earnt}.')

    # calculate amount of tax to be paid
    if is_pre_tax in POST: 
        after_tax = total_earnt
    else:
        print('\nCalculating your tax and take-home pay...')
        tax_total = calc_tax(total_earnt)
        after_tax = total_earnt - tax_total
        print(f'\nYou will be taxed roughly £{tax_total} between now and your saving deadline.')

    print(f'You will take home roughly £{after_tax}.')

    # calculate monthly expenses
    total_daily_expenses = get_expenses('daily')
    total_weekly_expenses = get_expenses('weekly')
    total_monthly_expenses = get_expenses('monthly') + total_daily_expenses + total_weekly_expenses

    print(f'\nYour total monthly expenses are £{total_monthly_expenses}, before accounting for any random spending.')
    print(f'\nYour new take home total from now until {deadline_date.strftime(DATE_FORMAT)} is roughly £{after_tax - ((total_monthly_expenses // 4) * weeks_to_deadline)}.')


# function to return user input within a given table of correct inputs; will always return a value within the correct table
def get_input(prompt, correct, numbered=False):
    while True:
        choice = str(input(f'\n{prompt}     ')).lower()
        # check if input is in the correct table, regardless of whether the input can be a number
        if choice in correct: return choice
        # check for number user inputs that can be integer <= table length
        if numbered and choice.isnumeric() and int(choice) <= len(correct) and int(choice) > 0: return correct[int(choice)-1]

        print(NOT_VALID)


# function to return only int user input, within an optional range
def get_int_input(prompt, inclusive=True, mini=0, maxi=1000000):
    while True:
        choice = str(input(f'\n{prompt}     ')).lower()

        if choice.isnumeric():
            # check for inclusive values (choice can be equal to bounds)
            if inclusive and mini <= int(choice) and int(choice) <= maxi: return int(choice)
            # check for exclusive values (choice cannot be equal to bounds)
            elif mini < int(choice) and int(choice) < maxi: return int(choice)
            
        print(NOT_VALID)


# function to return a validated user inputted date
def get_date_input(prompt):
    while True:
        choice = str(input(f'\n{prompt}     ')).lower()

        try:
            return dt.strptime(choice, DATE_FORMAT)
        except:
            print(NOT_VALID)

    
# function to calculate basic tax amount; returns the amount that will be deducted
def calc_tax(gross_pay):
    brackets = [12570, 50270, 125140]
    rates = [.20, .40, .45]

    tax_total = 0
    to_tax = 0

    for bracket in reversed(brackets):
        if gross_pay > bracket:
            to_tax = gross_pay - bracket
            gross_pay -= to_tax
        
        tax_total += to_tax * rates[brackets.index(bracket)]
        to_tax = 0

    return tax_total


# function to total, if any, all daily expenses
def get_expenses(frequency):
    total = 0
    multiplier = {'daily': days_in_month, 'weekly': 4, 'monthly': 1}

    while True:
        required = str(input(f'\nDo you have any {frequency} expenses? (y/n):   ')).lower()

        if required in NO: return 0
        
        elif required in YES:
            while True:
                expense_name = str(input(f'\nEnter name of a {frequency} expense (q to quit):  ')).lower()

                if expense_name in QUIT: return total * multiplier[frequency]

                expense_cost = get_int_input(f'\nEnter price of {frequency} expense \'{expense_name}\':   ')

                total += expense_cost

        else:
            print(NOT_VALID)


# main script
main()