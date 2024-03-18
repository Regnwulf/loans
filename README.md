# Loans and Payments API

This is a RESTful API built with Django and Django REST Framework to manage loans and payments from clients.

## Features

- CRUD (Create, Read, Update, Delete) for loans and payments.
- Token-based authentication to ensure secure access to resources.
- Outstanding balance automatically calculated considering interest rate and payments made.
- Access restriction: Users can only view and edit their own loans and payments.

## Endpoints

### Loans

- `GET /api/loans/`: Lists all loans of the authenticated user.
- `POST /api/loans/`: Creates a new loan for the authenticated user.
- `GET /api/loans/{id}/`: Retrieves details of a specific loan.
- `PUT /api/loans/{id}/`: Updates a specific loan.
- `DELETE /api/loans/{id}/`: Deletes a specific loan.

### Payments

- `GET /api/payments/`: Lists all payments associated with loans of the authenticated user.
- `POST /api/payments/`: Creates a new payment for a loan of the authenticated user.
- `GET /api/payments/{id}/`: Retrieves details of a specific payment.
- `PUT /api/payments/{id}/`: Updates a specific payment.
- `DELETE /api/payments/{id}/`: Deletes a specific payment.

### Authentication

- `POST /api/token/`: Obtains an authentication token for the user.

## Installation and Setup

1. Clone the repository to your local environment.
2. Create a venv `python3 -m venv venv`
3. Activate the venv `source venv/bin/activate`
4. Install project dependencies using `pip install -r requirements.txt`.
5. Run database migrations with `python manage.py migrate`.
6. Start the development server with `python manage.py runserver`.

Make sure to properly configure your environment variables for database configuration and other sensitive settings.

## Contributing

Feel free to contribute with improvements, bug fixes, or new features. Just follow these steps:

1. Fork the project.
2. Create a branch for your feature (`git checkout -b feature/new-feature`).
3. Commit your changes (`git commit -am 'Add new feature'`).
4. Push to the branch (`git push origin feature/new-feature`).
5. Create a new Pull Request.