class App:
    base = None
    @classmethod
    def set_base(cls, app_instance):
        cls.base = app_instance
    @classmethod
    def get_app(cls):
        return cls.base
