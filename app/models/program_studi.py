from app import db

# Class Program Studi
# Represents the program studi of the lecturer
class ProgramStudi(db.Model):
    __tablename__ = "program_studis"
    kode = db.Column(db.String(length=100), primary_key=True, nullable=False)
    kepanjangan = db.Column(db.String(length=256), nullable=False)

    # Identity function
    def __repr__(self):
        return '<Program Studi {}>'.format(self.kode)
    
    # Dictionary function
    def as_dict(self):
       return {c.name: getattr(self, c.name) for c in self.__table__.columns}