# Official Backend of SWARA

You can view the full website at https://swara-web.vercel.app.

## HOWEVER
You might find the latency of the website in production to be bad, so I suggest you to follow these steps to run at your local machine and feel the full experience of the Swara website.

### 1. Pull Backend and Frontend
As you can see this is the backend repository, as for the frontend repository you can view the front-end source code at https://github.com/lontonggg/swara-fe.

### 2. Setup python virtuan env
Run `python3 -m venv venv` to create your virtual env
and then activate that virtual env and run `pip install -r requirements.txt`.

### 3. .env for SECRET_KEY and Database
Create a .env file in the main application directory (swara_be) and fill in everythin as needed. If you want to request the credentials you can contact me through email at `dhafin.kamal@gmail.com`. Also remember to setup your database using POSTGRESQL, because psycopg3 is already part of the website.

### 4. Run
Turn on your repository, run your frontend with `npm run dev`, and your backend locally with `python manage.py runserver`. Have fun!
