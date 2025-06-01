## **Expense Tracker**

This project is a simple and user-friendly application designed to help users track their expenses efficiently.  It allows you to categorize your spending, get transaction statements and spending reports, and analyze your financial habits to make informed decisions.

## Getting Started

* Set up config as in `.env.example` named `.env`
* Install dependencies 
```python
pip install -r requirements.txt
```
* Start the application
```cmd
python3 -m api.v1.app
```

## API Endpoints

| Files | Endpoints | Basic Operations | Payload |
| ----- | ----- | ------ | ----- |
| `admin.py` | `/tags` | `POST` - Creates a new Tag. Only an admin can do this. | ``` {'name'} ```
| | `/tags/<tag_id>` | `GET` - Retrieves one Tag or all Tags created by the admin if no tag_id was passed |
| | | `PUT` - Updates a Tag object |
| | | `DELETE` - Deletes a Tag object |
| `auth.py` |  `/signup` | `POST` - Creates a new User | ```{'first_name', 'last_name', 'email', 'password','confirm_password'} ``` |
| | `/login` | `POST` - Creates a new session for the user and returns a JSON payload |
| | `/logout` | `GET` - Logs a user out from the session |
| | `/reset-password` | `POST` - Creates a password reset request which sends OTP to the registered email | ```{'email'}``` |
| | | `PATCH` - Updates the user password after OTP has been verified. | |
| | `/resend_otp` | Resends otp based on the value of the `process` parameter.
| | `/auth/verify/<process>/<otp>` | Verifies the OTP
| `categories.py` | `/categories` | `POST` - Creates a new Category of Expenses | ``` {'name'} ``` |
| | `/categories/<category_id>` | `GET` - Retrieves all Category objects created by the user or one Category if the `category_id` was passed. |
| | | `PUT` - Updates a Category object with data |
| | | `DELETE` - Deletes a Category object |
| `earnings.py` | `/earnings` | `POST` - Creates a new Earning object | ``` {'name', 'date_occurred', 'amount'} ``` |
| | `/earnings/<earning_id>` | `GET` - Retrieves all Earning objects created by the user or one object if the `earning_id` was passed. |
| | | `PUT` - Updates an Earning object with data |
| | | `DELETE` - Deletes an Earning object |



## 4. Contributing Guidelines

We welcome contributions from the community! Here are some ways you can get involved:

* **Report issues:**  If you encounter any bugs or have feature requests, please create an issue on the GitHub repository.
* **Submit pull requests:**  If you have code improvements or new features, create a pull request with clear descriptions and tests.
* **Document your code:**  Ensure that any code you write is properly documented for others to understand.
* **Follow the code style:**  Adhere to the existing code style guidelines to maintain consistency.

## 5. License Information

This project is licensed under the [License Name] license. See the `LICENSE` file for more details.

