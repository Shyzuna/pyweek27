from settings import settings


class Case(object):
    def __init__(self, center, diameter):
        """
        Init a resource
        :param position:
        :param size:
        :param category:
        """
        self._center = center
        self._diameter = diameter

    def __str__(self):
        return "{} - {} -> {} ({})".format(self._center, self._diameter)

    def getCenter(self):
        return self._center
