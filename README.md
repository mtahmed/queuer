# queuer

Makes it super easy to set up recurring downloads from [thepiratebay](http://thepiratebay.sx).

## Installation

Clone the repository to wherever is convenient (e.g. `~/bin/queuer`):

```bash
cd ~/bin/
hg clone https://mtahmed@bitbucket.org/mtahmed/queuer
# OR
git clone https://github.com/mtahmed/queuer.git
```

Then clone libtpb:

```bash
cd ~/bin/queuer
hg clone https://mtahmed@bitbucket.org/mtahmed/libtpb
# OR
git clone https://github.com/mtahmed/libtpb.git
```

Edit `settings.py` appropriately. For most users, the settings are just fine.

## Usage

Run the aria2 server with rpc enabled:

```bash
aria2c --enable-rpc --rpc-listen-all
```

To add new tv shows to track, run the enqueue.py and follow instructions.
To download a TV show called "some random tvshow", and enqueue all futuer episodes:

```bash
python enqueue.py
Enter tv show name: some random tvshow
Enter other keywords to search for torrents (e.g. 720p eztv): 720p [publichd]
Found 20 tv show(s)!

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
[a(ll), f(uture), l(ist)]: f
```

Run poller.py. It will keep scanning the database to look for new announced
episodes and download released torrents for released episodes.
```bash
python poller.py
```

## Dependencies

- python3.x
- [libtpb](https://bitbucket.org/mtahmed/libtpb): A simple module/library to
  provide a python interface to thepiratebay
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
