from spyne import Application


class SonosApplication(Application):
    def __init__(self, *args, **kwargs):
        self.service_proxy = kwargs["service_proxy"]
        new_kwargs = {k: v for k, v in kwargs.items() if k not in ["service_proxy"]}
        Application.__init__(self, *args, **new_kwargs)

    def get_service_proxy(self):
        return self.service_proxy
