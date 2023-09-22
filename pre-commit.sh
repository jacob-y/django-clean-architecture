#!/usr/bin/env bash

# Run the unit tests and check that they are successful before accepting any commit

'python3 -m unittest discover .'
if [[ $? = 0 ]]
then
    echo "> Tests passed"
else
    echo "> Tests DID NOT pass"
    exit 1
fi

echo "Ready to commit"
exit 0
