from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class Cases(db.Model):

    id_ = db.Column(db.String(), primary_key=True)
    employer_id = db.Column(db.Integer, db.ForeignKey('employers.id_'), nullable=False)
    nbr_immigrants = db.Column(db.Integer)
    job_code = db.Column(db.String(3), db.ForeignKey('job_codes.code'), nullable=False)
    begin_date = db.Column(db.DateTime)
    end_date = db.Column(db.DateTime)
    wage_rate = db.Column(db.Float)
    rate_per = db.Column(db.String())
    prevailing_wage = db.Column(db.Float)

    def __init__(self):
        pass

    def __rep__(self):
        return 'Case no: {}'.format(self.case_no)


class Employers(db.Model):

    id_ = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String())
    city = db.Column(db.String())
    state = db.Column(db.String(2))
    postal_code = db.Column(db.String())

    def __init__(self):
        pass

    def __rep__(self):
        return '{}'.format(self.name)


class JobCodes(db.Model):

    code = db.Column(db.String(), primary_key=True)
    title = db.Column(db.String())

    def __init__(self):
        pass

    def __rep__(self):
        return '{}: {}'.format(self.code, self.title)
