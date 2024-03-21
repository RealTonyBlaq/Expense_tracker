-- Script sets up SQL for the Expense Tracker project
CREATE DATABASE IF NOT EXISTS expense_tracker;
CREATE USER IF NOT EXISTS 'et_dev'@'localhost' IDENTIFIED WITH mysql_native_password BY 'et_dev_login';
GRANT ALL PRIVILEGES ON expense_tracker.* TO 'et_dev'@'localhost';
GRANT SELECT ON performance_schema.* TO 'et_dev'@'localhost';
FLUSH PRIVILEGES;
