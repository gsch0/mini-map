import argparse
import socket
import concurrent.futures

def scan_port_service(target, port):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.settimeout(0.5)  # Timeout pour chaque connexion
    try:
        result = sock.connect_ex((target, port))  # 0 = ouvert, sinon fermé
        if result == 0:
            try:
                banner = sock.recv(4096).decode("utf-8", errors="ignore").strip()

                return (port, f"OPEN: {banner}")
            except socket.timeout:
                return (port, "OPEN - UNKNOWN")
            except Exception as e:
                return (port, f"ERROR: {str(e)}")
        else:
            return (port, "CLOSED")
    except socket.error as e:
        return (port, f"ERROR: {e}")
    finally:
        sock.close()

def scan_ports(target, ports,nbreThread):
    
    try:
        target_ip = socket.gethostbyname(target)  # Résoudre l'IP depuis le nom d'hôte
        print(f"Scanning target: {target_ip}")
    except socket.gaierror:
        print("ERROR: Invalid target")
        return

    ports_to_scan = range(ports[0], ports[1] + 1)

    with concurrent.futures.ThreadPoolExecutor(max_workers=nbreThread) as executor:  # Nombre de threads
        results = executor.map(lambda port: scan_port_service(target_ip, port), ports_to_scan)
        
        # Afficher les résultats
        for port, banner in results:
            if banner != "CLOSED":
                print(f"[Port {port}] : {banner}")

def main():
    parser = argparse.ArgumentParser(description="Mini port scanner")
    parser.add_argument("target", type=str, help="Target ip")
    parser.add_argument("-p", "--ports", type=int, nargs=2, default=[0, 100], help="Ports to scan (start_port,end_port)")
    parser.add_argument("-t", "--thread", type=int, default=20, help="number of Tread")
    args = parser.parse_args()

    print(f"Scanning {args.target} from port {args.ports[0]} to {args.ports[1]}")
    scan_ports(args.target, args.ports,args.thread)

if __name__ == "__main__":
    main()
