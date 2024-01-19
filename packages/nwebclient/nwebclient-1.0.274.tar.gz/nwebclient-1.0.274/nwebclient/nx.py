"""
  High Level Computer functions

  npy
"""


import socket
from nwebclient import util


def get_ip():
    return socket.gethostbyname(socket.gethostname())

def udp_send(data, ip='255.255.255.255', port=4242):
    sock = socket.socket(socket.AF_INET,  socket.SOCK_DGRAM,  socket.IPPROTO_UDP)  # UDP
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
    sock.sendto(data.encode('ascii'), (ip, port))

def help():
    print('Usage: ')
    print('  npy send_ip')
    print('  npy ip')
    print('')
    print('Tipps:')
    print('  Cron-Job')
    print('    */10  * * * * npy send_ip')

def main():
    args = util.Args()
    if args.help_requested():
        return help()
    if args.hasShortFlag('send_ip') or args.hasName('send_ip'):
        udp_send('nxudp npy' + str(get_ip()) + " from-npy")
    elif args.hasShortFlag('ip') or args.hasName('ip'):
        print(get_ip())
    else:
        print("Error: Unknown command")
        print("")
        help()


if __name__ == '__main__':
    main()
