import random
from datetime import datetime, timedelta
from decimal import Decimal
from models.category import Category
from models.user import User
from utilities import db


# Helper functions to generate random values
def random_name():
    names = ["Salary", "Freelance Project", "Investment", "Gift", "Bonus", "Dividends", 
             "Side Hustle", "Consultation", "Refund", "Lottery", "Sale", "Rental Income"]
    return random.choice(names)

def random_date():
    start_date = datetime(2022, 1, 1)
    end_date = datetime(2024, 12, 31)
    delta = end_date - start_date
    random_days = random.randint(0, delta.days)
    return (start_date + timedelta(days=random_days)).strftime("%Y-%m-%d")

def random_amount():
    return f"{random.uniform(50, 10000):.2f}"

def random_description():
    descriptions = [
        "Payment for services rendered", "Monthly salary", "Annual bonus", "Investment returns",
        "Gift from a friend", "Refund for returned item", "Income from side business",
        "Consultation fee", "Rental income", "Freelance project payment"
    ]
    return random.choice(descriptions)

# Generating a list of 50 dictionaries with random values
earnings_data = [
    {
        "name": random_name(),
        "date_occurred": random_date(),
        "amount": random_amount(),
        "description": random_description()
    }
    for _ in range(50)
]

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
    for expense_name in expense_types:
        new_category = Category(name=expense_name, user_id=user_id)
        new_category.save()


def expense_data(user_id) -> list:
    """ Returns a list of auto generated data for a user """
    categories = [c.id for c in db.query(Category).filter_by(user_id=user_id).all()]

    return [
        {
            "category_id": random.choice(categories),
            "amount": 
        }
    ]
