# Bank Management System — Project Statement

## 1. Problem Statement

Managing customer banking records manually can be time-consuming and can lead to problems such as duplicate records, difficulty in finding customer information, and errors while updating or deleting records.

The **Bank Management System** is developed to provide a simple command-line solution for managing customer records. It allows authorized users to add, search, display, update, and delete customer information while storing the records in a database.

The project is intended to demonstrate how Python can be used with database systems to perform basic record-management operations in an organized way.

---

## 2. Scope of the Project

The scope of this project is limited to the basic management of customer records through a command-line interface.

The system covers:

- Creating and storing customer records.
- Searching for a customer using a unique customer ID.
- Displaying all stored customer records.
- Updating existing customer information.
- Deleting customer records.
- Preventing duplicate customer IDs.
- Validating basic user input.
- Providing login-based access to the system.
- Storing records using either **MySQL** or **SQLite**.
- Automatically creating the required customer table when the application starts.
- Supporting command-line options for selecting the database and SQLite database file.

The project is designed as an educational database-management application. It does not attempt to provide complete real-world banking services such as online transactions, fund transfers, ATM operations, loan management, or internet banking.

---

## 3. Target Users

The system is intended for users who need a simple application for maintaining customer records.

### Primary Users

- **Bank staff or employees** who need to add, search, view, update, or delete customer records.
- **Managers** who need access to customer information for basic record management.

### Educational Users

- **Students** learning Python programming.
- **Students** learning database connectivity and CRUD operations.
- **Teachers or evaluators** who want to demonstrate or evaluate a basic Python database project.

The project is primarily designed for a controlled/local environment rather than for direct use as a production banking system.

---

## 4. High-Level Features

### 4.1 User Login

The application provides a simple username and password login system. It allows a maximum of three incorrect login attempts before closing the program.

### 4.2 Add Customer Records

Users can add a new customer record containing:

- Customer/account number
- Customer name
- Year of birth
- Branch IFSC code
- Last four digits of the mobile phone number

The system checks whether the customer ID already exists before saving a new record.

### 4.3 Search Customer Records

Users can search for an individual customer by entering the customer ID. If the record exists, the customer's stored information is displayed.

### 4.4 Display Customer Records

The system can display all customer records stored in the database, arranged by customer ID.

### 4.5 Update Customer Records

Existing records can be updated. The user can change:

- Name
- Year of birth
- IFSC code
- Phone number

### 4.6 Delete Customer Records

Users can delete an existing customer record by entering its customer ID. The system first checks whether the record exists.

### 4.7 Input Validation

The program performs basic validation, including:

- Numeric validation for fields that require numbers.
- Prevention of empty text values.
- Checking for duplicate customer IDs.
- Handling invalid menu choices.

### 4.8 Database Support

The application supports two database options:

- **MySQL** for database-server-based storage.
- **SQLite** for local file-based storage.

The application can automatically use SQLite when MySQL is unavailable in automatic database mode.

### 4.9 Command-Line Configuration

The program supports command-line options for selecting the database type, SQLite database file, and environment configuration file.

---

## 5. Project Objective

The main objective of the project is to develop a simple and functional bank customer-record management system using Python and database connectivity.

The project demonstrates practical implementation of:

- Python programming
- Functions and control structures
- User input and validation
- CRUD operations
- SQL queries
- Database connectivity
- MySQL and SQLite integration
- Command-line arguments
- Basic authentication
- Error handling
