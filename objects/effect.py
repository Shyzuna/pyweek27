
class Effect(object):
    def __init__(self, name, duration, effectType, ratioPerStat={}, singleApplication=True, target=None, direct=False):
        self._name = name
        self._duration = duration
        self._effectType = effectType
        self._ratioPerStat = ratioPerStat
        self._singleApplication = singleApplication
        self._applied = False
        self._target = target

        if direct:
            self.apply()
            self._duration += 1

    def apply(self):
        self._duration -= 1
        if self._duration <= 0:
            self.remove()
            return

        if self._applied and self._singleApplication:
            return
        self._applied = True
        # Apply

    def remove(self):
        # Remove
        pass