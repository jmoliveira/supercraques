'''
    setting do projeto api console
'''
import logging, os


DEBUG = True
PROFILING = False


ROOT_URLS = "supercraques.urls"

DATABASE_ENGINE = "mysql://usr_cartola_r:usr_cartola_r@localhost/cartola?charset=utf8&use_unicode=0"
DATABASE_POOL_SIZE = 50

logging.basicConfig(
    level = getattr(logging, "DEBUG"),
    format = '%(asctime)s %(levelname)s %(message)s',
)
logging.getLogger('sqlalchemy').setLevel(logging.ERROR)

TEMPLATE_DIRS = "%s/templates" % os.path.abspath(os.path.dirname(__file__))
STATIC_DIR = "%s/static" % os.path.abspath(os.path.dirname(__file__))


SEDE = {
    "servicos":{
        "elenco_atual_da_equipe":"http://localhost:8001/futebol/time/%s/elenco/atual.json",
        "scout_do_atleta_na_edicao":"http://localhost:8001/futebol/scout/campeonato-brasileiro/brasileirao2010/atleta/%s/eventos_atleta_por_edicaocampeonato_atleta.json",
    }
}
