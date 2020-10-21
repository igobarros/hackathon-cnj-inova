import os

import sqlalchemy as db
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship


from config import connect_db # Abre conexão com o banco



Base = declarative_base()


# Precisamos melhorar a relação entre a tabelas
class Movimento(Base):
    
    __tablename__ = 'tb_movimento_tj'
    
    id = db.Column(db.BigInteger, db.Sequence('id_movimento_seq'), primary_key=True)
    codigoNacional = db.Column(db.Integer)
    dataHora = db.Column(db.DateTime())
    id_processo =  db.Column(db.Integer, db.ForeignKey('tb_processo_tj.id'))
    
    processo = relationship('Processo')
    
    
    def __repr__(self):
        return "<Movimento(codigoNacional='%s', dataHora='%s')>" % (self.codigoNacional, self.dataHora)
    
    
    
class Processo(Base):
    
    __tablename__ = 'tb_processo_tj'
    
    id = db.Column(db.BigInteger, db.Sequence('id_processo_seq'), primary_key=True)
    siglaTribunal = db.Column(db.String(100))
    grau = db.Column(db.String(100))
    numero = db.Column(db.String(100))
    dataAjuizamento = db.Column(db.DateTime())
    classeProcessual = db.Column(db.Integer)
    codigoOrgao = db.Column(db.Integer)
    codigoMunicipioIBGE = db.Column(db.Integer)
    instancia = db.Column(db.String(100))
    codigoLocalidade = db.Column(db.String(100))
    
    # movimento = relationship('Movimento')
    
    
    def __repr__(self):
        return "<Processo(siglaTribunal='%s', grau='%s', numero='%s', dataAjuizamento='%s', classeProcessual='%s', codigoOrgao='%s', codigoMunicipioIBGE='%s', instancia='%s', codigoLocalidade='%s')>" % (
            self.siglaTribunal,
            self.grau, 
            self.numero, 
            self.dataAjuizamento, 
            self.classeProcessual, 
            self.codigoOrgao, 
            self.codigoMunicipioIBGE, 
            self.instancia, 
            self.codigoLocalidade
        )
        
        



# Cria as tabelas no banco
engine = connect_db()
Processo.__table__.create(bind=engine, checkfirst=True)
Movimento.__table__.create(bind=engine, checkfirst=True)

