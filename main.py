# program to calculate different stats for finances


from datetime import datetime as dt, timedelta
from dateutil.relativedelta import relativedelta
import constants, inputs, finance


# main
def main():
    print('Welcome to finance calculator.')

    today = dt.now()
    
    is_pre_tax = inputs.string('Will you be inputting pay pre-tax or post-tax? (pre/post)', constants.PRE + constants.POST)

    already_earnt = inputs.number(f'How much have you earnt this tax year so far, since April {today.year}?')

    # calculate all data needed for annual wage
    freq = inputs.string('How often do you get paid?\n1. Weekly\n2. Bi-weekly\n3. Monthly\nChoice:', constants.PAY_FREQUENCY, True)
    avg_wage = inputs.number(f'What is the average pay per {freq} paycheck?')
    
    weeks_to_next_paycheck = constants.WEEKS_BETWEEN[constants.PAY_FREQUENCY.index(freq)]

    # calculate closest paycheck dates
    last_paycheck_date = inputs.date('When was your last paycheck (dd/mm/yy)?')
    next_paycheck_date = timedelta(weeks=weeks_to_next_paycheck) + last_paycheck_date

    # calculate saving deadline
    deadline_date = inputs.date('When are you trying to save money by? (dd/mm/yy)')
    weeks_to_deadline = (deadline_date - dt.now()).days // 7
    # calculate wage between next paycheck and saving deadline
    wage = (weeks_to_deadline / constants.WEEKS_BETWEEN[constants.PAY_FREQUENCY.index(freq)]) * avg_wage
    # calculate the total for this fiscal year
    total_earnt = wage + already_earnt
    
    print(f'\nYour next paycheck will be on {next_paycheck_date.strftime(constants.DATE_FORMAT)}.')
    print(f'\nOn average, you will earn {wage} in {weeks_to_deadline} weeks from now until your saving deadline, for a total of £{total_earnt}.')

    # calculate amount of tax to be paid
    if is_pre_tax in constants.POST:         # they have input income after tax, so do not need to calculate any tax
        after_tax = total_earnt
    else:
        print('\nCalculating your tax and take-home pay...')
        tax_total = finance.calc_tax(total_earnt)
        after_tax = total_earnt - tax_total
        print(f'\nYou will be taxed roughly £{tax_total} between now and your saving deadline.')

    print(f'You will take home roughly £{after_tax}.')

    # calculate monthly expenses
    total_daily_expenses = finance.get_expenses('daily')
    total_weekly_expenses = finance.get_expenses('weekly')
    total_monthly_expenses = finance.get_expenses('monthly') + total_daily_expenses + total_weekly_expenses

    print(f'\nYour total monthly expenses are £{total_monthly_expenses}, before accounting for any random spending.')
    print(f'\nYour new take home total from now until {deadline_date.strftime(constants.DATE_FORMAT)} is roughly £{after_tax - ((total_monthly_expenses // 4) * weeks_to_deadline)}.')


# main script
main()