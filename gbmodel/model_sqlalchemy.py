import sys
#sys.path.append('/Users/faisa/Desktop/Code/capstone_repo/capstone360')
from app import db, engine
import datetime

class teams(db.Model):
    __table__ = db.Model.metadata.tables['teams']
"""
    def __repr__(self):
        return self.DISTRICT
        """

class students(db.Model):
    __table__ = db.Model.metadata.tables['students']
"""
    def __repr__(self):
        return self.DISTRICT

"""
class capstone_session(db.Model):
    __table__ = db.Model.metadata.tables['capstone_session']


class removed_students(db.Model):
    __table__ = db.Model.metadata.tables['removed_students']

"""
def __repr__(self):
    return self.DISTRICT
"""