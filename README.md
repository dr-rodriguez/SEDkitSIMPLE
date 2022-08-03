# SEDkit with SIMPLE

To prepare, make sure your environment has the latest version of SEDkit and AstrodbKit2:

```bash
pip install sedkit
pip install AstrodbKit2
```

You will also need to have a copy of the SIMPLE database. 
If you have it in your current working directory you can connect to it with:

```python
from astrodbkit2.astrodb import Database
db = Database('sqlite:///SIMPLE.db')
```

This will need to be passed to `SEDSIMPLE` for it to work.

The key functionality in this package is a new class (`SEDSIMPLE`) that inherits from `SED` in order 
to provide wrappers around SIMPLE Database calls. 
For convenience, you may want to have utils.py in your current working directory. 
Initiating with `SEDSIMPLE` is as simple as:

```python
from utils import SEDSIMPLE
from astrodbkit2.astrodb import Database

db = Database('sqlite:///SIMPLE.db')
sed = SEDSIMPLE(db, 'Trappist-1', auto_db=True)
```

The parameter `auto_db=True` tells it to load as much information from the provided database as it can. 
This includes coordinates, parallaxes, spectral types, photometry, and spectra. 
If you choose `auto_db=False` (the default), you can load whichever data you need with:
 - sed.load_coords_db()
 - sed.load_parallax_db()
 - sed.load_photometry_db()
 - sed.load_spectral_type_db()
 - sed.load_spectra_db()

Note: upon initialization `SEDSIMPLE` will search for the specified target in the database. 
The internal database name may be different from what provided name. 
You may want to manually check database entries with:

```python
db.search_object('Trappist-1')
db.inventory('2MASS J23062928-0502285')  # primary source name in the database for Trappist-1
```

All methods available in `SED` are available in `SEDSIMPLE` which means you can proceed as normal.

# TODO:
 - Finish writing load_spectra_db
 - Write example notebook
