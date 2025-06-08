from api.v1.routes.auth import hash_password
import random
from datetime import datetime, timedelta
from decimal import Decimal
from models.category import Category
from models.recurring_expense import RecurringExpense
from models.expense import Expense
from models.earning import Earning
from models.user import User
from utilities import db
import os
import requests
from dotenv import load_dotenv, find_dotenv
from sqlalchemy.exc import IntegrityError

load_dotenv(find_dotenv())


# Helper functions to generate random values
def random_name():
    names = ["Salary", "Freelance Project", "Investment", "Gift", "Bonus", "Dividends", 
             "Side Hustle", "Consultation", "Refund", "Lottery", "Sale", "Rental Income"]
    return random.choice(names)

def random_date():
    start_date = datetime(2010, 1, 1)
    end_date = datetime(2024, 12, 31)
    delta = end_date - start_date
    random_days = random.randint(0, delta.days)
    random_hours = random.randint(0, 12)
    random_secs = random.randint(0, 60)
    return (start_date + timedelta(days=random_days,
                                   hours=random_hours,
                                   minutes=random.randint(0, 60),
                                   seconds=random_secs))

def random_amount():
    return f"{random.uniform(50, 100000):.2f}"

def random_description():
    descriptions = [
        "Payment for services rendered", "Monthly salary", "Annual bonus", "Investment returns",
        "Gift from a friend", "Refund for returned item", "Income from side business",
        "Consultation fee", "Rental income", "Freelance project payment"
    ]
    return random.choice(descriptions)


def create_earnings(user_id):
    """Generating a list of 50 dictionaries with random values"""
    earnings = [
        {
            "name": random_name(),
            "date_occurred": random_date(),
            "amount": random_amount(),
            "description": random_description(),
            "user_id": user_id
        }
        for _ in range(150)
    ]
    for e in earnings:
        new_income = Earning(**e)
        new_income.save()
        print('New Income - {} received \nDate - {}'.format(new_income.id, new_income.date_occurred))

    print()


def create_random_categories(user_id):
    """ Creates 20 expense categories for a user """
    expense_types = [
        "Rent",
        "Utilities",
        "Groceries",
        "Transportation",
        "Insurance",
        "Healthcare",
        "Internet",
        "Subscriptions",
        "Entertainment",
        "Dining Out",
        "Loan Payments",
        "Credit Card Payments",
        "Gym Membership",
        "Clothing",
        "Education",
        "Pet Supplies",
        "Phone Bill",
        "Home Maintenance",
        "Personal Care",
        "Gifts & Donations"
    ]
    for name in expense_types:
        new_category = Category(name=name, user_id=user_id)
        new_category.save()


def create_expenses(user_id):
    """ Returns a list of auto generated data for a user """
    categories = [c.id for c in db.query(Category).filter_by(user_id=user_id).all()]

    expenses = [
        {
            "category_id": random.choice(categories),
            "amount": random_amount(),
            "description": random_description(),
            "date_occurred": random_date(),
            "user_id": user_id
        }
        for _ in range(40)
    ]
    for e in expenses:
        new_expense = Expense(**e)
        new_expense.save()
        print('New Expense - {} created'.format(new_expense.id))

    print()
    

def create_recurring_expenses(user_id):
    """ Generates random recurring expense data """
    categories = [c.id for c in db.query(Category).filter_by(user_id=user_id).all()]

    rec_expenses = [
        {
            "category_id": random.choice(categories),
            "amount": random_amount(),
            "description": random_description(),
            "start_date": random_date(),
            "end_date": random_date(),
            "frequency": random.choice(['daily', 'weekly', 'monthly']),
            "user_id": user_id
        }
        for _ in range(30)
    ]
    for e in rec_expenses:
        new_rec_expense = RecurringExpense(**e)
        new_rec_expense.save()
        print(f'Recurring Expense with id - {new_rec_expense.id} created')

    print()


if __name__ == "__main__":
    api_key = os.getenv('API_NINJA_KEY')
    header = {"X-API-Key": api_key}
    for _ in range(20):
        URL = "https://api.api-ninjas.com/v1/randomuser"
        r = requests.get(URL, headers=header)
        if r.status_code == requests.codes.ok:
            data = r.json()
            first_name, last_name = data['name'].split(' ')
            email = data['email']
            password = hash_password(email)
            address = data['address']
            try:
                user = User(
                    first_name=first_name,
                    last_name=last_name,
                    email=email,
                    password=password,
                    address=address)
                user.save()
            except IntegrityError:
                print(f'User with email {email} already exists')
                continue
            print(f'User {user.first_name} {user.last_name} created with id - {user.id}')
            create_random_categories(user.id)
            create_earnings(user.id)
            create_expenses(user.id)
            create_recurring_expenses(user.id)
