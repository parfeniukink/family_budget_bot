DB_REGEX = (
    r"^(?P<db_engine>.*):\/\/((?P<db_username>[^:]*):(?P<db_password>[^@]*)@"
    r"(?P<db_hostname>[^:/]*)(:(?P<db_port>\d+))?\/)?(?P<db_name>.*)$"
)
