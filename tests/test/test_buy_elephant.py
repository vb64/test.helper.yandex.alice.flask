# coding: utf-8
"""Tests with buy-elephant.py module."""
import os
import sys
import unittest


class TestElephant(unittest.TestCase):
    """Module buy-elephant.py."""

    def test_app(self):
        """Test flask app."""
        from tests.buy_elephant import app
        from tester_alice_skill_flask import Interface, Skill

        skill = Skill(app, 'xxx-yyy-zzz', '/')
        assert skill

        session = skill.new_session('1234567890', [Interface.Screen])
        assert session.contain("Купи слона!")
        assert len(session.buttons) == 2

        session.send_button(0)
        assert session.contain("Все говорят")
        assert len(session.buttons) == 2

        session.send(
          "я завтра обдумаю этот вопрос на улице льва толстого, 16",
          nlu={
            "entities": [
              "я", "завтра", "обдумаю", "этот", "вопрос", "на", "улице", "льва", "толстого", "16"
            ],
            "tokens": [

              {
                "tokens": {"start": 2, "end": 6},
                "type": "YANDEX.GEO",
                "value": {
                  "house_number": "16",
                  "street": "льва толстого"
                }
              },

              {
                "tokens": {
                  "start": 3,
                  "end": 5
                },
                "type": "YANDEX.FIO",
                "value": {
                  "first_name": "лев",
                  "last_name": "толстой"
                }
              },

              {
                "tokens": {
                  "start": 5,
                  "end": 6
                },
                "type": "YANDEX.NUMBER",
                "value": 16
              },

              {
                "tokens": {
                  "start": 6,
                  "end": 8
                },
                "type": "YANDEX.DATETIME",
                "value": {
                  "day": 1,
                  "day_is_relative": True
                }
              }
            ]
          }
        )
        assert session.contain("Все говорят")
        print(session.dump())
        print(session.dump(tail=1))

        session.clear()
        session.send_button(1)
        assert session.contain("Слона можно найти на Яндекс.Маркете!")
        assert not session.contain("Все говорят")
        print(session.dump(tail=1))


if __name__ == '__main__':
    sys.path.insert(1, os.getcwd())
    unittest.main()
