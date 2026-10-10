#!/usr/bin/env bash
# Re-check CORS for candidate data endpoints (simple GET with an Origin header). Run 2026-10-09 for the notes.
# A browser (Pyodide pyfetch) can read the response only if Access-Control-Allow-Origin is "*" or echoes the page origin.
ORIGIN="${1:-https://qollab.xyz}"
while read -r u; do
  [ -z "$u" ] && continue
  h=$(curl -s -m 30 -o /dev/null -D - -H "Origin: $ORIGIN" -A "Mozilla/5.0" "$u")
  echo "$u | $(echo "$h" | grep -i '^HTTP' | tr -d '\r' | tail -1) | $(echo "$h" | grep -i '^access-control-allow-origin' | tr -d '\r' | tail -1)"
done <<'URLS'
https://query1.finance.yahoo.com/v8/finance/chart/AAPL?range=1mo&interval=1d
https://stooq.com/q/d/l/?s=aapl.us&i=d
https://fred.stlouisfed.org/graph/fredgraph.csv?id=DGS10
https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol=IBM&apikey=demo
https://api.twelvedata.com/time_series?symbol=AAPL&interval=1day&apikey=demo
https://api.frankfurter.dev/v1/latest
https://data-api.ecb.europa.eu/service/data/EXR/D.USD.EUR.SP00.A?lastNObservations=2&format=jsondata
https://api.fiscaldata.treasury.gov/services/api/fiscal_service/v2/accounting/od/avg_interest_rates
https://api.coingecko.com/api/v3/ping
https://data-api.binance.vision/api/v3/klines?symbol=BTCUSDT&interval=1d&limit=5
https://api.exchange.coinbase.com/products/BTC-USD/candles
https://api.worldbank.org/v2/country/US/indicator/NY.GDP.MKTP.CD?format=json
https://raw.githubusercontent.com/power-grid-lib/pglib-opf/master/pglib_opf_case14_ieee.m
https://cdn.jsdelivr.net/gh/MATPOWER/matpower@master/data/case14.m
https://api.eia.gov/v2/electricity/rto/region-data/data/?api_key=DEMO_KEY
https://api.open-meteo.com/v1/forecast?latitude=35&longitude=-85&hourly=temperature_2m
https://power.larc.nasa.gov/api/temporal/daily/point?parameters=T2M&community=AG&longitude=-90&latitude=40&start=20240101&end=20240105&format=JSON
https://api.carbonintensity.org.uk/intensity
https://overpass-api.de/api/status
https://earthquake.usgs.gov/earthquakes/feed/v1.0/summary/significant_month.geojson
https://www.fema.gov/api/open/v2/DisasterDeclarationsSummaries?$top=1
https://data.humdata.org/api/3/action/package_search?rows=1
https://services.nvd.nist.gov/rest/json/cves/2.0?resultsPerPage=1
https://clinicaltrials.gov/api/v2/studies?pageSize=1
https://api.fda.gov/drug/event.json?limit=1
https://rest.uniprot.org/uniprotkb/P69905.fasta
https://files.rcsb.org/download/1CRN.pdb
https://www.openml.org/api/v1/json/data/31
https://archive.ics.uci.edu/ml/machine-learning-databases/statlog/german/german.data
https://people.brunel.ac.uk/~mastjjb/jeb/orlib/files/port1.txt
URLS
