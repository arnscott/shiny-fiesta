# Usage
The following package may be installed using pip
```bash
$ pip install /path/to/this/repository
```
The commands can then be used as follows:
* Count MS/MS spectra

```bash
$ count-ms2 path/to/mzMLfile
```
* Filter for FDR
```bash
$ filter-fdr -i path/to/peptide_id_file -o outfile
```
* Macth the identified Features to MS/MS spectra and Peptides
```bash
$ match-features-to-peptides -mz mzMLfile -f featurefile -p peptidefile -o outfile
```



