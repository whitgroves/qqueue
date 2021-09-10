## Getting Started

Navigate to the backend API directory to create your virtual environment and start it:

    $ cd api
    $ py -m venv venv
    $ source venv/Scripts/activate

Install the project dependencies inside your `venv`:

    $ pip install -r requirements.txt
    
Then setup the database:

    $ flask db init
    $ flask db migrate
    $ flask db upgrade
    
(More detail about `flask-migrate` can be found [here](https://github.com/miguelgrinberg/flask-migrate).)

Navigate back to your home folder:

    $ cd ..
    
Then run:

    $ yarn start-api
    
To start the API server on [localhost:5000](http://localhost:5000/).
    
In a new terminal, run:

    $ yarn start
    
This will start the React app on [localhost:3000](http://localhost:3000/).
    

