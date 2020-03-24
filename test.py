from requests import get, post, delete, put

test_version_first = True
test_version_second = False

# методы
test_get = False
test_post = False
test_delete = False
test_put = True
# api.add_resource(user_resources.UserListResource, '/api/v2/user')
# api.add_resource(user_resources.UserResource, '/api/v2/user/<int:user_id>')
if test_version_first:
    print(get('http://localhost:8000/api/v2/user').json())
    if test_get:
        print(get('http://localhost:8000/api/v2/user/1').json())
        print(get('http://localhost:8000/api/v2/user/223').json())
        print(get('http://localhost:8000/api/v2/user/c').json())

    if test_post:
        print('пустой запрос')
        print(post('http://localhost:8000/aapi/v2/user').json())
        print('не полный запрос')
        print(post('http://localhost:8000/api/v2/user',
                   json={'name': 'Николай'}).json())
        print('желаемый id уже занят')
        print(post('http://localhost:8000/api/v2/user',
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
        print(post('http://localhost:8000/api/v2/user',
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
        print(get('http://localhost:8000/api/v2/user').json())

    if test_delete:
        print('нет в базе')
        print(delete('http://localhost:8000/api/v2/user/999').json())
        print('Успешно удалён')
        print(delete('http://localhost:8000/api/v2/user/10').json())
        print(get('http://localhost:8000/api/v2/user').json())

    if test_put:
        print('нет в базе')
        print(put('http://localhost:8000/api/v2/user/999').json())
        print('Успешно изменён')
        print(put('http://localhost:8000/api/v2/user/2',
                   json={'age': 20}).json())
        print(get('http://localhost:8000/api/v2/user').json())

if test_version_second:
    if test_get:
        print(get('http://localhost:8000/api/jobs/').json())
        print(get('http://localhost:8000/api/jobs/1').json())
        print(get('http://localhost:8000/api/jobs/100').json())
        print(get('http://localhost:8000/api/jobs/c').json())

    if test_post:
        print('пустой запрос')
        print(post('http://localhost:8000/api/jobs').json())
        print('не полный запрос')
        print(post('http://localhost:8000/api/jobs',
                   json={'job': 'Заголовок'}).json())
        print('желаемый id уже занят')
        print(post('http://localhost:8000/api/jobs',
                   json={'job': 'Заголовок',
                         'team_leader': 1,
                         'work_size': 1,
                         'collaborators': "все",
                         'is_finished': True,
                   'id': 1}).json())
        print('правильный запрос')
        print(post('http://localhost:8000/api/jobs',
                   json={'job': 'Заголовок',
                         'team_leader': 1,
                         'work_size': 1,
                         'collaborators': "все",
                         'is_finished': True,
                         'id': 10}).json())
        print(get('http://localhost:8000/api/jobs/').json())

    if test_delete:
        print('нет в базе')
        print(delete('http://localhost:8000/api/jobs/999').json())
        print('Успешно удалена')
        print(delete('http://localhost:8000/api/jobs/1').json())
        print(get('http://localhost:8000/api/jobs/').json())

    if test_put:
        print('нет в базе')
        print(put('http://localhost:8000/api/jobs/999').json())
        print('Успешно изменена')
        print(put('http://localhost:8000/api/jobs/10',
                   json={'job': 'нет загаловка'}).json())
        print(get('http://localhost:8000/api/jobs/').json())