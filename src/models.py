from enum import Enum
from datetime import datetime


class Map(Enum):
    MALLARDON = "Маллардон"
    THE_CARNIVAL = "Карнавал"
    EAGLETON_SPRINGS = "Иглтон Спрингс"
    BLOODHAVEN = "Кровавая Гавань"
    ANCIENT_SANDS = "Древняя Пустыня"
    THE_BASEMENT = "Подвал"
    JUNGLE_TEMPLE = "Храм Джунглей"
    GOOSECHAPEL = "Гусчэпл"
    MALLARD_MANOR = "Усадьба Крякв"
    NEXUS_COLONY = "Колония Нексус"
    BLACK_SWAN = "Черный Лебедь"
    SS_MOTHER_GOOSE = "К.К. Матушка Гусыня"
    OTHER = "Разные"


class GameMode(Enum):
    CLASSIC = "Classic"
    DRAFT = "Draft"
    CORRUPTION_MODE = "Corruption Mode"
    GOOSE_HUNT = "Goose Hunt"
    DINE_AND_DASH = "Dine and Dash"
    TRICK_OR_TREAT = "Trick or Treat"
    HANGING_OUT = "Hanging Out"
    TASTES_LIKE_CHICKEN = "Tastes Like Chicken"
    WOW_AND_LOCK = "Ух и ищи"
    OTHER = "Разные"


class ChooseEditEnum(Enum):
    code = "Код"
    host = "Хоста"
    map = "Карту"
    game_mode = "Режим"


class AnswerEnum(Enum):
    we_have_cancel = "У нас отмена!"
    error_code = "<b>Ошибка при вводе.</b> \n\nПожалуйста, введите 7-значный код комнаты"
    error_host = "<b>Ошибка при вводе.</b> \n\nПожалуйста, введите имя хоста (не более 15 символов):"
    choose_code = "Введите код комнаты"
    choose_host = "Введите имя хоста:"
    choose_map = "Выберите карту:"
    choose_game_mode = "Выберите режим игры:"
    choose_edit = "Выберите что изменить:"
    choose_room = "Выберите комнату:"
    info_added_room = "Комната добавлена успешно!"
    not_found = "Увы... Нет подходящей комнаты 😢"
    not_found_rooms = "Упс...\n\nНет опубликованных комнат 😢"
    success_edit = "Изменения приняты!"
    error_edit = "Изменения не приняты, попробуйте что-то исправить 😢"
    room_delite = "Комната удалена."
    room_delite_plus = "Комната удалена.\n\nТеперь вы можете добавить новую."
    invalid_option = "Пожалуйста, выберите один из предложенных вариантов или нажмите 'Отмена'."
    you_dont_have_root = "У вас нет прав для использования этой команды."


class QueryCommand(Enum):
    subscribe = "подписаться"
    unsubscribe = "отписаться"
    like = "like"
    dislike = "dislike"


class Chat:
    def __init__(self, chat_id: int):
        self.chat_id = chat_id

    def to_dict(self):
        return {
            'chat_id': self.chat_id
        }

    @classmethod
    def from_dict(cls, data):
        if data is None:
            raise ValueError("Cannot create Chat from None")

        return cls(
            chat_id=data['chat_id']
        )


class Rating:
    def __init__(self, rating: bool, user_id: int):
        self.rating = rating
        self.user_id = user_id

    def to_dict(self):
        return {
            'rating': self.rating,
            'user_id': self.user_id
        }

    @classmethod
    def from_dict(cls, data):
        if data is None:
            raise ValueError("Cannot create Rating from None")

        return cls(
            rating=data['rating'],
            user_id=data['user_id']
        )


class User:
    def __init__(self, user_id: int, is_admin: bool = False, subscribers=None, rating=None):
        self.user_id = user_id
        self.is_admin = is_admin
        self.subscribers = subscribers or []
        self.rating = rating or []

    def to_dict(self):
        return {
            'user_id': self.user_id,
            'is_admin': self.is_admin,
            'subscribers': [subscriber.to_dict() for subscriber in self.subscribers],
            'rating': [rating_item.to_dict() for rating_item in self.rating],
        }

    @classmethod
    def from_dict(cls, data):
        if data is None:
            raise ValueError("Cannot create User from None")

        subscribers = [Chat.from_dict(subscriber) for subscriber in data.get('subscribers', [])]
        rating = [Rating.from_dict(rating_item) for rating_item in data.get('rating', [])]
        return cls(
            user_id=data['user_id'],
            is_admin=data['is_admin'],
            subscribers=subscribers,
            rating=rating
        )


class Room:
    def __init__(self, code: str, host: str, map: Map, game_mode: GameMode, owner: User, chat: Chat, created_at=None):
        self.code = code.upper().strip()
        self.host = host.strip()
        self.map = map
        self.game_mode = game_mode
        self.owner = owner
        self.chat = chat
        self.created_at = created_at or datetime.now()

    def to_dict(self):
        return {
            'code': self.code,
            'host': self.host,
            'map': self.map.value,
            'game_mode': self.game_mode.value,
            'owner': self.owner.to_dict(),
            'chat': self.chat.to_dict(),
            'created_at': self.created_at
        }

    @classmethod
    def from_dict(cls, data):
        if data is None:
            raise ValueError("Cannot create Rooms from None")

        return cls(
            code=data['code'],
            host=data['host'],
            map=Map(data['map']),
            game_mode=GameMode(data['game_mode']),
            owner=User.from_dict(data['owner']),
            chat=Chat.from_dict(data['chat']),
            created_at=data['created_at']
        )
