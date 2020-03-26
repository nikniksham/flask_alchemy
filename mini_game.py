from io import BytesIO
import pygame
import requests
import random


#                       ----->Документация по мини игре<-----
#         После того, как будет программа будет запущена, начнётся подготовка файлов для игры
#         Подготовка данных будет осуществлятся по городам в списке sites, вы можете изменить его!
#                                       | | | | | | | | | | | | | | | | |
#                                       | | | | | | | | | | | | | | | | |
#                                       | | | | | | | | | | | | | | | | |
#                                       V V V V V V V V V V V V V V V V V
sites = ['Москва', 'Санкт-Петербург', 'Волгоград', 'Омск', 'Красноярск', 'Новгород',
         'Архангельск', 'Казань', 'Самара', 'Екатеринбург']
#        Горячие клавиши для игры:
#        1) Вправо/влево - следущий/предыдущий кадр
#        2) Esc - завершить игровую ссесию
#        3) 1 - Игрок готов отвечать, что за город (ответ осуществляется в консоль)
#        Если ответ был правильным, то отгадывающий получает 1 очко, если нет, то загадывающий,
#        далее игроки меняются местами
#        4) 2 - Завершить игру, выводится меню с очками, или игра завершится, когда города закончатся


def write_text(text, text_coord, font_size=36, font_color=(255, 255, 255)):
    f = pygame.font.SysFont('serif', font_size)
    text = f.render(text, 1, font_color)
    screen.blit(text, text_coord)


class TextForWaiting:
    def __init__(self, texts):
        self.texts = texts
        self.text = -1

    def next_text_for_waiting(self, site):
        screen.fill((0, 0, 0))
        self.text += 1
        if self.text >= len(self.texts):
            self.text = 0
        write_text(self.texts[self.text] + f' ({site})', [10, 400], font_size=22)
        pygame.display.flip()


waiting = TextForWaiting(['Подготовка файлов для игры', 'Подготовка файлов для игры.',
                          'Подготовка файлов для игры..', 'Подготовка файлов для игры...'])


class Player:
    def __init__(self, name):
        self.name = name
        self.score = 0

    def set_name(self, name):
        self.name = name

    def get_name(self):
        return self.name

    def upgrade_score(self, upgrade_points):
        self.score += upgrade_points

    def get_score(self):
        return self.score


class MiniGame:
    def __init__(self, sites):
        self.slides_sat = {}
        self.slides_map = {}
        self.sites = sites
        self.sites.sort()
        self.status_game = True
        self.guessing_player = None
        self.setting_player = None
        self.slide = 0
        self.city = ''
        self.players = []
        self.kinds_slides = ['map', 'sat']
        self.search_api_server = "https://search-maps.yandex.ru/v1/"
        self.map_api_server = "http://static-maps.yandex.ru/1.x/"
        self.api_key = "dda3ddba-c9ea-4ead-9010-f43fbc15c6e3"

    def set_city(self, city):
        self.city = city

    def create_slides(self):
        for site in self.sites:
            if site not in list(self.slides_sat.keys()):
                self.slides_sat[site] = []
                self.slides_map[site] = []
        for site in sites:
            json_response = requests.get(
                f'https://geocode-maps.yandex.ru/1.x/?apikey=40d1649f-0493-4b70-98ba-98533de7710b&geocode={site}&format=json')
            coord = ','.join(
                json_response.json()['response']['GeoObjectCollection']['featureMember'][0]['GeoObject']["Point"][
                    "pos"].split())
            self.add_slide(coord, site)
            corners = json_response.json()['response']['GeoObjectCollection']['featureMember'][0]['GeoObject'][
                'boundedBy']['Envelope']
            upper_corner = corners['upperCorner'].split()
            lower_corner = corners['lowerCorner'].split()
            x = [float(lower_corner[0]), abs(float(lower_corner[0]) - float(upper_corner[0]))]
            y = [float(lower_corner[1]), abs(float(lower_corner[1]) - float(upper_corner[1]))]
            for i in range(4):
                new_coord = f'{x[0] + x[1] / random.choice(range(1, 11))},{y[0] + y[1] / random.choice(range(1, 11))}'
                self.add_slide(new_coord, site)
        self.set_image()

    def add_slide(self, coord, site):
        waiting.next_text_for_waiting(site)
        map_params = {
            "ll": coord,
            "spn": '0.033,0.033',
            "l": "map",
            "size": "600,450"
        }
        response = requests.get(self.map_api_server, params=map_params)
        self.slides_map[site].append(pygame.image.load(BytesIO(response.content)))
        map_params['l'] = 'sat'
        response = requests.get(self.map_api_server, params=map_params)
        self.slides_sat[site].append(pygame.image.load(BytesIO(response.content)))

    def next_slide(self):
        self.slide += 1
        if self.slide == len(self.slides_map[self.city]):
            self.slide = 0
        self.set_image()

    def prev_slide(self):
        self.slide -= 1
        if self.slide < 0:
            self.slide = len(self.slides_map[self.city]) - 1
        self.set_image()

    def set_image(self, kind_slide=None):
        if kind_slide is None or kind_slide not in self.kinds_slides:
            kind_slide = random.choice(self.kinds_slides)
        if kind_slide == 'sat':
            screen.blit(self.slides_sat[self.city][self.slide], [0, 0])
        if kind_slide == 'map':
            screen.blit(self.slides_map[self.city][self.slide], [0, 0])

    def set_players(self, player_1, player_2):
        self.players.append(player_1)
        self.players.append(player_2)
        self.guessing_player = player_1
        self.setting_player = player_2

    def set_guessing_player(self):
        self.guessing_player, self.setting_player = self.setting_player, self.guessing_player

    def get_guessing_player(self):
        return self.guessing_player.get_name()

    def answer(self, answer):
        if self.city.lower() == answer.lower():
            self.guessing_player.upgrade_score(1)
            print(f'Это верный ответ, это {answer}')
        else:
            self.setting_player.upgrade_score(1)
            print(f'Увы, но вы ошиблись =(, это не {answer}')
        self.sites.remove(self.city)
        if len(self.sites) == 0:
            self.set_status_game(False)
        else:
            self.city = random.choice(self.sites)
            self.set_guessing_player()
            self.set_image("sat")

    def rating_table(self):
        screen.fill((0, 0, 0))
        write_text(self.players[0].get_name(), [10, 10])
        write_text(self.players[1].get_name(), [300, 10])
        write_text('Очки:', [10, 60])
        write_text(str(self.players[0].get_score()), [10, 110])
        write_text('Очки:', [300, 60])
        write_text(str(self.players[1].get_score()), [300, 110])
        player = self.get_max_score()
        if player is not None:
            write_text(f'Победил: {player.get_name()}', [10, 160])
            write_text(f'У него: {player.get_score()} очков', [10, 210])
        else:
            write_text(f'Победила дружба - ничья!', [10, 160])

    def get_max_score(self):
        player_max_score = None
        max_score = -1
        for player in self.players:
            if player.get_score() == max_score:
                player_max_score = None
            if player.get_score() > max_score:
                max_score = player.get_score()
                player_max_score = player
        return player_max_score

    def get_status_game(self):
        return self.status_game

    def set_status_game(self, status):
        self.status_game = status


player_1 = Player('Бобр добр')
player_2 = Player('Николя')
pygame.init()
size = w, h = [600, 450]
screen = pygame.display.set_mode(size)
pygame.display.flip()
clock = pygame.time.Clock()
mini_game = MiniGame(sites)
mini_game.set_city(random.choice(sites))
mini_game.create_slides()
mini_game.set_players(player_1, player_2)
tik = 0
while True:
    if mini_game.get_status_game():
        write_text(f'Отвечает игрок: {mini_game.get_guessing_player()}', [10, 10], font_color=(0, 0, 0))
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    quit()
                if event.key == pygame.K_RIGHT:
                    mini_game.next_slide()
                if event.key == pygame.K_LEFT:
                    mini_game.prev_slide()
                if event.key == pygame.K_1:
                    mini_game.answer(input('Введите название города: '))
                if event.key == pygame.K_2:
                    mini_game.set_status_game(False)

    else:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    quit()
        mini_game.rating_table()
    pygame.display.flip()
    clock.tick(60)
