# SEDkit with SIMPLE

To prepare, make sure your environment has the latest version of SEDkit and AstrodbKit2:

```bash
pip install sedkit
pip install AstrodbKit2
```

You will also need to have a copy of the SIMPLE database. 
You can download a SQLite binary version of SIMPLE from https://github.com/SIMPLE-AstroDB/SIMPLE-binary 
or can pull the raw data and build it yourself from https://github.com/SIMPLE-AstroDB/SIMPLE-db (see more instructions in that repo)

Once you have the database, you can place it in your current working directory and can connect to it with:

```python
from astrodbkit2.astrodb import Database
db = Database('sqlite:///SIMPLE.sqlite')
```

This `Database` object will need to be passed to `SEDSIMPLE` for it to work.

The key functionality in this package is a new class (`SEDSIMPLE`) that inherits from `SED` in order 
to provide wrappers around SIMPLE Database calls. 
For convenience, you may want to have sedsimple.py in your current working directory. 

Initiating with `SEDSIMPLE` is as simple as:

```python
from sedsimple import SEDSIMPLE
from astrodbkit2.astrodb import Database

db = Database('sqlite:///SIMPLE.sqlite')
sed = SEDSIMPLE(db, 'Trappist-1', auto_db=True)
```

The parameter `auto_db=True` tells it to load as much information from the provided database as it can. 
This includes coordinates, parallaxes, spectral types, photometry, and spectra. 
If you choose `auto_db=False` (the default), you can load whichever data you need manually with:
 - sed.load_coords_db()
 - sed.load_parallax_db()
 - sed.load_photometry_db()
 - sed.load_spectral_type_db()
 - sed.load_spectra_db()

You can use `sed.fetch_single_spectrum_db()` to fetch the wavelength, flux, flux uncertainty, 
and reference for a single spectrum if you need to do further transformations. 
The input is a Spectra row from `db.inventory`; 
see https://astrodbkit2.readthedocs.io/en/latest/ for more information on using AstrodbKit2 queries 
and the [SIMPLE Documentation](https://github.com/SIMPLE-AstroDB/SIMPLE-db/tree/main/documentation) for more info on the database structure.

Note: upon initialization `SEDSIMPLE` will search for the specified target in the database. 
The internal database name may be different from what provided name, 
but `db.search_object` is used to find the correct match. 
You may want to manually check database entries with queries like:

```python
db.search_object('Trappist-1')
db.inventory('2MASS J23062928-0502285')  # primary source name in the database for Trappist-1
```

All methods available in `SED` are available in `SEDSIMPLE` which means you can proceed as normal 
(eg, `sed.add_spectrum()`, `sed.plot()`, `sed.results`).

A tutorial notebook is available that walks you through the Trappist-1 example.
