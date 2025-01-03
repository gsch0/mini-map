import argparse
import socket
def scan_port(target,ports):
    print("tes")
    try:
        target = socket.gethostbyname(target)
    except socket.gaierror:
        print("Erreur : Hôte invalide pas de résolutino")
        return

    for port in range(ports[0],ports[1]+1):
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(0.5)  # Timeout pour chaque connexion
        result = sock.connect_ex((target, port))  # 0 = ouvert, sinon fermé
        if result == 0:
            print(f"Port {port}: OUVERT")
        sock.close()

def main():
    parser = argparse.ArgumentParser(description="mini ports scanner")
    parser.add_argument("target", type=str, help="Adresse IP à analysez")
    parser.add_argument("-p", "--ports", type=int, nargs="+", default=[0, 100],help="Liste des ports à analyser ")
    args = parser.parse_args()
    print(args.target,args.ports)
    scan_port(args.target,args.ports)


    
main()