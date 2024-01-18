class ProcessData:
    def __init__(self, _id, time, value):
        self.id = _id
        self.time = time
        self.value = value


# noinspection SpellCheckingInspection
class IndexData:

    def __init__(self, _id, datatype, time, value, properties):
        self.id = _id
        self.datatype = datatype
        self.time = time
        self.value = value
        self.properties = properties
