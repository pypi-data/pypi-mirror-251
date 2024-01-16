import os
class Settings(object):
    def __init__(self, _required_settings: str):
        required = self.required_settings(_required_settings)
        for name in required:
            split_name = name.split('.')
            type_settings = split_name[0]
            name_settings = split_name[1]

            if not type_settings in self.__dict__:
                self.__dict__[type_settings] = self.SubSettings()

            env = os.getenv(name)
            if env is None:
                raise Exception(f'Required environment variable [{name}] does not exist.')
            else:
                self.__dict__[type_settings].__dict__[name_settings] = env

    class SubSettings(object):
        def __init__(self):
            pass

    def __getattr__(self, name):
        if name not in self:
            raise KeyError(name)
        return self[name]

    def __delattr__(self, name):
        del self[name]

    def required_settings(self, string_present):
        required = [i.strip() for i in string_present.split(',')]
        return required
