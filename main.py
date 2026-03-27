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

#Tabela Intermediária
inscricoes = Table(
    "inscricoes", #nome da tabela
    Base.metadata,
    Column("aluno_id", Integer, ForeignKey("alunos.id"), primary_key=True),
    Column("curso_id", Integer, ForeignKey("cursos.id"), primary_key=True),
)

# Tabelas curso e aluno
class Aluno(Base):
    __tablename__ = "alunos"

    #Como cria uma coluna
    id = Column(Integer, primary_key=True, autoincrement=True)
    nome = Column(String(100), nullable=False)


    #Relacionamento
    cursos = relationship("Curso", secondary=inscricoes, back_populates="alunos")



    #Função para imprimir
    def __repr__(self):
        return f"ID: {self.id} - NOME: {self.nome}"
    
class Curso(Base):
    __tablename__ = "cursos"

    #Como cria uma coluna
    id = Column(Integer, primary_key=True, autoincrement=True)
    nome = Column(String(100), nullable=False)

    #Relacionamento
    alunos = relationship("Aluno", secondary=inscricoes, back_populates="cursos")

    #Função para imprimir
    def __repr__(self):
        return f"ID: {self.id} - NOME: {self.nome}"
    

#Conexão com db
engine = create_engine("sqlite:///gestao_escolar.db")

Base.metadata.create_all(engine)

Session = sessionmaker(bind=engine)

#Criar
def cadastrar_curso():
    with Session() as session:
        try:
            #Criar o objeto cruso
            nome_curso = input("Digite o nome do curso: ").capitalize()
            curso = Curso(nome=nome_curso)
            #Adicionar no banco
            session.add(curso)
            #Salvar
            session.commit()
            print(f"Curso {nome_curso} cadastrado com sucesso!")
        except Exception as erro:
            session.rollback()
            print(f"Ocorreu um erro {erro}")

def cadastrar_aluno():
    with Session() as session:
        try:
            #Buscar o curso do aluno
            nome_curso = input("Digite o nome do curso para cadastrar o aluno: ").capitalize()
            curso = session.query(Curso).filter_by(nome=nome_curso).first()
            if curso == None:
                print(f"Nenhum curso encontrado com esse nome {nome_curso}")
                return
            else:
                nome_aluno = input("Digite o nome do aluno para cadastrar: ").capitalize()
                aluno = Aluno(nome=nome_aluno)
                aluno.cursos.append(curso)

                session.add(aluno)
                session.commit()
                print(f"Aluno cadastrado com sucesso!")
        except Exception as erro:
            session.rollback()
            print(f"Ocorreu um erro {erro}")


def adicionar_curso():
    with Session() as session:
        try:
            #Buscar o curso do aluno
            nome_curso = input("Digite o nome do curso para inserir o aluno: ").capitalize()
            curso = session.query(Curso).filter_by(nome=nome_curso).first()
            if curso == None:
                print(f"Nenhum curso encontrado com esse nome {nome_curso}")
                return
            else:
                nome_aluno = input("Digite o nome do aluno para cadastrar: ").capitalize()
                aluno = session.query(Aluno).filter_by(nome=nome_aluno).first()
                if aluno == None:
                    print(f"Nenhum aluno cadastro com esse nome {nome_aluno}")
                    return
                else:
                    aluno.cursos.append(curso)
                    session.commit()
                    print(f"Aluno registro com sucesso no curso {nome_curso}")
        except Exception as erro:
            session.rollback()
            print(f"Ocorreu um erro {erro}")

#Listar
def listar_cursos():
    with Session() as session:
        try:
            #Como pegar todos os registros da tabela?
            todos_cursos = session.query(Curso).all()
            for curso in todos_cursos:
                print(f"\n--- Curso {curso.nome} ---")
                for aluno in curso.alunos:
                    print(aluno.nome)
        except Exception as erro:
            session.rollback()
            print(f"Ocorreu um erro {erro}")
# listar_cursos()

def listar_alunos():
    with Session() as session:
        try:
            #Como pegar todos os registros da tabela?
            todos_alunos = session.query(Aluno).all()
            for aluno in todos_alunos:
                nomes_cursos = [curso.nome for curso in aluno.cursos]
                print(f"Nome: {aluno.nome} - Cursos: {nomes_cursos}")
        except Exception as erro:
            session.rollback()
            print(f"Ocorreu um erro {erro}")

# listar_alunos()

#Atualizar


def atualizar_curso():
    with Session() as session:
        try:
            nome_antigo = input("Digite o nome do curso que deseja alterar: ").capitalize()
            curso = session.query(Curso).filter_by(nome=nome_antigo).first()

            if curso:
                novo_nome = input(f"Digite o novo nome para o curso '{nome_antigo}': ").capitalize()
                curso.nome = novo_nome
                session.commit()
                print(f"Curso atualizado com sucesso de '{nome_antigo}' para '{novo_nome}'!")
            else:
                print(f"Curso '{nome_antigo}' não encontrado.")
        except Exception as erro:
            session.rollback()
            print(f"Ocorreu um erro ao atualizar o curso: {erro}")

# atualizar_curso()

def atualizar_aluno():
    with Session() as session:
        try:
            nome_antigo = input("Digite o nome do aluno que deseja alterar: ").capitalize()
            aluno = session.query(Aluno).filter_by(nome=nome_antigo).first()

            if aluno:
                novo_nome = input(f"Digite o novo nome para o aluno '{nome_antigo}': ").capitalize()
                aluno.nome = novo_nome
                session.commit()
                print(f"Nome do aluno atualizado com sucesso!")
            else:
                print(f"Aluno '{nome_antigo}' não encontrado.")
        except Exception as erro:
            session.rollback()
            print(f"Ocorreu um erro ao atualizar o aluno: {erro}")

# atualizar_aluno()

#Deletar

def deletar_curso():
    with Session() as session:
        try:
            nome_curso = input("Digite o nome do curso que deseja deletar: ").capitalize()
            curso = session.query(Curso).filter_by(nome=nome_curso).first()

            if curso:
                confirmar = input(f"Tem certeza que deseja deletar o curso '{nome_curso}'? (S/N): ").upper()
                if confirmar == 'S':
                    session.delete(curso)
                    session.commit()
                    print(f"Curso '{nome_curso}' deletado com sucesso!")
                else:
                    print("Operação cancelada.")
            else:
                print(f"Curso '{nome_curso}' não encontrado.")
        except Exception as erro:
            session.rollback()
            print(f"Ocorreu um erro ao deletar o curso: {erro}")

deletar_curso()

def deletar_aluno():
    with Session() as session:
        try:
            nome_aluno = input("Digite o nome do aluno que deseja deletar: ").capitalize()
            aluno = session.query(Aluno).filter_by(nome=nome_aluno).first()

            if aluno:
                confirmar = input(f"Tem certeza que deseja deletar o aluno '{nome_aluno}'? (S/N): ").upper()
                if confirmar == 'S':
                    session.delete(aluno)
                    session.commit()
                    print(f"Aluno '{nome_aluno}' deletado com sucesso!")
                else:
                    print("Operação cancelada.")
            else:
                print(f"Aluno '{nome_aluno}' não encontrado.")
        except Exception as erro:
            session.rollback()
            print(f"Ocorreu um erro ao deletar o aluno: {erro}")

deletar_aluno()