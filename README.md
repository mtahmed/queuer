UPDATE: Use popcorntime instead (for legal downloads/free tv shows only).

# queuer

Makes it super easy to set up recurring torrent downloads.

## Installation

Clone the repository to wherever is convenient (e.g. `~/bin/queuer`):

```bash
cd ~/bin/
git clone --recursive https://github.com/mtahmed/queuer.git
```

Edit `settings.py` appropriately. For most users, the settings are just fine.

## Usage

Run the aria2 server with rpc enabled:

```bash
aria2c --enable-rpc --rpc-listen-all
```

#### Add a TV Show

To add new tv shows to track, run `queue.py --enqueue` and follow instructions.
To download a TV show called "some random tvshow", and enqueue all future episodes:

```bash
python queue.py --enqueue
Enter tv show name: some random tvshow
Enter other keywords to search for torrents (e.g. 720p eztv): 720p [publichd]
Found 2 tv show(s)!

 1: Some Random TVShow (Oct/1/2010)
    Seasons: 4
    Airs 21:00 every Sunday
    http://www.tvrage.com/Some_Random

 2: Another Random TVShow (Jan/01/2006)
    Seasons: 1
    Airs 20:00 every Wednesday
    http://www.tvrage.com/shows/id-9999

Enter tv show number: 1
Found 40 episode(s)!

Which episodes to enqueue?
[[a(ll), f(uture), l(ist)]]: f
```

#### Remove a TV Show

To remove an enqueued tv show, run `queue.py --dequeue` and select the tv show
to remove.
```bash
python queue.py --dequeue

 1: Some Random TVShow (Oct/1/2010)

 2: Another Random TVShow (Jan/1/2006)
Which tvshows to dequeue?
[[space-separated list]]: 1

Removed 1 tvshow(s)!
```

#### Run poller

Run `poller.py`. It will keep scanning the database to look for new announced
episodes and download released torrents for released episodes.
```bash
python poller.py
```

## Dependencies

- python3.x
- [kat](https://github.com/stephan-mclean/KickassTorrentsAPI): A library to interface with KickAssTorrents.
- [Beautiful Soup 4](http://www.crummy.com/software/BeautifulSoup/bs4/doc/): Python
  library for pulling data out of HTML/XML files. Used by tvshows.py and libtpb
  for parsing the data from tvrage.com and thepiratebay.org.
- [aria2](http://aria2.sourceforge.net/): For now, only the aria2 downloader is
  supported. You may submit patches to support additional downloaders. Will only
  need to add a new downloader in torrentdl.py and make changes to how it's used etc.

## Notes

- The episodes will download to the default download directory in aria2.
- Simultaneous downloads limits, upload speeds, download speeds, continuing
  downloads etc. is all taken care of by the downloader.
