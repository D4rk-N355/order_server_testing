@Menu System API

A Flask + SQLAlchemy based restaurant order management API.

Supports creating, retrieving, updating, and canceling orders.

Designed to follow a consistent JSON response format for easy integration with front-end applications or third-party systems.



@Features

\- Create Order POST /api/order

\- Get Order GET /api/order/<order\_id>

\- Update Order Status PUT /api/order/<order\_id>/status

\- Cancel Order DELETE /api/order/<order\_id>



@Project Structure

|app/

|--routes/

|----order\_routes.py   # API routes

|--services/

|----order\_service.py  # Database logic

|run.py                # Entry point

|requirements.txt      # Dependencies



@ Installation \& Run



1\. Create virtual environment

python -m venv venv

source venv/bin/activate   # macOS/Linux

venv\\Scripts\\activate      # Windows



2\. Install dependencies

pip install -r requirements.txt



3\. Start server

python run.py



@Environment Variables

Use a local .env file (do not upload to GitHub). Example:

DATABASE\_URL=postgresql://user:password@localhost:5432/menu\_db

SECRET\_KEY=supersecret





On Zeabur or other cloud platforms, configure these values in the Environment Variables section.



@API Example

Create Order

POST /api/order

Content-Type: application/json



{

  "restaurant\_id": 1,

  "table\_id": "T05",

  "items": \[

    {"dish\_id": 1, "name": "Spaghetti", "quantity": 1, "price": 220}

  ],

  "note": "No spicy",

  "payment\_method": "credit\_card"

}





Response JSON

{

  "order\_id": 9,

  "restaurant\_id": 1,

  "table\_id": "T05",

  "note": "No spicy",

  "status": "pending",

  "created\_at": "2025-11-30T23:43:05",

  "updated\_at": "2025-11-30T23:43:05",

  "total\_amount": 220.0,

  "payment": {

    "method": "credit\_card",

    "status": "unpaid"

  },

  "items": \[

    {

      "dish\_id": 1,

      "name": "Spaghetti",

      "quantity": 1,

      "price": 220.0

    }

  ]

}







@ Docker Deployment

Dockerfile Example

FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY . .

ENV FLASK\_APP=run.py

ENV FLASK\_RUN\_HOST=0.0.0.0

ENV FLASK\_RUN\_PORT=2323

CMD \["flask", "run"]





Local Test

docker build -t menu-api .

docker run -p 2323:2323 menu-api







@Status Codes

\- 201 Created → Order created successfully

\- 200 OK → Order retrieved / updated / canceled successfully

\- 400 Bad Request → Invalid input

\- 404 Not Found → Order not found



@ Notes

\- .env is for local development only. Use environment variables in cloud deployment.

\- Keep an .env.example file to list required variables for team members.



