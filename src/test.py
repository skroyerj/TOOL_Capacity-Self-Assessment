from pathlib import Path

import main_analysis as ma
import sort_education

PARTICIPANT_INFO_AGREEMENT, INFO, ALL_Qs, include_in_df, likert_6pt = ma.to_include()

ANON_FILES = [
          Path("data/output_data/AGILE_5_anon.xlsx"),
          Path("data/output_data/AGILE_6_anon.xlsx"),
          Path("data/output_data/AGILE_7_anon.xlsx"),
          Path("data/output_data/AGILE_8_anon.xlsx"),
          Path("data/output_data/AGILE_9_anon.xlsx"),
          Path("data/output_data/AGILE_10_anon.xlsx"),
          Path("data/output_data/AGILE_11_anon.xlsx"),
          Path("data/output_data/AGILE_12_anon.xlsx"),
          Path("data/output_data/AGILE_13_anon.xlsx")]

dfs = ma.read_and_sort(ANON_FILES, include_in_df)

print("Names of dfs'", dfs.name)
# Sort by education (current master's programme or not-yet-completed bachelor's programme)


