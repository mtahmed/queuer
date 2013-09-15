# queuer

Makes it super easy to set up recurring downloads from [thepiratebay](thepiratebay.sx).

# Setting it up

## Settings

Clone the repository to wherever is convenient (e.g. `~/bin/queuer`):

    cd ~/bin/
    hg clone https://mtahmed@bitbucket.org/mtahmed/queuer

Then clone libtpb:

    cd ~/bin/queuer
    hg clone https://mtahmed@bitbucket.org/mtahmed/libtpb

Edit settings.py appropriately. For most users, the settings are just fine.

## Adding downloads

Run the enqueue.py and follow instructions:

- Enter the name of the download (e.g. the name of the tv show)
- Enter the number of the tv show that you want to add (click the tvrage.com
  link to verify it is the one you want).
- Select which episodes you want to download. If you want all the previous
  episodes to be downloaded as well, select all. If you only want future
  episodes to be downloaded, select future. You can also list the episodes to
  see which ones you want to download.


# Dependencies

## python3.x

Yeah. Python 3.x. Start using it.

## libtpb

[libtpb](https://bitbucket.org/mtahmed/libtpb): A simple module/library to
provide a python interface to thepiratebay

## aria2

For now, only the aria2 downloader is supported. You may submit patches to
support additional downloaders. Will only need to add a new downloader in
torrentdl.py and make changes to how it's used etc.

# Notes

- The episodes will download to the default download directory in aria2.
- Simultaneous downloads limits, upload speeds, download speeds, continuing
  downloads etc. is all taken care of by the downloader.
