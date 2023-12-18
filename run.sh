#!/bin/bash

if (( $# != 1 )); then
    echo "Please provide script argument: either 'mesa'' or 'solara'."
    exit 1
fi

if [[ $1 == "mesa" ]]; then
    python3 run_mesa.py
elif [[ $1 == "solara" ]]; then
    solara run run_solara.py
else
    echo "Unknown argument value. Please use either 'mesa' or 'solara'."
    exit 1
fi