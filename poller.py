# Standard imports
import time

# Custom imports
import libtpb
import enqueue
import torrentdl
import settings


seconds = 1
minute = 60 * seconds
hour = 60 * minute
halfhour = 0.5 * hour

def poller():
    '''
    The poller wakes up every 30 minutes and does the following checks:
    - Are there any undownloaded episodes released in the past? If yes, it tries
      to find a torrent for that episode and downloads the torrent if it finds
      it feasible.
    - Are there any queued tv shows that have new announced episodes? If yes, it
      enqueues the new episodes.
    '''

if __name__ == '__main__':
    poller('example.db')
