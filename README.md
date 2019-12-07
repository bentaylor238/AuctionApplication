## An explanation of the organization and name scheme for the workspace
  ### /docs/
    This will contain all documentation information 
  ### /auction/
    All project level code for django project
  ### /auction_app/
    All app level code for django project
## Version-control procedures
  We will be using Git. 
  Each user story will be it's own small branch.
  Each pull request will be reviewed by at least 1 other team member.
## Tool stack description and setup procedure
  We will be using django version 2.2 for the backend.
  We will be using python version 3.7 as part of the django backend.
  The database will be in SQL, which is default in django.
  We will be using HTML5 and Javascript to design the frontend.
## Build instructions
  Project installs
    python
    pipenv
    git

  clone repo 
    git clone git@github.com:usu-cs-3450/Repo-1.01.git
  install dependencies
    cd Repo-1.01
    pipenv install
  start environment
    pipenv shell
  run development server
    python manage.py runserver [port number]
  
## Unit and system testing instructions
  Using django's built in test framework.  All tests are written in test.py
  python manage.py test
