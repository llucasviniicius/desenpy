from typing import Literal
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field

app = FastAPI(
    title="Calculadora API",
    description=(
        "API simples que recebe dois números e uma operação "
        "(soma, subtracao, multiplicacao, divisao) e retorna o resultado em JSON."
    ),
)

Operacao = Literal[
    "soma",
    "subtracao",
    "subtração",
    "multiplicacao",
    "divisao",
    "divisão",
]

class DadosEntrada(BaseModel):
    a: float = Field(..., example=10)
    b: float = Field(..., example=5)
    operacao: Operacao = Field(
        ..., example="soma",
        description="Operação a ser realizada: soma, subtracao/subtração, multiplicacao ou divisao/divisão"
    )
    
class ResultadoSaida(BaseModel):
    a: float
    b: float
    operacao: str
    resultado: float

@app.post(
    "/calcular",
    response_model=ResultadoSaida,
    summary="Executa cálculo entre dois números",
    description=(
        "Recebe dois números e o tipo de operação para retornar o resultado em JSON."
    ),
)
async def calcular(dados: DadosEntrada) -> ResultadoSaida:
    op = dados.operacao.lower()

    if op == "soma":
        resultado = dados.a + dados.b
    elif op in ("subtracao", "subtração"):
        resultado = dados.a - dados.b
    elif op == "multiplicacao":
        resultado = dados.a * dados.b
    elif op in ("divisao", "divisão"):
        if dados.b == 0:
            raise HTTPException(status_code=400, detail="Não existe divisão por zero")
        resultado = dados.a / dados.b
    else:
        raise HTTPException(
            status_code=400,
            detail=(
                "Operação inválida. Use soma, subtracao/subtração, "
                "multiplicacao ou divisao/divisão"
            ),
        )
    return ResultadoSaida(
        a=dados.a,
        b=dados.b,
        operacao=op,
        resultado=resultado,
    )
