dev:
	docker compose -f docker-compose.yml up --build
logs:
	docker compose -f docker-compose.yml logs -f web
migrate:
	docker compose -f docker-compose.yml exec expense_web python manage.py migrate
shell:
	docker compose -f docker-compose.yml exec expense_web python manage.py shell