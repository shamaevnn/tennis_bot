# Contributing

## First start
1. Create `.env` file.
```bash
cp .env_example .env # (uncomment one line with DATABASE_URL)
```
2. Create two bots via @BotFather in Telegram and change `TELEGRAM_TOKEN`, `ADMIN_TELEGRAM_TOKEN` variables in `.env` file.
3. Apply migraitons.
```bash
python manage.py migrate
```
4. Create superuser to get access to django admin panel.
```bash
python manage.py createsuperuser
```
5. Visit [admin-panel](http://127.0.0.1:8000/tgadmin/) to check that everything is alright.


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
