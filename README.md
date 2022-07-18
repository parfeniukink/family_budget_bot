# Family Budget Bot

</br>

<p align="left">

<a href="https://app.circleci.com/pipelines/github/parfeniukink/family_budget_bot" target="_blank">
    <img src="https://circleci.com/gh/parfeniukink/family_budget_bot.svg?style=svg">
</a>

<a href="https://github.com/parfeniukink/family_budget_bot/releases" target="_blank">
    <img src="https://img.shields.io/github/license/parfeniukink/family_budget_bot?color=green">
</a>

<a href="https://shields.io/" target="_blank">
    <img src="https://img.shields.io/badge/python_versions-3.10+-blue.svg">
</a>

<a href="https://github.com/parfeniukink/family_budget_bot/releases" target="_blank">
    <img src="https://img.shields.io/github/v/release/parfeniukink/family_budget_bot">
</a>

</p>


</br>


<b><p align="left">✔️ A family budget bot developed for Telegram users</p>

<p align="left">✔️ Shared database with specified members</p>

<p align="left">✔️ Montly & annually analytics</p></b>


</br>


## Table of content

1. [Setup the environment](#setup-the-environment)

2. [Setup the application](#setup-the-application)

3. [Usage](#usage)

4. [Additional information](#additional-information)

    4.1 [Creating database dump cronjobs](#creating-database-dump-cronjobs)

    4.2 [Restore from dump](#restore-from-dump)

    4.3 [Upgrade release version](#upgrade-release-version)

4. [Images](#images)

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



# Setup the application

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

> 🤔 If you have cloud storage that synchronizes with your local folder would be great to set up copying from the external server right into your cloud folder.
>
> 👉🏻 For that you can create an independent cronjob on server that creates database dumps and another cronjob that works on your local machine that copying it from the server. (P.S. I choose this flow as far I found it better not to give extra access to the server)

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

2.2. Add a new job for copying dump from the server every **5** hours on MacOS to the iCloud folder
```bash
*   */5   *   *   *   scp <username>@<server>:/root/family_budget_bot/dump.sql $HOME/Library/Mobile\ Documents/com~apple~CloudDocs/family_budget_dump.sql
```

</br>

### Restore from dump
Connect to the PostgreSQL with psql
```bash
$ docker-compose exec postgrers psql
```

Remove old data
```postgres
postgres=# DROP DATABASE family_budget;
postgres=# CREATE DATABASE family_budget;
postgres=# \q
```

Ingest data into the database
```bash
docker-compose -T exec postgrers psql -U postgres family_budget < dump.sql
```

### Upgrade release version

> Currently we don't support any migration tools like alembic for upgrade or downgrade the database.
>
> But anyway, you can use custom created migration scripts that work only in case you want to upgrade.


💡 If I use version `2` and I'd like to upgrade to `3+`

📍 Make sure that you set the `PYTHONPATH` in the `.env` file

⚠️  You can not upgrade from version `2` to version `4`

⚠️  If you have version `3` and you would like to upgrade to the version `4.2` first you have to upgrade to the version `4.0`

</br>

👇 <b><u>Upgrade could be done just running the specific script</u></b> 👇

```python
# Using Docker
docker-compose exec bot python scripts/db/release_<version>_migration.py

# With NO Docker
python scripts/db/release_<version>_migration.py
```


# Images


### Configurations

> Here you can easily take a look all or change bot configurations

##### Allowed configurations:

👉🏻 Number of dates behind for adding costs & taking a look the analytics & removings costs

👉🏻 Default currency that applies when you add cost (not to set it every time manually)

👉🏻 Costs sources that shows you keyboard with text snippets not to enter common stuff every time

👉🏻 Incomes sources that shows you keyboard with text snippets not to enter common stuff every time

<image src="https://media.giphy.com/media/uMfLHU8ALHtVARoCY7/giphy.gif" width="400"/>


### Analytics

<image src="https://media.giphy.com/media/GHclnxSDsmkwglrYcR/giphy.gif
" width="400"/>


### Adding and removnig costs process



<image align="left" src="https://media.giphy.com/media/arNzYpAUU75DyOY5fH/giphy.gif" width="400"/>
<image src="https://media.giphy.com/media/1hrS1Zkbm3soRklWFI/giphy.gif" width="400"/>


### Adding incomes
<image src="https://media.giphy.com/media/q2BxepdQfxC3x9J3QQ/giphy.gif" width="400"/>
