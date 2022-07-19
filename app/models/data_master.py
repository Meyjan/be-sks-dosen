from app import db
from app.models.kelompok_keahlian import KelompokKeahlian

# Class DataMaster
# Represents the master data for list of dosen
class DataMaster(db.Model):
    __tablename__ = "data_masters"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True, nullable=False)
    kode_dosen = db.Column(db.String(length=100), nullable=False, default="")
    kelompok_keahlian = db.Column(db.String(length=100), db.ForeignKey(KelompokKeahlian.kode), nullable=False)

    uc_args_1 = db.UniqueConstraint(kode_dosen)
    __tableargs__ = (uc_args_1)

    # Identity function
    def __repr__(self):
        return '<DataMaster {}>'.format(self.id)
    
    # Dictionary function
    def as_dict(self):
       return {c.name: getattr(self, c.name) for c in self.__table__.columns}