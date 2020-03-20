from requests import get, post, delete, put

test_1 = False
test_2 = False
test_3 = False
if test_1:
    print(get('http://localhost:8000/api/jobs').json())
    print(get('http://localhost:8000/api/jobs/999999').json())
    # Не выдаст работу, тк работы с таким id не существует
    print(get('http://localhost:8000/api/jobs/').json())
    # Не выдасть работу, тк мы не даём id работы
    print(get('http://localhost:8000/api/jobs/n').json())
    # Не выдаст работу, тк мы даём str вместо int
if test_2:
    print(get('http://localhost:8000/api/jobs').json())
    print(delete('http://localhost:8000/api/jobs/2').json())
    print(get('http://localhost:8000/api/jobs').json())
    # Удачное удаление
    print(delete('http://localhost:8000/api/jobs/9999999').json())
    # Не удалит, тк нет работы с таким id
    print(delete('http://localhost:8000/api/jobs/').json())
    # Не удалит работу, тк мы не даём id работы
    print(delete('http://localhost:8000/api/jobs/n').json())
    # Не удалит работу, тк мы даём str вместо int
if test_3:
    print(put('http://localhost:8000/api/jobs/1', json={'work_size': 300}).json())
