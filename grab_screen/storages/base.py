class File(object):
    IMAGE = 'image'
    GIF = 'gif'
    VIDEO = 'video'

    def __init__(self, file_type, path):
        self.file_type = file_type
        self.path = path


class BaseStorage(object):

    def upload_image(self, path):
        raise NotImplementedError()
