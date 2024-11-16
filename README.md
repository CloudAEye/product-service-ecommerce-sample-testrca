# Demo E-commerce App - Product Microservice

This project demonstrates a simple e-commerce system built using a microservices architecture. It consists of one of the service used by this demo app:
**Product Service**: Manages product information, including creation, updates, and retrieval of product details.

## Technology Stack

- Backend: Flask (Python)
- Database: MySQL
- Authentication: JWT

## Getting Started

These instructions will get you a copy of the project up and running on your local machine for development and testing purposes.

### Prerequisites

- Python 3.12+
- Docker and Docker Compose (optional, for containerized deployment)

### Installation

1. **Set up virtual environment (optional)**

```bash
python -m venv venv
source venv/bin/activate  # On Windows use `venv\Scripts\activate`
```

2. **Install dependencies**

Navigate to each service directory and install the required Python packages.

```bash
pip install -r requirements.txt
```

### Running the Services

#### Without Docker

Run the below command from the root path of the dir

```bash
export FLASK_APP='src/app.py'
export DATABASE_URL="mysql+pymysql://productname:password@hostname:3306/defaultdb"
flask run --port=5000
```

> The application should be up and running on http://127.0.0.1:5000


#### With Docker

Run the below command from root path of the dir

```bash
export DATABASE_URL="mysql+pymysql://username:password@hostname:3306/defaultdb"
docker build -t ecomm-product-service .
docker run -e DATABASE_URL=$DATABASE_URL -p 5000:5000 ecomm-product-service
```

> The application should be up and running on http://127.0.0.1:5000

## API Endpoints

- **Create a Product** (Authenticated)
  - POST `/products`
  - Headers: `Authorization: Bearer <JWT_Token>`
  - Payload: `{"name": "New Product", "description": "Product Description", "price": 99.99, "quantity": 100}`

- **Get All Products** (Authenticated)
  - GET `/products`

- **Get a Single Product** (Authenticated)
  - GET `/products/<product_id>`

- **Update a Product** (Authenticated)
  - PUT `/products/<product_id>`
  - Headers: `Authorization: Bearer <JWT_Token>`
  - Payload: `{"name": "Updated Product", "description": "Updated Description", "price": 89.99, "quantity": 150}`

- **Delete a Product** (Authenticated)
  - DELETE `/products/<product_id>`
  - Headers: `Authorization: Bearer <JWT_Token>`

### Example Requests

1. **Create a Product** (as an authenticated user)

POST `http://localhost:5002/products`

Headers:

```
Authorization: Bearer <JWT_Token>
```

Payload:

```json
{
    "name": "New Product",
    "description": "Product Description",
    "price": 99.99,
    "quantity": 100
}
```

## Testing

To run unit tests for each service:

```bash
export FLASK_APP='src/app.py'
export DATABASE_URL="mysql+pymysql://username:password@hostname:3306/testdb"
export TEST='TRUE'
export USER_SERVICE_URL='http://localhost:5100' # Replace with the actual url
python -m unittest discover tests
```
