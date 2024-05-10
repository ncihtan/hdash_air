# Release Notes

## 2024-05-09

* Added new Folder check table to identify folders with un-annotated files.
* Added CDS File Name check.

## 2023-04-08

* Migrated to new Airflow infrastructure.
* Misc. front-end changes based on Bootstrap.

## 2023-03-23

* Fixed Discrepancies between HTAN Dashboard and BigQueries.  See:  https://github.com/ncihtan/hdash/issues/12
* Heatmaps now represent "completeness" of data, where 1 indicates availability of data, and 0 indicates absense of data.
* Metafile table now include percent of completed metadata fields.  This represents the total number of metadata fields that have data that is not set to, e.g. "unknown", "not applicable", "not reported".  See:  https://github.com/ncihtan/hdash/blob/59c0c1b0bed3dc4a15ba4f0aa7016b5ccaef3332/hdash/stats/meta_summary.py#L11  
* Cytoscape SIF networks have been added back to the atlas pages.