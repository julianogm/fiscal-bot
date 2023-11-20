start:
	python3 main.py
test:
	coverage run -m pytest && coverage html
coverage:
	xdg-open htmlcov/index.html > /dev/null 2>&1
