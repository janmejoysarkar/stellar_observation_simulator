![Logo](https://suit.iucaa.in/sites/default/files/top_banner_compressed_2_1.png)
# SUIT ☀️🛰️ Stellar Observation Simulator
Simulate what Sirius might look like when seen through SUIT. It simulates the predicted observation with the movement of the PSF due to satellite jitter/ drift.
## Authors

- [@janmejoysarkar](https://github.com/janmejoysarkar)

## Acknowledgements

 - [IUCAA, Pune](https://www.iucaa.in)
 - [ISRO, Aditya-L1](https://www.isro.gov.in/Aditya_L1.html)



## Usage/Examples

### PSF generation
Run `src/data/psf.py` to generate sample PSF from post-disasm data. The PSF is  saved in `data/interim/psf.fits`. A sample PSF is already generated.

### Batch processing
Use  `src/simulated_observation.py` to generate mock observations using PSF and user defined values. Processed images will be saved in `data/processed`

NOTE: This is prepared without any functions for easy testing and to extend it to further usecases, like implementing sun center information to mode the PSF.
