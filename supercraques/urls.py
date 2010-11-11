from torneira.core.dispatcher import url
from supercraques.controller.atleta import AtletaController

urls = (
    url("/atletas", AtletaController, action="atletas", name="atletas"),
)