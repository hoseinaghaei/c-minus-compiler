#!/bin/bash

# Loop from 1 to 10
for i in {1..10}; do
    # Convert the loop variable to a two-digit string
    arg=$(printf "P2_testcases/T%02d" $i)
    echo "$arg"

    # Call test.py with the argument
    python test.py "$arg" 1
    python test.py "$arg" 0
done

echo "Done"
