# Library Management System API

This is a Django REST Framework-based API for managing a library system, which supports book borrowing, return, user registration/login with JWT authentication, penalty tracking, and more.

---

## Documentation

###  Postman Collection
[Download Postman Collection](./library_system_api.postman_collection.json)

###  ER Diagram
[Click here to view the ER Diagram (PDF)](./ER_diagram.pdf)

---

##  Features

- User registration and JWT login system
- Book, author, and category management (CRUD)
- Borrow and return books with rules and penalties
- Track user borrowing history and penalties
- Admin permissions for modifying data

---

---

## How borrowing/return logic works

After getting a borrowing request form a valide user. 
I first check
1. Did he borrow less than 3 books?
2. Is book copie is available?

If the condition true then I give him to borrow a book.

```bash
if active_borrows>=3:
            raise serializers.ValidationError("Your Already Borrow 3 Books. 
            Which is Max Limit Of Borrowing.")

        book= data["book"]
        if book.available_copies<1:
            raise serializers.ValidationError("No Copies Available. Sorry!")

        return data
```
---

 ## How penalty points are calculated

When a user want to borrow a book. I automatically set a due_date
```bash
borrow_date+timedelta(days= 14)
```
Then I check the borrow date expiration. And give penalty usng days_late.

```bash
if date.today() > borrow.due_date:
            days_late = (date.today() - borrow.due_date).days
            request.user.penalty_points += days_late
            request.user.save()
```



##  Setup Instructions

### Clone the repository

```bash
git clone https://github.com/AzizurRahamanGithub/Library-Management-System.git
cd Library-Management-System
```

### Clone the repository

```bash
python -m venv env
source env/bin/activate   # This is for Linux
```

### Create and activate virtual environment
```bash
python -m venv env
source env/bin/activate   # This is for Linux
```

### Install dependencies
```bash
pip install -r requirements.txt
```
###  Run migrations

```bash
python manage.py makemigrations
python manage.py migrate
```
### Create a superuser (for admin access)

```bash
python manage.py createsuperuser
```
### Run the development server

```bash
python manage.py runserver
```

---
     
