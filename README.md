# Family budget Telegram bot

</br>

✅ This is a family budget bot, developerd for Telegram messanger

✅ Use it as collaborational tool to save costs and incomes

✅ Also, you can find pertty usefull monthly or annually analytics



# Setup the environment

### Create environment configuration file based on `.env.example`
```bash
cp .env.example .env
```

### Install [pre-commit hooks](https://pre-commit.com/#install)
> Note: Install pre-commit tool before
```bash
pre-commit install
```

### Complete next variables:

| Key | Default value | Description |
| --- | ------------- | ----------- |
| `COMPOSE_FILE` | `docker-compose.yaml` | Docker-compose file you would like to use. Use `docker-compose.yaml` for production and `docker-compose.dev.yaml` for development
| `API_KEY` | - | Telegram API key. Get it from [**BotFather**](https://t.me/botfather) |
| `DATABASE_URL` | `postgresql://postgres:postgres@postgres:5432/family_budget` | Database URL that should match pattern: `db_engine://username:password@host:port/db_name` </br> **Note:** *currenctly Bot allowes you to use only `postgresql` database engine*
| `USERS_ACL` | - | The list of Telegram account ids. Set it not to show your data to other people. </br> **Note:** 99% of features allowed only for bot members you pass throw this variable |



# Setup

### with Docker

🔗  [Install Docker](https://docs.docker.com/get-docker/)

```bash
# Run docker-compose services as deaemon
docker-compose build
```


### with NO Docker

#### Install dependencies with Poetry & activate virtual environment
🔗  [Poetry official page](https://python-poetry.org)
```bash
# Install poetry
pip3 install -U poetry

# Install dependencies
poetry install
poetry shell
```



# Usage

### With Docker

```bash
# Run the container
docker-compose up -d
```
> Note: It will create 2 containers: **family_budget_bot_app** and **family_budget_bot_postgres**

> Note: database volume is static for the app. It means, that after removing any container your data will not be removed.


### With NO Docker
```bash
# Run the bot
python src/run.py
```
</br>



# Additional information

## Creating database dump cronjobs

#### Create a job on the hosting server

1. Connect to the server via SSH
```bash
ssh my_user@my_server
```

2. Open crontab editor
```bash
crontab -e
```

3. Add a new job for creating dumps every **5** hours
```bash
*   */5   *   *   *   docker exec family_budget_bot_postgres pg_dump -U postgres -d family_budget > /root/family_budget_bot/dump.sql
```

#### Create a job on local UNIX machine

1. Open crontab editor
```bash
crontab -e
```

2.1. Add a new job for copying dump from the server every **5** hours.
```bash
*   */5   *   *   *   scp <username>@<server>:/root/family_budget_bot/dump.sql $HOME/dumps/family_budget_dump.sql
```

2.2. Add a new job for copying dump from the server every **5** hours on MacOS to iCloud folder
```bash
*   */5   *   *   *   scp <username>@<server>:/root/family_budget_bot/dump.sql $HOME/Library/Mobile\ Documents/com~apple~CloudDocs/family_budget_dump.sql
```

</br>

### Restore from dump
Connect to the PostgreSQL with psql
```bash
$ docker-compose exec postgrers psql
```

Exec commands below
```postgres
postgres=# DROP DATABASE family_budget;
postgres=# CREATE DATABASE family_budget;
postgres=# \q
```

Ingest data into database
```bash
docker-compose -T exec postgrers psql -U postgres family_budget < dump.sql
```

# Images
### Start the bot
<img width="1382" alt="image" src="https://user-images.githubusercontent.com/45270625/164975013-ed323070-ae0f-464f-8b45-22bb4960ca5e.png">

### Monthly analytics
<img width="1382" alt="image" src="https://user-images.githubusercontent.com/45270625/164975082-bba2ee53-877a-44d7-b6e8-6cefbb84ac42.png">

### Adding costs process
<img width="1359" alt="image" src="https://user-images.githubusercontent.com/45270625/164975104-f7ebf517-7a78-4979-8b57-461b0d7e735f.png">

### Removing costs process
<img width="1150" alt="image" src="https://user-images.githubusercontent.com/45270625/165398291-454ca4fd-c4e2-41b0-bdd1-b373be897bf0.png">

### Equity
<img width="1362" alt="image" src="https://user-images.githubusercontent.com/45270625/165388913-ed52bffb-3d94-4f69-a93b-cfbd97b32c25.png">

### Flexible configurations
<img width="1146" alt="image" src="https://user-images.githubusercontent.com/45270625/165398121-a9191fad-9946-4467-97af-61cf62ee8bcd.png">

