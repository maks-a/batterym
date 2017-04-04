coverage run batterym/unittests.py
coverage report --omit=batterym/unittests.py,batterym/main.py
coverage html --omit=batterym/unittests.py,batterym/main.py