#!/usr/bin/env bash

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
