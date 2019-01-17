# test.helper.yandex.alice.flask

[![Python 2.7.14 3.6.3 3.7-dev](https://img.shields.io/travis/vb64/test.helper.yandex.alice.flask.svg?label=Python%202.7%203.6%203.7&style=plastic)](https://travis-ci.org/vb64/test.helper.yandex.alice.flask)
[![Code Climate](https://codeclimate.com/github/codeclimate/codeclimate/badges/gpa.svg)](https://codeclimate.com/github/vb64/test.helper.yandex.alice.flask)

Класс python для автоматического тестирования навыка Яндекс Алиса, реализованного на python/flask.

Установка:
```
$ pip install tester_alice_skill_flask
```

Использование:
```python

from tester_alice_skill_flask import Interface, Skill
from buy_elephant import app  # импортируем приложение flask из тестируемой программы

# создаем экземпляр навыка
skill = Skill(
  app,
  'xxx-yyy-zzz',  # идентификатор навыка из кабинета разработчика
  '/alice',  # адрес, на котором приложение принимает запросы от Алисы
  is_screen_need=False  # наличия устройства с экраном для работы навыка не требуется
)

# новая сессия работы с Яндекс.Алиса
session = skill.new_session(
  '1234567890',  # ID пользователя Алисы, создавшего сессию
  [Interface.Screen],  # сессия открывается для устройства с экраном
  locale='ru-RU',
  timezone="Europe/Moscow",
  client_id="ru.yandex.searchplugin/5.80 (Samsung Galaxy; Android 4.4)",
  command=""  # опциональная команда, передаваемая при запуске навыка. например, 'помощь'
)

# история диалога содержит подстроку
session.contain("Купи слона!")
True

# диалог содержит две кнопки
len(session.buttons)
2

# нажать первую кнопку
session.send_button(0)

session.contain("Все говорят")
True

# послать текст
session.send("Отстань!", command="", nlu={"entities": [], "tokens": []})

# вывести текущую историю диалога
print(session.dump())

Q:
A: Привет! Купи слона!

Q: [Не хочу.]
A: Все говорят "Не хочу.", а ты купи слона!

Q: Отстань!
A: Все говорят "Отстань!", а ты купи слона!

[Отстань!] [Ладно]

# очистить историю диалога
session.clear()

# купить слона
session.send("ладно")

session.contain("Слона можно найти на Яндекс.Маркете!")
True

session.contain("Все говорят")
False

```
