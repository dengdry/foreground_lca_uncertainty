# Foreground LCA Uncertainty Analysis

[![Python Version](https://img.shields.io/badge/python-3.8%2B-blue)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)

---

## Project Overview

This project provides an implementation of data uncertainty analysis for Life Cycle Assessment (LCA), focusing on the integration of **foreground system uncertainty** using the **Pedigree Matrix** method. It leverages the capabilities of [Brightway2.5](https://brightway.dev/)—a next-generation framework for LCA in Python—to perform Monte Carlo simulations and visualize the uncertainty impact on LCA results.

---

## Key Features

- Import custom Excel-based foreground models  
- Automatically parse Pedigree Matrix parameters and calculate uncertainty scales  
- Generate Monte Carlo random samples for uncertainty propagation  
- Output statistical distributions of LCA impact scores with visualization support  
- Highly extensible for integration of advanced analyses such as sensitivity studies  

---

## Technologies & Dependencies

This project is based on the following main packages:

- [`brightway2.5`](https://brightway.dev/) – LCA data framework and calculation engine
- `pedigree_matrix` – Pedigree matrix-based uncertainty propagation
- `stats_arrays` – Uncertainty distributions and sampling
- `pandas`, `numpy`, `matplotlib` – Data processing & visualization
---

## Installation

Recommended Python version: 3.8 or above.

```bash
# Create virtual environment
python -m venv venv
source venv/bin/activate   # Linux/macOS
venv\Scripts\activate      # Windows

# Install dependencies
pip install -r requirements.txt
```
---

## Example

You can try the workflow interactively using the included Jupyter Notebook:

examples/uncertainty_demo.ipynb

This notebook demonstrates:

Setting up a Brightway project

Importing data and applying Pedigree Matrix uncertainty

Generating Monte Carlo samples

Running LCA with uncertainty

Plotting impact score distribution

## Related Publication

This repository supports the results presented in the following scientific publication:

**"The Application of LCA Data Uncertainty Analysis in the Sustainable Development Process"**  
*Ruiyang Deng, Sebastian Kilchert*  
Automotive Production Technology – Digital Product Development and Manufacturing. SCAP 2024. ARENA2036. Springer, Cham. https://doi.org/10.1007/978-3-031-88831-1_29
