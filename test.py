from requests import get, post, delete, put

# Тесты: 1 - api/v2/user; 2 - api/v2/jobs
test_version_first = False
test_version_second = True

# методы
test_get = False
test_post = False
test_delete = True
test_put = False
if test_version_first:
    print(get('http://localhost:8100/api/v2/user').json())
    if test_get:
        print('Пустой запрос')
        print(get('http://localhost:8100/api/v2/user/').json())
        print('Правильный запрос')
        print(get('http://localhost:8100/api/v2/user/1').json())
        print('Не существующий id')
        print(get('http://localhost:8100/api/v2/user/223').json())
        print('Не правильный id')
        print(get('http://localhost:8100/api/v2/user/c').json())

    if test_post:
        print('пустой запрос')
        print(post('http://localhost:8100/aapi/v2/user').json())
        print('не полный запрос')
        print(post('http://localhost:8100/api/v2/user',
                   json={'name': 'Николай'}).json())
        print('желаемый id уже занят')
        print(post('http://localhost:8100/api/v2/user',
                   json={'id': 1,
                         'name': 'Николай',
                         'surname': 'Шамков',
                         'age': 16,
                         'position': 'Стажёр',
                         'speciality': 'Программист',
                         'address': 'module_1',
                         'email': 'nikniksham@gmail.com',
                         'city_from': 'Москва',
                         'password': '123'}).json())
        print('правильный запрос')
        print(post('http://localhost:8100/api/v2/user',
                   json={'id': 10,
                         'name': 'Николай',
                         'surname': 'Шамков',
                         'age': 16,
                         'position': 'Стажёр',
                         'speciality': 'Программист',
                         'address': 'module_1',
                         'email': 'nikniksham@gmail.com',
                         'city_from': 'Москва',
                         'password': '123'}).json())

    if test_delete:
        print('нет в базе')
        print(delete('http://localhost:8100/api/v2/user/999').json())
        print('Успешно удалён')
        print(delete('http://localhost:8100/api/v2/user/10').json())

    if test_put:
        print('нет в базе')
        print(put('http://localhost:8100/api/v2/user/999').json())
        print('Успешно изменён')
        print(put('http://localhost:8100/api/v2/user/2',
                   json={'age': 20}).json())
    print(get('http://localhost:8100/api/v2/user').json())

if test_version_second:
    print(get('http://localhost:8100/api/v2/jobs').json())
    if test_get:
        print('Пустой запрос')
        print(get('http://localhost:8100/api/v2/jobs/').json())
        print('Успешный запрос')
        print(get('http://localhost:8100/api/v2/jobs/1').json())
        print('Не существующий id')
        print(get('http://localhost:8100/api/v2/jobs/100').json())
        print('Не правильный id')
        print(get('http://localhost:8100/api/v2/jobs/c').json())

    if test_post:
        print('пустой запрос')
        print(post('http://localhost:8100/api/v2/jobs').json())
        print('не полный запрос')
        print(post('http://localhost:8100/api/v2/jobs',
                   json={'id': 10}).json())
        print('желаемый id уже занят')
        print(post('http://localhost:8100/api/v2/jobs',
                   json={'id': 1,
                         'team_leader': 1,
                         'job': 'Заголовок',
                         'work_size': 1,
                         'collaborators': "все",
                         'speciality': 'специальность',
                         'hazard_category': 3,
                         'is_finished': True}).json())
        print('правильный запрос')
        print(post('http://localhost:8100/api/v2/jobs',
                   json={'id': 10,
                         'team_leader': 1,
                         'job': 'Заголовок',
                         'work_size': 1,
                         'collaborators': "все",
                         'speciality': 'специальность',
                         'hazard_category': 3,
                         'is_finished': True}).json())

    if test_delete:
        print('нет в базе')
        print(delete('http://localhost:8100/api/v2/jobs/999').json())
        print('Успешно удалена')
        print(delete('http://localhost:8100/api/v2/jobs/4').json())

    if test_put:
        print('нет в базе')
        print(put('http://localhost:8100/api/v2/jobs/999').json())
        print('Успешно изменена')
        print(put('http://localhost:8100/api/v2/jobs/10',
                   json={'job': 'Нет Заголовка'}).json())
    print(get('http://localhost:8100/api/v2/jobs').json())
