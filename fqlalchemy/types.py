from sqlalchemy import String


class ID(String):
    def __init__(self, *args, **kwargs):
        kwargs['length'] = 256
        super(ID, self).__init__(*args, **kwargs)
