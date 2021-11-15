# Contributing

## Running locally
1. Create `.env` file
```bash
cp .env_example .env 
```
2. Create two bots and change `TELEGRAM_TOKEN`, `ADMIN_TELEGRAM_TOKEN`
3. Start bot's
```bash
python run_pooling.py  # player's bot
python run_admin_pooling.py  # coach's bot in another terminal window
```
4. Create superuser
```bash
python manage.py createsuperuser
```
5. Visit [admin-panel](http://127.0.0.1:8000/tgadmin/)

## Adding new features
1. Pull new changes
```bash
git pull
```
2. Create new branch with short name explaining new feature
3. Write code with **tests**
4. Push changes and make `pull request` to *master* branch.