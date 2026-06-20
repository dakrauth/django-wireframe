import pathlib
from datetime import datetime


def make_stat_property(name, converter=None):
    def _stat(self):
        try:
            stat = self.stat()
        except FileNotFoundError:
            return None

        result = getattr(stat, name)
        return converter(result) if converter else result

    return property(_stat)


class Path(pathlib.Path):
    size = make_stat_property("st_size")
    mode = make_stat_property("st_mode")
    uid = make_stat_property("st_uid")
    gid = make_stat_property("st_gid")
    mtime = make_stat_property("st_mtime", datetime.fromtimestamp)
    ctime = make_stat_property("st_ctime", datetime.fromtimestamp)
    atime = make_stat_property("st_atime", datetime.fromtimestamp)
