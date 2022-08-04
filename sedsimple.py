# Wrapper to implement a subclass of SED that works natively with SIMPLE through Astrodbkit2
# David R Rodriguez
# 2022-08   Initial implementation

import astropy.units as u
from astropy.units.quantity import Quantity
from astropy.coordinates import Angle, SkyCoord
from sedkit import SED


class SEDSIMPLE(SED):
    def __init__(self, db, name, auto_db=False, **kwargs):
        # ProcessClass initialization
        super().__init__(name, **kwargs)

        # Database variable
        self.db = db

        # Check if the name in the database is different
        # If a match is found,  use that as a temporary overwrite of the name when fetching the inventory
        Sources = db.search_object(name)
        if len(Sources) == 1:
            db_name = Sources['source'][0]
            if db_name != name:
                self.message(f'{name} matched to {db_name} in the database', pre='[SIMPLE]')
                name = db_name

        # Database inventory
        self.inventory = db.inventory(name, pretty_print=False)

        if auto_db:
            self.load_coords_db()
            self.load_parallax_db()
            self.load_photometry_db()
            self.load_spectral_type_db()
            self.load_spectra_db()

    def load_coords_db(self):
        # Fetch coordiantes from database
        table = 'Sources'
        if table in self.inventory:
            if len(self.inventory[table]) == 1:
                data = self.inventory[table][0]
                s = SkyCoord(ra=data['ra']*u.degree, dec=data['dec']*u.degree)
                self.sky_coords = s
            else:
                self.message(f"More than one source in database: \n{self.inventory[table]}", pre='[SIMPLE]')
        else:
            self.message(f"Source {self.name} not in database.", pre='[SIMPLE]')

    def load_parallax_db(self):
        # Fetch parralax from database
        table = 'Parallaxes'
        if table in self.inventory:
            # Fetch the adopted parallax
            for row in self.inventory[table]:
                if row['adopted']:
                    value = Quantity(row['parallax'], unit=u.mas)
                    error = Quantity(row['parallax_error'], unit=u.mas)

                    # Fetch reference used in database
                    bibcode = self._fetch_db_bibcode(row['reference'])

                    # Store value
                    self.parallax = value, error, bibcode
        else:
            self.message(f"No parallax for {self.name} in database.", pre='[SIMPLE]')

    def load_photometry_db(self):
        # Fetch photometry from database
        table = 'Photometry'
        if table in self.inventory:
            # Fetch the adopted parallax
            for row in self.inventory[table]:
                bibcode = self._fetch_db_bibcode(row['reference'])
                band = self._fix_bands(row['band'])
                self.add_photometry(band, row['magnitude'], mag_unc=row['magnitude_error'], ref=bibcode)
        else:
            self.message(f"No photometry for {self.name} in database.", pre='[SIMPLE]')

    def load_spectral_type_db(self):
        # Fetch spectral type from database
        table = 'SpectralTypes'
        if table in self.inventory:
            # Fetch the adopted spectral type
            for row in self.inventory[table]:
                if row['adopted']:
                    bibcode = self._fetch_db_bibcode(row['reference'])
                    self.spectral_type = row['spectral_type_string'], bibcode
        else:
            self.message(f"No spectral type for {self.name} in database.", pre='[SIMPLE]')

    def load_spectra_db(self):
        pass

    def _fix_bands(self, band):
        # Manual fixes to some SIMPLE bands
        FIX_DICT = {'GAIA2': 'Gaia',
                    'GAIA3': 'Gaia',
                    'Gaia.Grp': 'Gaia.rp',
                    'GaiaGbp': 'Gaia.bp'
                    }
        for key, value in FIX_DICT.items():
            band = band.replace(key, value)
        return band

    def _fetch_db_bibcode(self, ref):
        # Utility function to fetch a reference from the database
        try:
            t = self.db.query(self.db.Publications.c.bibcode). \
                filter(self.db.Publications.c.publication == ref). \
                table()
            bibcode = t['bibcode'][0]
        except Exception as e:
            self.message(f'Error trying to fetch references: {e}', pre='[SIMPLE]')
            bibcode = None

        # Fix for missing bibcode (sedkit can't handle None)
        if bibcode is None:
            bibcode = ''

        return bibcode
