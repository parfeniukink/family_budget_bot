# Family budget Telegram bot

</br>

✅ This is a family budget bot, developed for Telegram messenger

✅ Use it as collaboration tool to save costs and incomes

✅ Also, you can find pretty useful monthly or annually analytics



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
| `DATABASE_URL` | `postgresql://postgres:postgres@postgres:5432/family_budget` | Database URL that should match pattern: `db_engine://username:password@host:port/db_name` </br> **Note:** *curently Bot allows you to use only `postgresql` database engine*
| `USERS_ACL` | - | The list of Telegram account ids. Set it not to show your data to other people. </br> **Note:** 99% of features allowed only for bot members, you pass throw this variable |



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
<image src="https://user-images.githubusercontent.com/45270625/166680780-4c0e004a-929b-438b-aaff-6b39052b1197.png" width="400" height="800"/>


### Adding costs process
<image align="left" src="https://user-images.githubusercontent.com/45270625/166680891-db15e3ca-45d4-4030-b5f1-35afb9fd0b63.png" width="400" height="800"/>
<image src="https://user-images.githubusercontent.com/45270625/166681049-90dc1a22-d2ae-40f6-9f9e-afdd8aff4ad2.png" width="400" height="800"/>


### Removing costs process
<image align="left" src="https://user-images.githubusercontent.com/45270625/166681180-26e28542-6f94-4b4f-8abf-a50accad92a7.png" width="400" height="800"/>
<image src="https://user-images.githubusercontent.com/45270625/166681364-3c5f82ec-1d15-49df-9422-ffacaa0fa057.png" width="400" height="800"/>


### Adding incomes process
<image align="left" src="https://user-images.githubusercontent.com/45270625/166682417-61c34b04-3405-4527-a312-dd618e42a2a2.png" width="400" height="800"/>
<image src="https://user-images.githubusercontent.com/45270625/166682497-9ccb105a-2b25-4969-b40c-09181d3918da.png" width="400" height="800"/>
<image align="left" src="https://user-images.githubusercontent.com/45270625/166682534-5ac10762-50dc-4539-827b-1fee73a8bf4d.png" width="400" height="800"/>
<image src="https://user-images.githubusercontent.com/45270625/166682568-78f8ccb1-9f6e-4290-9fec-128b1a824e17.png" width="400" height="800"/>


### Monthly analytics
<image align="left" src="https://user-images.githubusercontent.com/45270625/166681415-f282f41d-5e76-458f-b803-5918b369b413.png" width="400" height="800"/>
<image src="https://user-images.githubusercontent.com/45270625/166681471-51d70d6f-678b-44ae-83e1-4358fd11218d.png" width="400" height="800"/>
<image src="https://user-images.githubusercontent.com/45270625/166681856-46aa4790-185a-48ea-ade4-de2f693004a1.jpeg" width="400" height="800"/>


### Equity
<image src="https://user-images.githubusercontent.com/45270625/166681912-132c7cdb-b7b4-4e59-bbeb-606708989496.png" width="400" height="800"/>


### Flexible configurations
<image align="left" src="https://user-images.githubusercontent.com/45270625/166681975-1cb4cc6a-31f9-499d-b650-254e29b98e45.png" width="400" height="800"/>
<image src="https://user-images.githubusercontent.com/45270625/166682221-71dfffae-83ac-4652-9522-3d194351545e.png" width="400" height="800"/>
