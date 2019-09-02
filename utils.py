import yaml

def load_config(config_file):
    with open(config_file, 'r') as stream:
        try:
            return yaml.safe_load(stream)
        except yaml.YAMLError as exc:
            print(exc)

class subsDict(dict):
    def __setitem__(self, k, v):
        try:
            self.__getitem__(k)
            # TODO: change to log.error or rise.exception
            raise ValueError('Subscription {} already exists, please, unsubscribe before setting up new subscription', k)
            return False
        except KeyError:
            super().__setitem__(k, v)
