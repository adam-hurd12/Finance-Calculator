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