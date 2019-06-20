from __future__ import print_function
import os, glob, itertools

# Delete conll files in conll-formatted-ontonotes-5.0

results = itertools.chain.from_iterable(glob.iglob(os.path.join(root, '*_conll'))
                                        for root, dirs, files in
                                        os.walk('conll-formatted-ontonotes-5.0/'))
results = list(results)
print("Delete {} conll files.".format(len(results)))
for result in results:
    os.remove(result)