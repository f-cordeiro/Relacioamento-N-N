# Relacionamentos Muitos para Muitos (N:N)

# Estudantes se inscrevem em cursos.
# Um estudante pode fazer vários cursos.
# um curso pode ter vários estudantes

# Forma simples:
# A relação não precisa guardar dados extres
# So fazer o relacionamento

from sqlalchemy import create_engine, Column, Integer, Integer, String, ForeignKey, Table
from sqlalchemy.orm import declarative_base, sessionmaker, relationship

Base = declarative_base()


# Tabelas curso e aluno
class Aluno(Base):
    __tablename__ = "alunos"

    #Como cria uma coluna
    id = Column(Integer, primary_key=True, autoincrement=True)
    nome = Column(String(100), nullable=False)

    #Função para imprimir
    def __repr__(self):
        return f"ID: {self.id} - NOME: {self.nome}"
    
class Curso(Base):
    __tablename__ = "cursos"

    #Como cria uma coluna
    id = Column(Integer, primary_key=True, autoincrement=True)
    nome = Column(String(100), nullable=False)

    #Função para imprimir
    def __repr__(self):
        return f"ID: {self.id} - NOME: {self.nome}"
    
#Tabela Intermediária
inscricoes = Table(
    "inscricoes", #nome da tabela
    Base.metadata,
    Column("aluno_id", Integer, ForeignKey("alunos.id"), primary_key=True),
    Column("curso_id", Integer, ForeignKey("cursos.id"), primary_key=True),
)

#Conexão com db
engine = create_engine("sqlite:///gestao_escolar.db")

Base.metadata.create_all(engine)

Session = sessionmaker(bind=engine)

