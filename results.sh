#!/bin/bash

# For each run, record relevant performance metrics over the generations, such as:
# Best fitness achieved so far.
# Average fitness of the population.
# (Optional) Size or complexity of the best individual.

num_runs=10

echo "run_number,avg_fitness,gen_max,gen_min,avg_size" > results.txt # overwrites old file and starts with column names

for run in $(seq 1 $num_runs); do
    echo "Starting Run $run"
    output=$(py ./SubstitutionCipher.py)

    result=$(echo "$output" | awk '$1 == 100') # grab line of generation 100
    avg_fitness=$(echo "$result" | awk '{print $3}') 
    gen_max=$(echo "$result" | awk '{print $5}')
    gen_min=$(echo "$result" | awk '{print $6}')
    avg_size=$(echo "$result" | awk '{print $9}')

    echo "$run,$avg_fitness,$gen_max,$gen_min,$avg_size" >> results.txt
done