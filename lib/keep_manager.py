import gkeepapi
import keyring
import json

from gkeepapi.node import List, Note
from collections import namedtuple


class KeepManager:

    keyring_key = 'google-keep-token'
    app_password_link = 'https://myaccount.google.com/apppasswords'
    temporary_login_link = 'https://accounts.google.com/b/0/DisplayUnlockCaptcha'

    def __init__(self, email, password=None):
        self.my_data = None
        self.email = email
        self.password = password
        self.keep = gkeepapi.Keep()

    def load_data(self):
        if self.login():
            data = self.keep.dump()
            self.my_data = {
                'notes': self.get_notes(self.keep._nodes),
                'lists': self.get_lists(self.keep._nodes),
                'keep_version': data['keep_version']
            }

    def get_data(self):
        self.load_data()
        return self.json2obj(json.dumps(self.my_data))

    def login(self):
        login_status = False
        try:
            master_token = keyring.get_password(KeepManager.keyring_key, self.email)
        except Exception as exception:
            print(exception)
            master_token = None
        if master_token is None:
            try:
                login_status = self.keep.login(self.email, self.password)
            except Exception as exception:
                print(exception)
        else:
            try:
                login_status = self.keep.resume(self.email, master_token)
            except Exception as exception:
                print(exception)

        try:
            if login_status:
                keyring.set_password(KeepManager.keyring_key, self.email, self.keep.getMasterToken())
        except Exception as exception:
            print(exception)

        return login_status

    def get_notes(self, nodes):
        notes = []
        for node in nodes['root'].children:
            if isinstance(node, Note):
                my_note = {'title': node.title, 'text': node.text, 'archived': node.archived}
                labels = [label._name for label in node.labels._labels.values()]
                if labels:
                    my_note['labels'] = labels
                notes.append(my_note)
        return notes

    def get_lists(self, nodes):
        lists = []
        for node in nodes['root'].children:
            if isinstance(node, List):
                my_list = {'title': node.title, 'items': [],
                           'labels': [label._name for label in node.labels._labels.values()], 'archived': node.archived}
                for item in node.children:
                    my_item = {'text': item.text, 'checked': item.checked}
                    my_list['items'].append(my_item)
                lists.append(my_list)
        return lists

    @staticmethod
    def _json_object_hook(d):
        return namedtuple('node', d.keys())(*d.values())

    @staticmethod
    def json2obj(data):
        return json.loads(data, object_hook=KeepManager._json_object_hook)


def main():
    keep = KeepManager('lightrescuer')
    print(keep.get_data())


if __name__ == '__main__':
    main()
