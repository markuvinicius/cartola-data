
#!/bin/bash

echo '----------iniciando serviços--------------'
echo '----[INICIANDO MONGODB]----'
brew services start mongodb
echo '----[INICIANDO ELASTICSEARCH]----'
brew services start elasticsearch

echo '----------executando [get-cartola-data]----------'
python3 get-cartola-data/get_cartola_data.py -auth '../auth.k'
