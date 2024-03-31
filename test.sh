#!/bin/bash

# Loop from 1 to 10
for i in {1..10}; do
    # Convert the loop variable to a two-digit string
    arg=$(printf "testcases/T%02d" $i)

    # Call test.py with the argument
    python test.py "$arg"
done

echo "Done"
