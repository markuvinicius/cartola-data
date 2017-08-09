
#!/bin/bash

echo '----------iniciando serviços--------------'
echo '----[INICIANDO MONGODB]----'
brew services start mongodb
echo '----[INICIANDO ELASTICSEARCH]----'
brew services start elasticsearch

echo '----------executando [get-cartola-data]----------'
python3 /Users/Marku/Documents/WorkSpace/cartola-data/get-cartola-data/get-cartola-data.py -auth '../auth.k'