up:
	docker compose -f docker-compose.yml up --build

up-dev:
	docker compose -f docker-compose.yml -f docker-compose.dev.yml up --build

down:
	docker compose down -v

logs:
	docker compose -f docker-compose.yml logs -f web

migrate:
	docker compose -f docker-compose.yml exec expense_web python manage.py migrate

shell:
	docker compose -f docker-compose.yml exec expense_web python manage.py shell

lint:
	flake8 apps expense_tracking manage.py

format:
	black apps expense_tracking manage.py
	isort apps expense_tracking manage.py

typecheck:
	mypy apps expense_tracking manage.py --explicit-package-bases

precommit:
	pre-commit run --all-files

install-hooks:
	pre-commit install

test:
	 pytest --cov --cov-report term

seed-categories:
	docker compose -f docker-compose.yml exec expense_web python manage.py seed_categories

collectstatic:
	docker compose -f docker-compose.yml exec expense_web python manage.py collectstatic