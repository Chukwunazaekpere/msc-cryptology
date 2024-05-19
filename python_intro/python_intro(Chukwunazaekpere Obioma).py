"""
Author: Chukwunazaekpere Emmanuel Obioma
Nationality: Biafran
Course: Pre-course Programming

instructions: for the function 'cost_calculator_from_file', ensure to have created a file called
'expenses.txt' with content in the format as below;
********************
library = 100
transport = 500
feeding = 300
electricity = 200
gas = 100
water = 150
*********************
"""
def check_number_validity(number):
    int_number = int(number)
    if type(int_number) != int:
        return False
    return True

def cost_calculator():
    name = input("\n\t Please enter your name & press enter: " )
    print(f"\n\t Welcome {name}. This is an expenses calculator")
    number_of_categories = input("\n\t Please enter the number of items & press enter: ")
    is_valid_number = check_number_validity(number_of_categories)
    if is_valid_number:
        count = 0
        total_expenses = 0
        while count < int(number_of_categories):
            item_cost = input(f"\n\t Please enter the cost for item {count+1} & press enter: ", )
            is_valid_number = check_number_validity(item_cost)
            if not is_valid_number:
                print(f"\n\t {item_cost} is not a valid number. Please try again")
                continue
            total_expenses+=int(item_cost)
            print(f"\n\t Total expenses after {count+1} items is: ${total_expenses}")
            count+=1
        return print(f"\n\t Thank you {name}. The total cost for your {number_of_categories} items is: {total_expenses}")
    print(f"\n\t {number_of_categories} is not a valid number. Please try again")

cost_calculator()


expenses_file = "expenses.txt"
def cost_calculator_from_file():
    total_expenses = 0
    with open(file=expenses_file, mode="r")as expenses_content:
        expenses = expenses_content.readlines()
    for expense in expenses:
        if "=" in expense:
            line = expense.split("=")
            expense_value = line[1]
            # expense_name = line[0]
            is_valid_number = check_number_validity(expense_value)
            if is_valid_number:
                total_expenses+=int(expense_value)
        # print(expense)
    with open(file=expenses_file, mode="+a")as expenses_content:
        expenses_content.write(f"\n\t Total expenses: {total_expenses}")


# cost_calculator_from_file()
