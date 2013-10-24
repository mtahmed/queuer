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

Run the enqueue.py and follow instructions:

- Enter the name of the download (e.g. the name of the tv show)
- Enter the number of the tv show that you want to add (click the tvrage.com
  link to verify it is the one you want).
- Select which episodes you want to download. If you want all the previous
  episodes to be downloaded as well, select all. If you only want future
  episodes to be downloaded, select future. You can also list the episodes to
  see which ones you want to download.


## Dependencies

- python3.x: Yeah. Python 3.x. Start using it.
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
