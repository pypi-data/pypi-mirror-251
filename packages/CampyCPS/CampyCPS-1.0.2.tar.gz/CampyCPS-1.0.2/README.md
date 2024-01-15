# CampyCPS


CampyCPS is a tool for Campylobacter CPS relevant genes identification.

```
usage: CampyCPS -i <genome assemble directory> -o <output_directory>

Author: Qingpo Cui(SZQ Lab, China Agricultural University)

optional arguments:
  -h, --help      show this help message and exit
  -i I            <input_path>: the PATH to the directory of assembled genome files. Could not use with -f
  -f F            <input_file>: the PATH of assembled genome file. Could not use with -i
  -o O            <output_directory>: output PATH
  -minid MINID    <minimum threshold of identity>, default=95
  -mincov MINCOV  <minimum threshold of coverage>, default=90
  -init      <initialize the reference database>
  -t T            <number of threads>: default=8
  -v, --version   Display version
```


## Installation
### Using pip
pip3 install CampyCPS

### Using conda
comming soon...

## Dependency
- BLAST+ >2.7.0

**you should add BLAST in your PATH**


## Blast installation
### Windows


Following this tutorial:
[Add blast into your windows PATH](http://82.157.185.121:22300/shares/BevQrP0j8EXn76p7CwfheA)

### Linux/Mac
The easyest way to install blast is:

```
conda install -c bioconda blast
```

## Usage

The first time when running CampyCPS, you should use **CampyCPS -init** command to initialize your database.

**The default database including the following genes.**

### CPS relevant genes
| Loci     | Gene/Aliases   | Full name/product                                                           |
|----------|----------------|-----------------------------------------------------------------------------|
| CAMP1067 | waaF           | Heptosyltransferase II (K02843)                                             |
| CAMP1326 | cysC           | Putative adenylylsulfate kinase (K00860)                                    |
| CAMP1327 | Cj1416c        | Putative sugar nucleotidyltransferase                                       |
| CAMP1328 | Cj1417c        | Putative amidotransferase (K07010)                                          |
| CAMP1329 | Cj1418c        | Putative transferase                                                        |
| CAMP1330 | Cj1419c        | Putative methyltransferase                                                  |
| CAMP1331 | Cj1420c        | Putative methyltransferase                                                  |
| CAMP1332 | Cj1421c        | Putative sugar transferase                                                  |
| CAMP1333 | Cj1422c        | Putative sugar transferase                                                  |
| CAMP1334 | hddC           | Putative D-glycero-D-manno-heptose 1-phosphate guanosyltransferase (K15669) |
| CAMP1335 | gmhA2          | Phosphoheptose isomerase (K03271)                                           |
| CAMP1336 | hddA           | Putative D-glycero-D-manno-heptose 7-phosphate kinase (K07031)              |
| CAMP1337 | Cj1426c        | Putative methyltransferase family protein                                   |
| CAMP1338 | Cj1427c        | Putative sugar-nucleotide epimerase/dehydratease                            |
| CAMP1339 | fcl            | GDP-L-fucose synthetase (K02377)                                            |
| CAMP1340 | Cj1429c        | Hypothetical protein Cj1429c                                                |
| CAMP1341 | rfbC           | Putative dTDP-4-dehydrorhamnose 3,5-epimerase (K01790)                      |
| CAMP1342 | hddC           | Capsular polysaccharide heptosyltransferase                                 |
| CAMP1343 | Cj1432c        | Putative sugar transferase                                                  |
| CAMP1344 | Cj1433c        | Hypothetical protein Cj1433c                                                |
| CAMP1345 | Cj1434c        | Putative sugar transferase                                                  |
| CAMP1346 | Cj1435c        | Putative phosphatase                                                        |
| CAMP1347 | Cj1436c        | Aminotransferase                                                            |
| CAMP1348 | Cj1437c        | Aminotransferase (K00817)                                                   |
| CAMP1349 | Cj1438c        | Putative sugar transferase                                                  |
| CAMP1350 | glf            | UDP-galactopyranose mutase (K01854)                                         |
| CAMP1351 | Cj1440c        | Putative sugar transferase                                                  |
| CAMP1352 | kfiD           | UDP-glucose 6-dehydrogenase (K00012)                                        |
| CAMP1353 | Cj1442c        | Putative sugar transferase                                                  |
| CAMP1354 | kpsF           | D-arabinose 5-phosphate isomerase (K06041)                                  |
| CAMP1355 | kpsD           | Capsule polysaccharide export system periplasmic protein                    |
| CAMP1356 | kpsE           | Capsule polysaccharide export system inner membrane protein (K10107)        |
| CAMP1357 | kpsT           | Capsule polysaccharide export ATP-binding protein (K09689)                  |
| CAMP1358 | kpsM           | Capsule polysaccharide export system inner membrane protein (K09688)        |

### Example
```
# Single Genome Mode
CampyCPS -f /PATH_TO_ASSEBLED_GENOME/sample.fa -o PATH_TO_OUTPUT

# Batch Mode
CampyCPS -i /PATH_TO_ASSEBLED_GENOME_DIR -o PATH_TO_OUTPUT
```
