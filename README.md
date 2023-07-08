#  CashFlow
Expence Tracker for CS50 final project.

## Table of Contents

- [Introduction](#Introduction)
- [Features](#Features)
- [Technologies](#Technologies)
- [Usage](#Usage)

## Introduction

This project is designed to provide a user registration and login system using Python and MySQL. It allows users to register, login, and access a dashboard where they can manage their income and expenses.

When a user registers by filling out the required information, such as username and password, their data is saved in a MySQL database. During the login process, the Python script will validate the entered username and password by checking if they exist and match the records stored in the database. Upon successful authentication, the user is redirected to the dashboard.

The dashboard presents the user with options to record their income and expenses. When the user clicks the income button, the income amount will be stored in the database. Similarly, expenses are also recorded in the database.



## Features
* User registration
* User login
* Secure password storage
* Dashboard with income and expense options
* Database integration for data storage

## Technologies

The project utilizes the following technologies:

- Python: The programming language used for the backend logic and database integration.
- Flask: The Python web framework 
- MySQL: The database management system used to store user information, income, and expenses.
- HTML & CSS: For the frontend and styles

## Usage
- first, you can log in using the login button.
- when you click the login button you will see an interface like below

![login](https://github.com/nadunwee/CashFlow/blob/main/screenshots/login_page.jpg)

- you can log in by giving login info 
- if you haven't registered you can register using the register button.

![homepage](https://github.com/nadunwee/CashFlow/blob/main/screenshots/register_page.jpg)

- Then you will see your dashboard

![dashboard](https://github.com/nadunwee/CashFlow/blob/main/screenshots/dashboard_page.png)

- you can click income tab to add an income

![income](https://github.com/nadunwee/CashFlow/blob/main/screenshots/income_page.jpg)

-  and you can click expense button to add an expense

![expense](https://github.com/nadunwee/CashFlow/blob/main/screenshots/expence_page.jpg)
