# Staff Scheduling with Genetic Algorithm and Z3 Solver

This repository contains Python scripts that demonstrate staff scheduling using two different approaches: a genetic algorithm (with the DEAP library) and the Z3 SMT solver. The scripts are designed to generate weekly schedules, considering constraints such as maximum consecutive working days, minimum days off, and specific vacation requests.

## Table of Contents

1. [Installation](#installation)
2. [Usage](#usage)
3. [Script Descriptions](#script-descriptions)
4. [Input Format](#input-format)
5. [Output Explanation](#output-explanation)
6. [Verification](#verification)
7. [Contributing](#contributing)

## Installation

Ensure you have Python installed on your system. Additionally, install the required libraries:

```bash
pip install deap z3-solver numpy
```

## Usage

To run the scheduling scripts and verify their output, use the following commands:

```bash
python test-deap.py | python verify.py
python test-z3.py | python verify.py
```

## Script Descriptions

### test-deap.py

Implements a genetic algorithm to solve the staff scheduling problem. It uses the DEAP library to evolve a population of potential schedules, aiming to minimize conflicts and respect constraints.

Key Features:
- Constants for days, staff, shifts, and constraints
- Vacation request handling
- Fitness function to evaluate schedules
- Genetic operators (mutation, crossover, selection)

### test-z3.py

Utilizes the Z3 SMT solver for staff scheduling. It translates the scheduling problem into a set of logical constraints and finds a solution that satisfies them.

Highlights:
- Formulating scheduling constraints
- Handling vacation requests
- Using Z3 to find a schedule that satisfies all constraints

### verify.py

Processes the output of the scheduling scripts to verify if the generated schedules meet all requirements. It checks for total shifts, night shifts, consecutive working days, days off, and coverage of all shifts.

Features:
- Parsing of vacation requirements and generated schedules
- Detailed checks for each constraint
- Output of verification results and explanations

## Input Format

Scripts expect input in a specific format. For instance, vacation requests should be provided as a dictionary with staff IDs as keys and lists of requested days off as values.

## Output Explanation

The scripts output the generated schedule along with any constraint violations. The `verify.py` script further explains the scheduling decisions and constraint compliance.

## Verification

Run `verify.py` to analyze the output of the scheduling scripts. It will provide a detailed explanation of how the schedule meets (or fails to meet) the various constraints.

## Installing Dependencies

For Debian-based Linux distributions, you can install the necessary Python libraries using the following `sudo apt` commands:

```bash
sudo apt install python3-deap
sudo apt install python3-z3
```
## Understanding Genetic Algorithms (GA) vs. SAT Solvers

### Genetic Algorithms (GA)

GAs are stochastic optimization techniques inspired by natural evolution. They are particularly effective for complex problems where the solution space is vast and not easily traversable using deterministic methods. GAs use randomness in various stages, including initial population generation, selection, crossover, and mutation. This randomness helps in exploring the solution space, maintaining diversity in the population, and avoiding premature convergence on suboptimal solutions. GAs are suited for problems where finding an approximate or 'good enough' solution is acceptable.

### Boolean Satisfiability Problem (SAT) Solvers

SAT solvers, in contrast, are deterministic and are used for decision problems. They determine whether a given Boolean formula can be satisfied. SAT solvers use logical deduction and systematic search strategies, employing algorithms like DPLL or CDCL. These solvers systematically explore variable assignments, aiming to either find a satisfying assignment or prove that none exists. They are ideal for problems that can be expressed in logical formulas and require definitive yes/no answers.

### Key Differences

- **Randomness**: Central to GAs for exploring solution space and maintaining diversity; not used in SAT solvers which follow a more deterministic approach.
- **Problem Types**: GAs are used for optimization problems; SAT solvers are used for decision problems.
- **Methodology**: GAs evolve populations of solutions using mechanisms akin to natural selection; SAT solvers systematically explore variable assignments based on logical constraints.
- **Determinism**: GAs are inherently stochastic and can produce different outcomes; SAT solvers typically produce consistent results for the same problem and configuration.

