# nameserver.py
import argparse
from Pyro4.naming import startNSloop
from Config import config

def main():
    parser = argparse.ArgumentParser(description="Arranca un Pyro4 Name Server en host y puerto especificados")
    parser.add_argument('-n', '--host', default=config.HOSTNAME,
                        help='Host o IP donde escuchará el Name Server')
    parser.add_argument('-p', '--port', type=int, default=config.NAMESERVER_PORT,
                        help='Puerto donde escuchará el Name Server')
    parser.add_argument('--no-broadcast', dest='enableBroadcast', action='store_false',
                        help='Desactivar el broadcast de UDP (útil en redes cerradas)')
    args = parser.parse_args()
    
    print(f"Arrancando Pyro4 Name Server en {args.host}:{args.port} "
          f"(broadcast={'ON' if args.enableBroadcast else 'OFF'})")
    startNSloop(host=args.host, port=args.port, enableBroadcast=args.enableBroadcast)

if __name__ == "__main__":
    main()
