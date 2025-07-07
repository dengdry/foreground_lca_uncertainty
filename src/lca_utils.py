import os
import numpy as np
import bw2data as bd
import bw2io as bi
import bw2calc as bc
from pedigree_matrix import PedigreeMatrix


def setup_project(project_name):
    """
    Set the current Brightway2 project and initialize default biosphere and methods.
    """
    bd.projects.set_current(project_name)
    bi.bw2setup()


def import_background(path, db_name):
    """
    Import the ecoinvent background database from a local directory into the Brightway2 project.
    """
    if db_name not in bd.databases:
        importer = bi.SingleOutputEcospold2Importer(path, db_name)
        importer.apply_strategies()
        importer.write_database()
    else:
        print("[INFO] Background DB already exists.")


def import_foreground_with_uncertainty(excel_path, fg_db_name, bg_db_name):
    """
    Import a foreground system from an Excel file, apply Pedigree Matrix uncertainty
    to its exchanges, and save it as a new Brightway2 database.

    === Pedigree Matrix Dimension Constants (P1–P5) ===
    'P1'     # Reliability: Source of the data (e.g., measured, estimated)
    'P2'     # Completeness: Coverage of data over time, flows, or processes
    'P3'   # Temporal correlation: How well the data matches the timeframe
    'P4'   # Geographical correlation: Relevance to the study region
    'P5'    # Further technological correlation: Technological representativeness
    """
    pedigree_keys = ['P1', 'P2', 'P3', 'P4', 'P5']
    imp = bi.ExcelImporter(excel_path)
    bi.create_core_migrations()
    imp.apply_strategies()
    imp.match_database(fields=('name', 'unit', 'location', 'reference product'))
    imp.match_database(bg_db_name, fields=('name', 'unit', 'location', 'reference product'))

    for act in imp.data:
        for exc in act.get("exchanges", []):
            if exc.get('type') == 'production':
                continue
            if 'Pedigree matrix' not in exc:
                exc['Pedigree matrix'] = tuple(exc.pop(k, 1) for k in pedigree_keys)
            if exc['Pedigree matrix'] == (1, 1, 1, 1, 1):
                exc['uncertainty type'] = 1
            if exc['uncertainty type'] == 2:
                exc['loc'] = np.log(exc['amount'])
            else:
                exc['loc'] = exc['amount']
            pm = PedigreeMatrix(version=1)
            pm.from_numbers(*exc['Pedigree matrix'])
            try:
                exc['scale'] = np.log(pm.calculate(basic_uncertainty=1, as_geometric_sigma=True))
            except Exception:
                exc['scale'] = 0
            if exc['scale'] == 0:
                exc['uncertainty type'] = 0

    imp.write_database(name=fg_db_name)
    print("[INFO] Foreground DB written.")


def run_mc_simulation(fg_db_name, product_key, method, iterations=100):
    """
    Run Monte Carlo simulations for a specified product using a given LCIA method,
    and return the list of LCA scores across iterations.
    """
    db = bd.Database(fg_db_name)
    product = db.get(product_key)
    results = []
    for i in range(iterations):
        lca = bc.LCA({product: 1}, method, use_distributions=True)
        lca.lci()
        lca.lcia()
        results.append(lca.score)

    return results
