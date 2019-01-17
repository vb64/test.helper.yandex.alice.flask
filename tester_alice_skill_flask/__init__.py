"""
Helper for Yandex.Alice skill autotests
"""
import sys
import json

if sys.version_info < (3, 0):
    reload(sys)  # noqa: F821 pylint: disable=undefined-variable
    sys.setdefaultencoding('utf-8')  # pylint: disable=no-member


class Surface:
    """
    Available Alice surfaces
    """
    Windows = 1
    MobileAndBrowser = 2
    Navigator = 3
    Station = 4


class Interface:
    """
    Available Alice interfaces
    """
    Screen = "screen"


class Skill:
    """
    Approved Alice skill as flask app
    """
    sessions = {"current_id": 10000}

    def __init__(self, flask_app, skill_id, webhook_url, is_screen_need=False):
        self.app = flask_app
        self.app.config['TESTING'] = True
        self.client = self.app.test_client()

        self.skill_id = skill_id
        self.url = webhook_url
        self.is_screen_need = is_screen_need

    def new_session(
      self,
      user_id,
      interfaces,
      locale='ru-RU',
      timezone="Europe/Moscow",
      client_id="ru.yandex.searchplugin/5.80 (Samsung Galaxy; Android 4.4)",
      command=""
    ):
        """
        create new Alice session
        """
        return Session(self, user_id, interfaces, locale, timezone, client_id, command)


class Session:
    """
    Approved Alice skill
    """
    def __init__(self, skill, user_id, interfaces, locale, timezone, client_id, command=""):
        self.skill = skill
        self.messages = {}
        self.buttons = []

        self.version = "1.0"
        self.meta = {
          "locale": locale,
          "timezone": timezone,
          "client_id": client_id,
          "interfaces": {interface: {} for interface in interfaces}
        }
        self.session = {
          "new": True,
          "message_id": 0,
          "session_id": "2eac4854-fce721f3-b845abba-{}".format(self.skill.sessions["current_id"]),
          "skill_id": self.skill.skill_id,
          "user_id": user_id
        }

        self.send(command, command=command)

        self.session["new"] = False
        self.skill.sessions["current_id"] += 1

    def send_button(self, index):
        """
        Alice user press button in the skill chat
        """
        button = self.buttons[index]
        req = {
          "nlu": {"entities": [], "tokens": []},
          "type": "SimpleUtterance",
          "original_utterance": button["title"],
        }

        if "payload" in button:
            req["payload"] = button["payload"]
            req["type"] = "ButtonPressed"

        self.send_request(req, "[{}]".format(button["title"]))

    def send(self, text, command="", nlu=None):
        """
        Alice user send text to skill
        """
        if not nlu:
            nlu = {"entities": [], "tokens": []}

        req = {
          "command": command,
          "nlu": nlu,
          "type": "SimpleUtterance",
          "original_utterance": text,
        }
        self.send_request(req, text)

    def send_request(self, req, text, follow=True):
        """
        internal send function
        """
        data = json.dumps({
          "meta": self.meta,
          "version": self.version,
          "session": self.session,
          "request": req,
        })

        response = self.skill.client.post(
          self.skill.url,
          data=data,
          follow_redirects=follow,
          content_type='application/json'
        )
        assert response.status_code == 200
        resp = json.loads(response.data)

        if 'buttons' in resp['response']:
            self.buttons = resp['response']['buttons']
        else:
            self.buttons = [button for button in self.buttons if not button.get('hide', False)]

        self.messages[self.session["message_id"]] = (text, resp['response']['text'])
        self.session["message_id"] += 1

    def clear(self):
        """
        Clear the chat history
        """
        self.messages = {}

    def dump(self, tail=5):
        """
        Print tail of the session history, order by message dates
        """
        suff = ''
        if len(self.messages) > tail:
            suff = 'Latest {}\n\n'.format(tail)

        lines = [suff]
        for message_id in sorted(self.messages)[-tail:]:
            req, res = self.messages[message_id]
            lines.append("Q: {}\nA: {}\n\n".format(req, res))

        if self.buttons:
            lines.append('\n\n' + ' '.join(["[{}]".format(but["title"]) for but in self.buttons]))

        return ''.join(lines)

    def contain(self, substring, tail=5):
        """
        Check for presence of the substring in tail of chat history
        """
        for message_id in sorted(self.messages)[-tail:]:
            req, res = self.messages[message_id]
            if (substring in req) or (substring in res):
                return True

        return False
