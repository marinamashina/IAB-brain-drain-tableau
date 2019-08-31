Práctica de Visualización - Marina Kurmanova

Getting Started
The dataset is from German IAB (Insitute for Employment and Research). 20 OECD destination countries and 195 countries of origin. The data is desaggregated by gender. The time period covered is 1980 to 2010 in 5-year intervals.
The orignal dataset is in wide format: a sigle excel sheet with 20 tabs and 195 rows per tab, 12 columns each. The dataset has been reshaped to long format to fit Tableau dataset requirements by means of python code using pandas.

Attached files
1. iabbd_8010_v1_gender.xls - original data in wide format
2. reshaping_result_long_format.xls - reshaped data in long format suitable for input to Tableau
3. pre.py - python reshape to long format code. Requirements: python 3.x and pandas
4. IAB brain-drain.twb - tableau project for visualization

Run 
1. To view Tableau project open IAB brain-drain.twb in Tableau.
(Optional): If you want to run reshape code, run:
$ python pre.py
