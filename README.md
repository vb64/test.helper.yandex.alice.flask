# Класс для автотестов навыка ЯндексАлисы

[![GitHub Workflow Status](https://img.shields.io/github/actions/workflow/status/vb64/test.helper.yandex.alice.flask/pep257.yml?label=Pep257&style=plastic&branch=master)](https://github.com/vb64/test.helper.yandex.alice.flask/actions?query=workflow%3Apep257)
[![GitHub Workflow Status](https://img.shields.io/github/actions/workflow/status/vb64/test.helper.yandex.alice.flask/py2.yml?label=Python%202.7&style=plastic&branch=master)](https://github.com/vb64/test.helper.yandex.alice.flask/actions?query=workflow%3Apy2)
[![GitHub Workflow Status](https://img.shields.io/github/actions/workflow/status/vb64/test.helper.yandex.alice.flask/py3.yml?label=Python%203.7-3.10&style=plastic&branch=master)](https://github.com/vb64/test.helper.yandex.alice.flask/actions?query=workflow%3Apy3)
[![Codacy Badge](https://app.codacy.com/project/badge/Grade/936dcebe15214c6baded2a7470d520e3)](https://app.codacy.com/gh/vb64/test.helper.yandex.alice.flask/dashboard?utm_source=gh&utm_medium=referral&utm_content=&utm_campaign=Badge_grade)
[![Codacy Badge](https://app.codacy.com/project/badge/Coverage/936dcebe15214c6baded2a7470d520e3)](https://app.codacy.com/gh/vb64/test.helper.yandex.alice.flask/dashboard?utm_source=gh&utm_medium=referral&utm_content=&utm_campaign=Badge_coverage)

Класс python для автоматического тестирования навыка Яндекс Алиса, реализованного на python/flask.
Пример [использования в юнит-тестах](https://github.com/vb64/test.helper.yandex.alice.flask/blob/master/tests/test_buy_elephant.py).

Установка:
```bash
pip install tester_alice_skill_flask
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
assert session.contain("Купи слона!")

# диалог содержит две кнопки
assert len(session.buttons) == 2

# нажать первую кнопку
session.send_button(0)

assert session.contain("Все говорят")

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

assert session.contain("Слона можно найти на Яндекс.Маркете!")
assert not session.contain("Все говорят")

```
