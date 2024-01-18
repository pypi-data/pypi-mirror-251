class servers:
    def server(server):
        host = "https://web-service.x-api.ir"
        if server == "login":
           server = "%s/login.php"% host
        elif server == "webservice":
            server = "%s/service.php"% host
        elif server == "view_webservice":
            server = "%s/view-web.php"% host
        else:
            server = "Server not found"
        return server