# Hybrid Analytics of Formula 1 Driver-Mechanic Radio Messages


## Overview

This project demonstrates a **hybrid analytics pipeline** for Formula 1 (F1) data, integrating structured race event data from PostgreSQL with unstructured driver-mechanic radio messages stored in MongoDB. The solution enables cross-domain analysis of communication patterns, event causality, and team strategies—insights that are not possible using single-source analytics.

## Features

- **Hybrid Data Integration:**  
  - Structured F1 race data (results, constructors, pit stops, circuits) in PostgreSQL.
  - Unstructured, tagged radio messages in MongoDB.
- **Synthetic Data Generation:**  
  - Realistic radio messages programmatically generated based on actual race events, ensuring event/message integrity.
- **Flexible Analytics Pipeline:**  
  - Python scripts using `pandas`, `pymongo`, and `psycopg2` for ETL and data analysis.
  - Cross-database queries for event/message validation, communication escalation, and team/circuit analytics.
- **Visualization:**  
  - Export-ready CSVs for use in Tableau or other BI tools.

## Project Structure

```
.
├── data/                   # (Optional) CSV or fixture data sources
├── data_generation/        # Creating accurate radio messages 
├── etl/                    # Loading Postgres and Mongo with the desired files (change the destination paths)
├── output/                 # Exported CSVs and Tableau sheets
├── F1_2page_abstract.pdf   # Extended abstract describing the methodology
├── queries/                # Directory storing the hybrid queries that performed the interoperation between the 2 systems
├── f1_fonts/               # Fonts used for the presentation
├── requirements.txt        # Python dependencies
└── README.md               # This file
```

## Getting Started

### Prerequisites

- Python 3.8+
- PostgreSQL (with F1 data loaded)
- MongoDB (with radio messages loaded)
- Recommended: [Tableau](https://www.tableau.com/) for visualization

### Installation

1. **Clone the repository:**
   ```bash
   git clone https://github.com/StratosDns/F1_PROJECT.git
   cd F1_PROJECT
   ```

2. **Install Python dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Configure Database Connections:**
   - Update connection strings in the `/ETL` scripts as appropriate for your local setup.

### Data Loading

- **Structured data:**  
  Download the [Kaggle F1 Dataset](https://www.kaggle.com/datasets/rohanrao/formula-1-world-championship-1950-2020) and load it into PostgreSQL.
- **Unstructured data:**  
  Use provided scripts to generate synthetic radio messages and insert into MongoDB, or use your own dataset.

### Running Analytics

Navigate to the `queries/` directory and execute the desired queries/analytics. Example:
```bash
python queries/hQ1.py
python queries/hQ2.py
```
Refer to script headers and comments for details.

### Visualization

- Exported CSVs in `results/` can be imported into Tableau or your preferred BI tool.

## Results

Key findings and visualizations are documented in the [F1_2page_abstract.pdf](F1_2page_abstract.pdf) and in sample outputs. Highlights include:


## References

- Kaggle F1 Dataset: [Formula 1 World Championship 1950-2020](https://www.kaggle.com/datasets/rohanrao/formula-1-world-championship-1950-2020)
- F1 fonts used: [font link](https://fontforfree.com/formula-1-font/)


**Contact:**  
Efstratios Demertzoglou  
Hellenic Mediterranean University  
[GitHub Issues](https://github.com/StratosDns/F1_PROJECT/issues)
