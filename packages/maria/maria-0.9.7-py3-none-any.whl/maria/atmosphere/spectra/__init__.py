import os

import h5py

from ... import utils
from ...site import InvalidRegionError, all_regions

here, this_filename = os.path.split(__file__)

SPECTRA_DATA_DIRECTORY = f"{here}/data"
SPECTRA_DATA_CACHE_DIRECTORY = "/tmp/maria_data_cache/spectra"
SPECTRA_DATA_URL_BASE = "https://github.com/thomaswmorris/maria/raw/master/maria/atmosphere/spectra/data"  # noqa F401
MAX_CACHE_AGE_SECONDS = 86400


class AtmosphericSpectrum:
    def __init__(self, region, source="am", from_cache=None):
        """
        A dataclass to hold spectra as attributes.
        """

        if region not in all_regions:
            raise InvalidRegionError(region)

        self.region = region
        self.source = source
        self.source_path = f"{SPECTRA_DATA_DIRECTORY}/{self.source}/{self.region}.h5"

        # if the data isn't in the module, default to use the cache
        self.from_cache = (
            from_cache
            if from_cache is not None
            else not os.path.exists(self.source_path)
        )

        if self.from_cache:
            self.source_path = (
                f"{SPECTRA_DATA_CACHE_DIRECTORY}/{self.source}/{self.region}.h5"
            )
            utils.io.fetch_cache(
                source_url=f"{SPECTRA_DATA_URL_BASE}/{self.source}/{self.region}.h5",
                cache_path=self.source_path,
                max_cache_age=MAX_CACHE_AGE_SECONDS,
            )
            self.from_cache = True

        with h5py.File(self.source_path, "r") as f:
            self.side_nu_GHz = f["side_nu_GHz"][:].astype(float)
            self.side_elevation_deg = f["side_elevation_deg"][:].astype(float)
            self.side_line_of_sight_pwv_mm = f["side_line_of_sight_pwv_mm"][:].astype(
                float
            )
            self.temperature_rayleigh_jeans_K = f["temperature_rayleigh_jeans_K"][
                :
            ].astype(float)
            self.phase_delay_um = f["phase_delay_um"][:].astype(float)
