import argparse
import socket
import concurrent.futures
from datetime import datetime



def scan_port_service(target, port):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.settimeout(1)  
    try:
        result = sock.connect_ex((target, port)) 
        if result == 0:
            try:
                banner = ""
                
                sock.send(f"HEAD / HTTP/1.1\r\nHost: {target}\r\n\r\n".encode("utf-8"))
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


def scan_ports(target, ports,nbreThread,output):
    
    try:
        target_ip = socket.gethostbyname(target)  
        print(f"Scanning target: {target_ip}")
        with open(output, mode="a") as file:
            file.write(f"Scanning {target} : {target_ip} from port {ports[0]} to {ports[1]}\n")
    except socket.gaierror:
        print("ERROR: Invalid target")
        with open(output, mode="a") as file:
            file.write(f"Scanning {target} from port {ports[0]} to {ports[1]}\n")
        return
    
    

    ports_to_scan = range(ports[0], ports[1] + 1)

    with concurrent.futures.ThreadPoolExecutor(max_workers=nbreThread) as executor:  
        results = executor.map(lambda port: scan_port_service(target_ip, port), ports_to_scan)
        
        with open(output, mode="a") as file:
            for port, banner in results:
                if banner != "CLOSED":
                    print(f"[Port {port}] : {banner}")
                    file.write(f"[Port {port}] : {banner}\n")

def main():
    parser = argparse.ArgumentParser(description="Mini port scanner")
    parser.add_argument("target", type=str, help="Target ip")
    parser.add_argument("-p", "--ports", type=int, nargs=2, default=[0, 100], help="Ports to scan (start_port,end_port)")
    parser.add_argument("-t", "--thread", type=int, default=20, help="number of Tread")
    parser.add_argument("-o", "--output", type=str, default=f"mini_map_{datetime.now().strftime("%Y_%m_%d_%H_%M_%S")}.txt", help="output file")
    args = parser.parse_args()

    print(f"Scanning {args.target} from port {args.ports[0]} to {args.ports[1]}")
    

    scan_ports(args.target, args.ports,args.thread,args.output)

if __name__ == "__main__":
    main()
