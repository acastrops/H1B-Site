from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class TestTable(db.Model):
    __tablename__ = 'test_table'

    id_ = db.Column(db.Integer, primary_key=True)
    str_ = db.Column(db.String())

    def __init__(self, str_):
        self.str_ = str_

    def __rep__(self):
        return "<id {}>".format(self.id_)
