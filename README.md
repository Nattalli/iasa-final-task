# IASA final task

## Running via Docker (it takes a time!)

1. Install / open Docker
2. Run `docker-compose up --build` at the terminal

## Running locally

### Backend

#### Installing using Github

Python 3.10+ is a must

1. Clone the repository in the terminal:
`git clone https://github.com/Nattalli/iasa-final-task.gitt`
2. Make the following command and populate it with required data:
`cp .env.example .env`
3. Create virtual env:
`python -m venv venv`
4. Setup virtual env:
    * On Windows: `venv\Scripts\activate`
    * On Linux or MacOS: `source venv/bin/activate`
5. Go to the `backend` folder: 
`cd backend`
6. And mark it as the source root 
7. Install requirements: `pip install -r requirements.txt`
8. Make migrations: `python manage.py migrate`
9. Now you can run it: `python manage.py runserver`

### Frontend

1. Go to the `frontend` folder:
   `cd frontend`
2. Install requirements: `npm i`
3. Run the frontend part: `npm run dev`
