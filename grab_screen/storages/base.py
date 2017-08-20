class File(object):
    IMAGE = 'image'
    GIF = 'gif'
    VIDEO = 'video'

    def __init__(self, file_type, path):
        self.file_type = file_type
        self.path = path


class BaseStorage(object):
    """Base class for storages."""

    def save_image(self, image):
        """
        Saves an image.

        :param image: `Image` tuple with image data.
        :return: `File` object.
        """
        raise NotImplementedError()
