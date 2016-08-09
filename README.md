README


Intro
-----


database.py: for postprocess of merger tree
DataImport/*: Modules of importing merger tree, halo properties, particles

USAGE:
 - put the directory DataImport in to the package-site path or put it in the
 - working directory or put to any path you like and import it to the PATH enviroment.

 - import DataImport

## Construct a tree and importing data
tree = DataImport(inputfile, type='filetype', keyword=keyword,
maxsnap=maxsnap, filez=filez)
tree[snap][haoid][nth pro]=proid

## Construct a empty halo catalogue
halo = DataImport(filez=filez)

## import properties of halos from one snap
halo.import_one_snap(file, col=col, ftype=ftype)
## import properties of all snaps
halo.import_all_snap(file, col=col, keyword=keyword, ftype=ftype)
## col is a diction to indicate the properties to be imported
## ftype indicate the file type, this programe only work for txt property files
## keyword is the extend that can distinct the merger tree file, like 'mtree'


## filez file is a file list the redshift of each snap, it's necessary for importing all datas.

halo[snap]['property'][haloid]=value

