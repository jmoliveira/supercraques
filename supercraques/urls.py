from torneira.core.dispatcher import url
from supercraques.controller.banca import BancaController
from supercraques.controller.home import HomeController
from supercraques.controller.facebook import FacebookController
from supercraques.controller.desafio import DesafioController

urls = (
    url("/login", HomeController, action="login", name="login"),
    url("/auth/login", HomeController, action="auth_login", name="auth_login"),
    url("/home", HomeController, action="home", name="home"),
    url("/banca", BancaController, action="banca", name="banca"),
    url("/cards.{extension}", BancaController, action="cards", name="cards"),
    url("/cards", BancaController, action="cards_box", name="cards_box"),
    url("/fb/friends.{extension}", FacebookController, action="friends", name="friends"),
    url("/card/{card_id}/usuario_desafiado/{usuario_desafiado_id}/desafiar", DesafioController, action="enviar_desafio", name="enviar_desafio"),
    url("/atleta/{atleta_id}/comprar", BancaController, action="comprar_card", name="comprar_card"),
    url("/equipe/{equipe_id}/atletas.{extension}", BancaController, action="busca_atletas_por_equipe", name="busca_atletas_por_equipe"),
)