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

| Files | Endpoints | Basic Operations |
| ----- | ----- | ------ |




**Basic operations:**

* **Add expense:**  Enter the expense details through prompts in the console.
* **View expenses:**  Use the "view" command followed by optional filters (e.g., "view date", "view category").
* **Generate report:**  Enter the "report" command and specify the time period (e.g., "report monthly", "report weekly").
* **Set budget:**  Use the "budget" command followed by the category and limit.
* **Export data:**  Use the "export" command and select the desired format.

**Refer to the help menu:**

* Enter the "help" command for a detailed list of available commands and options.

## 4. Contributing Guidelines

We welcome contributions from the community! Here are some ways you can get involved:

* **Report issues:**  If you encounter any bugs or have feature requests, please create an issue on the GitHub repository.
* **Submit pull requests:**  If you have code improvements or new features, create a pull request with clear descriptions and tests.
* **Document your code:**  Ensure that any code you write is properly documented for others to understand.
* **Follow the code style:**  Adhere to the existing code style guidelines to maintain consistency.

## 5. License Information

This project is licensed under the [License Name] license. See the `LICENSE` file for more details.

