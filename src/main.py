from fastapi import FastAPI
from sqlmodel import SQLModel, create_engine, Field, Session, select
from fastapi.responses import JSONResponse
from typing import Optional
from datetime import datetime
from http import HTTPStatus

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


@app.patch("/manutencoes/{id}/finalizar")
def finalizar_manutencao(id: int):
    with Session(engine) as session:
        statement = select(Manutencao).where(Manutencao.id == id)
        manutencao = session.exec(statement=statement).first()
        if manutencao.dataSaida:
            return JSONResponse(content={"message": "manutenção ja finalizada"},
                                status_code=HTTPStatus.BAD_REQUEST)
        manutencao.dataSaida = str(datetime.now())
        session.commit()
        session.refresh(manutencao)
        return manutencao
    


@app.delete("/manutencoes/{id}")
def deletar_manutencao(id: int):
    with Session(engine) as session:
        statement = select(Manutencao).where(Manutencao.id == id)
        manutencao = session.exec(statement=statement).first()
        # print(manutencao)
        # if not manutencao:
        #     return JSONResponse(
        #         content={"message": "manutenção nao encontrada"},
        #         status_code=HTTPStatus.NOT_FOUND,
        #     )
        # if manutencao.dataSaida:
        #     return JSONResponse(
        #         content={"message": "manutenção já foi finalizada"},
        #         status_code=HTTPStatus.BAD_REQUEST,
        #     )
        session.delete(manutencao)
        session.commit()  
        return JSONResponse(content=None,
                            status_code=HTTPStatus.NO_CONTENT)
  
    