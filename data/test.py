from requests import get, post, delete

test_1 = False
if test_1:
    print(get('http://localhost:8000/api/jobs').json())
    print(get('http://localhost:8000/api/jobs/999999').json())
    # Не выдаст работу, тк работы с таким id не существует
    print(get('http://localhost:8000/api/jobs/').json())
    # Не выдасть работу, тк мы не даём id работы
    print(get('http://localhost:8000/api/jobs/n').json())
    # Не выдаст работу, тк мы даём str вместо int
