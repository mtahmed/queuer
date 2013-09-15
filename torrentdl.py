# Standard imports
import xmlrpc.client


def download_torrent(torrent):
    '''
    Torrent is a dict as produced by the thepiratebay search_torrents function.

    This function uses xmlrpc to communicate with aria2 client. At the moment,
    only aria2 is supported.

    If you want it to work with other clients, please feel free to contribute
    patches.
    '''

    while True:
        try:
            s = xmlrpc.client.ServerProxy('http://localhost:6800/rpc')
            _ = s.aria2.getVersion()
            gid = s.aria2.addUri([torrent['magnet']])
            print("Added download with gid: %s" % gid)

            break
        except ConnectionRefusedError:
            print("Failed to connect to aria2 rpc server. Retrying ...")

    return
