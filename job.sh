#!/bin/bash

for i in 4 6 8 10 12 14 16 18 20
do
    python3 graphs.py --type chains --nodes $i | python3 minimizer.py --depth 4
done
