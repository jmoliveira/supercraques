# coding: utf-8
#!/usr/bin/env python

from torneira.controller import render_to_extension
from supercraques.controller import BaseController, logged, authenticated
from supercraques.model.usuario import Usuario
from supercraques.model.desafio import Desafio
from supercraques.core.facebook import GraphAPI


#https://ssl.facebook.com/login.php?api_key=131760776839225&amp;skip_api_login=1&amp;display=popup&amp;cancel_url=http%3A%2F%2Fapp.apigee.com%2Foauth2callback.jsp%3Fprovider%3Dfacebook&amp;fbconnect=1&amp;next=http%3A%2F%2Fwww.facebook.com%2Fconnect%2Fuiserver.php%3Fapp_id%3D131760776839225%26method%3Dpermissions.request%26display%3Dpopup%26next%3Dhttp%253A%252F%252Fapp.apigee.com%252Foauth2callback.jsp%253Fprovider%253Dfacebook%26type%3Duser_agent%26fbconnect%3D1%26perms%3Dpublish_stream%252Ccreate_event%252Crsvp_event%252Csms%252Coffline_access%252Cemail%252Cread_insights%252Cread_stream%252Cuser_about_me%252Cuser_activities%252Cuser_birthday%252Cuser_education_history%252Cuser_events%252Cuser_groups%252Cuser_hometown%252Cuser_interests%252Cuser_likes%252Cuser_location%252Cuser_notes%252Cuser_online_presence%252Cuser_photo_video_tags%252Cuser_photos%252Cuser_relationships%252Cuser_religion_politics%252Cuser_status%252Cuser_videos%252Cuser_website%252Cuser_work_history%252Cuser_checkins%252Cread_friendlists%252Cread_requests%252Cfriends_about_me%252Cfriends_activities%252Cfriends_birthday%252Cfriends_education_history%252Cfriends_events%252Cfriends_groups%252Cfriends_hometown%252Cfriends_interests%252Cfriends_likes%252Cfriends_location%252Cfriends_notes%252Cfriends_online_presence%252Cfriends_photo_video_tags%252Cfriends_photos%252Cfriends_relationships%252Cfriends_religion_politics%252Cfriends_status%252Cfriends_videos%252Cfriends_website%252Cfriends_work_history%252Cfriends_checkins%26from_login%3D1



class HomeController (BaseController):
  
    @logged 
    def home(self, usuario, *args, **kargs):
        desafios_recebidos = Desafio().get_desafios_recebidos(usuario.id)
        desafios_enviados = Desafio().get_desafios_enviados(usuario.id)
        return self.render_to_template("/home.html", usuario=usuario, desafios_recebidos=desafios_recebidos, desafios_enviados=desafios_enviados)

    @authenticated
    def auth_login(self, user_cookie, *args, **kargs):
        request_handler = kargs.get('request_handler')
        usuario = Usuario().get(user_cookie["uid"])
        if not usuario:
            graphAPI = GraphAPI(access_token=user_cookie["access_token"])
            user_facebook = graphAPI.request(user_cookie["uid"])
            Usuario().criar_usuario(user_facebook)
            return request_handler.redirect("/home")
        else:
            #TODO FAZER UPDATE DO DADOS DO USUARIO
            pass
        
        return request_handler.redirect("/home")

    def login(self, *args, **kargs):
        return self.render_to_template("/login.html")





















#        "equipes_na_edicao": "http://localhost:8001/futebol/campeonato/campeonato-brasileiro/brasileirao2010/equipes_no_campeonato.json",
#        "elenco_atual_da_equipe":"http://localhost:8001/futebol/time/%s/elenco/atual.json",
#        "scout_do_atleta_na_edicao":"http://localhost:8001/futebol/scout/campeonato-brasileiro/brasileirao2010/atleta/%s/eventos_atleta_por_edicaocampeonato_atleta.json",

#        # ordena os itens de acordo com o criterio escolhido
#        if orderby == 'pontos':
#            atletas.sort(key=lambda x:x['pontuacao'], reverse=True)
#        else:    
#            c = Collator("%s/allkeys.txt" % utils.__path__[0])
#            atletas.sort(key=lambda x:c.sort_key(x['apelido'].lower()))


#    def login(self, *args, **kargs):
#        
#        verification_code = self.request.get("code")
#        args = dict(client_id=FACEBOOK_APP_ID, redirect_uri=self.request.path_url)
#        
#        if verification_code:
#            args["client_secret"] = FACEBOOK_APP_SECRET
#            args["code"] = self.request.get("code")
#            response = cgi.parse_qs(urllib.urlopen(
#                "https://graph.facebook.com/oauth/access_token?" +
#                urllib.urlencode(args)).read())
#            access_token = response["access_token"][-1]
#
#            # Download the user profile and cache a local instance of the
#            # basic profile info
#            profile = json.load(urllib.urlopen(
#                "https://graph.facebook.com/me?" +
#                urllib.urlencode(dict(access_token=access_token))))
#            
#                
#            user = User(id=str(profile["id"]), name=profile["name"], 
#                        access_token=access_token, profile_url=profile["link"])
#            set_cookie(self.response, "fb_user", str(profile["id"]),
#                       expires=time.time() + 30 * 86400)
#            self.redirect("/")
#        else:
#            self.redirect(
#                "https://graph.facebook.com/oauth/authorize?" +
#                urllib.urlencode(args))
#        
#        
#        
#        return self.render_to_template("/login.html")
