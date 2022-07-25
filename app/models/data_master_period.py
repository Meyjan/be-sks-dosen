from app import db
from app.models.data_master import DataMaster
from app.models.program_studi import ProgramStudi

# Class DataMasterPeriod represents data master during a certain period
class DataMasterPeriod(db.Model):
    __tablename__ = "data_master_periods"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True, nullable=False)
    id_data_master = db.Column(db.Integer, db.ForeignKey(DataMaster.id), nullable=False)
    semester = db.Column(db.Integer, nullable=False)
    year = db.Column(db.Integer, nullable=False)
    jfa = db.Column(db.String(length=256), nullable=False)
    status_kepegawaian = db.Column(db.String(length=256), nullable=False)
    tingkatan = db.Column(db.String(length=100), nullable=False)
    program_studi = db.Column(db.String(length=100), db.ForeignKey(ProgramStudi.kode), nullable=False)
    sertifikasi = db.Column(db.Boolean, nullable=False)
    dik_diakui = db.Column(db.Integer, nullable=False, default=0)
    lit_diakui = db.Column(db.Integer, nullable=False, default=0)
    abdimas_diakui = db.Column(db.Integer, nullable=False, default=0)
    penunjang = db.Column(db.Integer, nullable=False, default=0)
    cluster = db.Column(db.Integer)

    uc_args_1 = db.UniqueConstraint(id_data_master, semester, year)
    __tableargs__ = (uc_args_1)

    # Identity function
    def __repr__(self):
        return '<DataMasterPeriod {} at year {}>'.format(self.id_data_master, self.year)
    
    # Dictionary function
    def as_dict(self):
       return {c.name: getattr(self, c.name) for c in self.__table__.columns}