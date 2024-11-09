import random
from datetime import datetime, timedelta
from decimal import Decimal
from models.user import User


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

def create_random_categories(user: User):
    """ Creates 20 expense categories for a user """
    
