# PayEase
[![Demo Video](https://img.shields.io/badge/Watch-Demo-blue?style=for-the-badge)](https://drive.google.com/file/d/1rmjsOZTqseRoh0Ngc4z-4ocRmjWCB7dj/view?usp=drive_link)
## Description
PayEase is a dummy money transaction web application similar to PhonePe. Users can transfer money using various methods such as account number, phone number, or UPI ID. The project generates transaction histories for both sender and receiver accounts and supports multiple account management. Users can also perform mobile recharges and check their balance securely. Additionally, PayEase functions as a payment gateway that can be integrated into other projects to facilitate transactions via API.

## Features
- Send money using account number, phone number, or UPI ID.
- Transaction history for both sender and receiver.
- Mobile recharge functionality with automatic balance deduction.
- Users can add multiple accounts with a secure 6-digit password.
- Check balance of each account using the password.
- Filter transaction history by minimum amount, maximum amount, date, debit, and credit.
- Payment Gateway feature: Integrate API for seamless transactions in external projects.
- Secure authentication using Django's built-in authentication system.
- Proper error handling and validation using Django Forms.

## Technologies Used
- **Backend:** Django (Python)
- **Frontend:** HTML, CSS, Bootstrap, JavaScript
- **Database:** SQLite
- **API:** Django Rest Framework API for Payment Gateway feature
- **Environment:** Virtual Environment (venv)

## Installation
1. Clone the repository:
   ```sh
   git clone <repository-url>
   ```
2. Navigate to the project directory:
   ```sh
   cd PayEase
   ```
3. Create and activate a virtual environment:
   ```sh
   python -m venv venv
   source venv/bin/activate  # On macOS/Linux
   venv\Scripts\activate  # On Windows
   ```
4. Install dependencies:
   ```sh
   pip install -r requirements.txt
   ```
5. Run database migrations:
   ```sh
   python manage.py migrate
   ```
6. Start the Django development server:
   ```sh
   python manage.py runserver
   ```
7. Access the application at `http://127.0.0.1:8000/`.

## Usage
- Register/Login to the PayEase platform.
- Add multiple accounts by providing account details and setting a password.
- Perform money transactions and view transaction history.
- Use the payment gateway feature by integrating the provided API into another project.
- Securely check balances and apply filters to analyze transactions.

## Configuration
- Ensure the virtual environment is activated before running the project.
- Configure API settings for payment gateway integration.
- Modify Django settings if deploying to production.

