# What is this?

This repository contains a python script that generates fake data for Defguard system and inserts it into database. Data
that is generated includes:

- Users
- Devices

# How do I use it?

```
Usage: main.py [OPTIONS] COMMAND [ARGS]...

Options:
  --help  Show this message and exit.

Commands:
  insert-devices
  insert-users
```

To insert users:

```
main.py insert-users postgresql+psycopg2://defguard:defguard@localhost/defguard --count 1000
```

To insert devices:

```
main.py insert-devices postgresql+psycopg2://defguard:defguard@localhost/defguard --count 10 --user-id 1
```
