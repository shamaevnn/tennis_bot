# Contributing

## First start
1. Create virtual environment and install dependencies
```{shell}
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```
2. Install `pre-commit` hooks to automatically format code
```{shell}
pre-commit install-hooks
pre-commit install
```
3. Create `.env` file.
```{shell}
cp .env_example .env
```
4. Create two bots via @BotFather in Telegram and change `TELEGRAM_TOKEN`, `ADMIN_TELEGRAM_TOKEN` variables in `.env` file.
5. Apply migraitons.
```bash
python manage.py migrate
```
6. Create superuser to get access to django admin panel.
```bash
python manage.py createsuperuser
```
7. Visit [admin-panel](http://127.0.0.1:8000/tgadmin/) to check that everything is alright.


## Running locally (manually).
1. Start bots
```bash
python run_pooling.py  # player's bot
python run_admin_pooling.py  # coach's bot in another terminal window
```
2. Start django.
```bash
python manage.py runserver
```

## Running locally (docker-compose).
```bash
docker-compose up -d --build
```

## Adding new features
1. Pull new changes from git.
```bash
git pull
```
2. Create new branch with short name explaining new feature.
3. Write code with **tests**.
4. Push changes and make `pull request` to *master* branch.
