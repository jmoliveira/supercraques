
SHELL := /bin/bash

root_dir=.
build_dir=${root_dir}/build
src_dir=${root_dir}/supercraques

dump_path=./supercraques/dump.sql

all: compile

clean:
	@echo "Executando clean"
	@find -name *.pyc -delete

dump:
	@echo "Iniciando processo de dump do path: ${dump_path} para a base de dados supercraques"
	@make drop_db create_db
	@mysql -u root --database supercraques < ${dump_path}
	@echo "Finalizado processo de dump"
	
compile:
	@echo "Compiling source code..."
	@rm -f -r ${src_dir}/*.pyc >> /dev/null
	@python -m compileall ${src_dir}

run: compile
	@echo "Executing app"
	@python ${src_dir}/start.py

db: drop_db create_db migrate_db

drop_db:
	@echo "Dropping database... supercraques"
	@mysql -u root -e 'DROP DATABASE IF EXISTS supercraques;'

create_db:
	@echo "Creating database... supercraques"
	@mysql -u root -e 'CREATE DATABASE IF NOT EXISTS supercraques;'

migrate_db:
	@echo "Migrating supercraques"
	@db-migrate -c supercraques/migrations/local.conf
	@echo "Database migrated!"
	