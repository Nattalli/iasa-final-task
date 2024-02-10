# IASA final task

## Installing using Github

### Backend

Python 3.9+ is a must

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
