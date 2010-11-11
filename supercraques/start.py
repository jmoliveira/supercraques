import os, sys, getopt
import settings

def usage():
    print "\nServer Super Craques:"
    print "usage: start.py [--port=PORT] [-d (run as daemon)] [--help] COMMAND"
    print "\nOs comandos podem ser:"
    print "     start       incia o server como daemon"
    print "     stop        para um server que esteja rodando"
    print "     restart     reinicia um server que esteja rodando"
    print "     help        mostra esse help\n"

def main():

    try:
        optlists, command = getopt.getopt(sys.argv[1:], "dhpe", ["help", "port=", "daemon"])
    except getopt.GetoptError, err:
        print str(err) # will print something like "option -a not recognized"
        usage()
        sys.exit(2)

    port = 8082
    asDaemon = False
    
    for opt, value in optlists:
        if opt in ("-h", "--help"):
            usage()
            sys.exit()
        elif opt in ("-p", "--port"):
            port = int(value) if value else None
        elif opt in ("-d", "--daemon"):
            asDaemon = True
            
    pidfile = "/opt/logs/supercraques-%s.pid" % port
    
    project_root = os.path.abspath(os.path.dirname(__file__))
    sys.path.insert(0, os.path.abspath("%s/.." % project_root))
    
    from torneira.core.server import TorneiraServer
    server = TorneiraServer(pidfile=pidfile, port=port, project_root=project_root, media_dir=settings.STATIC_DIR)
    if asDaemon:
        if not command or command[0] not in ["start","stop","restart"]:
            usage()
            sys.exit()

        if command[0] == "start":
            server.start()

        elif command[0] == "stop":
            server.stop()

        elif command[0] == "restart":
            server.restart()
    else:
        server.run()

if __name__ == "__main__":
    main()
