.PHONY: sandbox

sandbox:
	-rm sandbox/sandbox/sandbox.sqlite3
	./sandbox/manage.py syncdb --noinput
	./sandbox/manage.py migrate
	./sandbox/manage.py loaddata sandbox/fixtures/auth.json
	./sandbox/manage.py loaddata countries.json ticket_types.json ticket_statuses.json
