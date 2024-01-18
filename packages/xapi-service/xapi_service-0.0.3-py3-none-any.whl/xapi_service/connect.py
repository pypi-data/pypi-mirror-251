from requests import post, get
from .servers import servers

class connect_xapi:
    def __init__(self, username_account, password_account):
        self.username_account = username_account
        self.password_account = password_account
    login = lambda self:post(servers.server("login"), data={'username': self.username_account, 'password': self.password_account}).json()
    view_webservice = lambda self:post(servers.server("view_webservice"), data={'username': self.username_account, 'password': self.password_account}).json()
    view = lambda self, username_webservice, type:get("https://web-service.x-api.ir/webservice/%s.%s"% (username_webservice, type)).text
    def create_webservice(self, username_webservice, password_webservice, type):
        if type == "json":
            type = "webservice-create"
        elif type == "html":
            type = "webservice-create-html"
        elif type == "css":
            type = "webservice-create-css"
        elif type == "txt":
            type = "webservice-create-txt"
        elif type == "log":
            type = "webservice-create-log"
        elif type == "md":
            type = "webservice-create-md"
        else:
            type = None
        return post(servers.server("webservice"), data={'username_account': self.username_account, 'password_account': self.password_account, 'username': username_webservice, 'password': password_webservice, 'method': type}).json()
    def edit_webservice(self, username_webservice, password_webservice, type, text):
        if type == "json":
            type = "webservice-edit"
        elif type == "html":
            type = "webservice-edit-html"
        elif type == "css":
            type = "webservice-edit-css"
        elif type == "txt":
            type = "webservice-edit-txt"
        elif type == "log":
            type = "webservice-edit-log"
        elif type == "md":
            type = "webservice-edit-md"
        else:
            type = None
        return post(servers.server("webservice"), data={'username_account': self.username_account, 'password_account': self.password_account, 'username': username_webservice, 'password': password_webservice, 'method': type, 'text': text}).json()
    def off_webservice(self, username_webservice, password_webservice, type):
        if type == "json":
            type = "webservice-off"
        elif type == "html":
            type = "webservice-off-html"
        elif type == "css":
            type = "webservice-off-css"
        elif type == "txt":
            type = "webservice-off-txt"
        elif type == "log":
            type = "webservice-off-log"
        elif type == "md":
            type = "webservice-off-md"
        else:
            type = None
        return post(servers.server("webservice"), data={'username_account': self.username_account, 'password_account': self.password_account, 'username': username_webservice, 'password': password_webservice, 'method': type}).json()
    def on_webservice(self, username_webservice, password_webservice, type):
        if type == "json":
            type = "webservice-on"
        elif type == "html":
            type = "webservice-on-html"
        elif type == "css":
            type = "webservice-on-css"
        elif type == "txt":
            type = "webservice-on-txt"
        elif type == "log":
            type = "webservice-on-log"
        elif type == "md":
            type = "webservice-on-md"
        else:
            type = None
        return post(servers.server("webservice"), data={'username_account': self.username_account, 'password_account': self.password_account, 'username': username_webservice, 'password': password_webservice, 'method': type}).json()
    def delete_webservice(self, username_webservice, password_webservice, type):
        if type == "json":
            type = "webservice-delete"
        elif type == "html":
            type = "webservice-delete-html"
        elif type == "css":
            type = "webservice-delete-css"
        elif type == "txt":
            type = "webservice-delete-txt"
        elif type == "log":
            type = "webservice-delete-log"
        elif type == "md":
            type = "webservice-delete-md"
        else:
            type = None
        return post(servers.server("webservice"), data={'username_account': self.username_account, 'password_account': self.password_account, 'username': username_webservice, 'password': password_webservice, 'method': type}).json()