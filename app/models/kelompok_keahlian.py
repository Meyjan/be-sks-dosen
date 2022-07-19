from app import db

# Class Kelompok Keahlian
# Represents the kelompok keahlian of the lecturer
class KelompokKeahlian(db.Model):
    __tablename__ = "kelompok_keahlians"
    kode = db.Column(db.String(length=100), primary_key=True, nullable=False)
    kepanjangan = db.Column(db.String(length=256), nullable=False)

    # Identity function
    def __repr__(self):
        return '<Kelompok Keahlian {}>'.format(self.kode)
    
    # Dictionary function
    def as_dict(self):
       return {c.name: getattr(self, c.name) for c in self.__table__.columns}