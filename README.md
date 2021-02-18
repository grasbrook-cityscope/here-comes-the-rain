# Here comes the rain

create a SWMM storm event time series from KOSTRA data

---

## Installation

Requires
* Python3

```$ python3 -m pip install -r requirements.txt ```


## Usage

`$ python3 parse_kostra.py [-h] datadir index` to create a CSV table from KOSTRA shapefiles

`$ python3 make_timeseries.py [-h] [--interval INTERVAL] [--type1] datapath returnperiod duration` to create a timeseries file from the parsed CSV file
