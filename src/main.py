from fastapi import FastAPI
from sqlmodel import SQLModel, create_engine, Field, Session  # pylint: disable=import-error
from typing import Optional

class Manutencao(SQLModel, table=True):
    id: int = Field(default=None, primary_key=True)
    placa: str 
    marca: str
    modelo: str 
    cor: str
    nomeCliente: str 
    nomeMecanico: str 
    dataChegada: str 
    dataSaida: Optional[str] = Field(default=None)

sqliteFileName = 'database.db'
sqliteUrl = f'sqlite:///{sqliteFileName}'

connect_args = {"check_same_thread": False}
engine = create_engine(sqliteUrl, echo=True, connect_args=connect_args) 

def create_db_and_table():
    SQLModel.metadata.create_all(engine)


app = FastAPI()

@app.on_event("startup")
def on_startup():
    create_db_and_table()

@app.get("/")
def root():
    return {"message": "ok"}


@app.post("/manutencoes")
def cria_registro(manutencao: Manutencao):
    with Session(engine) as session:
        session.add(manutencao)
        session.commit()
        session.refresh(manutencao)
        return manutencao
