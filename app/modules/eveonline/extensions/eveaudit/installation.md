# Installation
To install, simply enable the extension in settings.py

# Disabling
Disabling is where it gets difficult.

Due to dependencies the and relations it makes to the EVE Online module, you must drop the MySQL table.

1. `mysql -u {user} -p`
2. `use {database}`
3. `DROP TABLE eveaudit_evecharacterdata`

# Re-enabling
Since we dropped the table from last time, it's a bit more involved to re-enable.

1. Undo the migration `python3 manage.py migrate eveaudit zero`
2. Reapply the migration `python3 manage.py migrate`