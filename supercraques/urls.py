from torneira.core.dispatcher import url
from supercraques.controller.banca import BancaController
from supercraques.controller.home import HomeController

urls = (
    url("/login", HomeController, action="login", name="login"),
    url("/auth/login", HomeController, action="auth_login", name="auth_login"),
    url("/home", HomeController, action="home", name="home"),
    url("/banca", BancaController, action="banca", name="banca"),
    url("/atleta/{atleta_id}/comprar", BancaController, action="comprar_card", name="comprar_card"),
    url("/equipe/{equipe_id}/atletas.{extension}", BancaController, action="busca_atletas_por_equipe", name="busca_atletas_por_equipe"),
)