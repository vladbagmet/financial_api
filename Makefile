start:
	# Be sure to use 0.0.0.0 for the host within the Docker container,
	# otherwise the browser won't be able to find it
	docker-compose run --rm --service-ports backend sh -c "python manage.py migrate & python manage.py runserver 0.0.0.0:8000"

test:
	@docker-compose run --rm backend python manage.py test
