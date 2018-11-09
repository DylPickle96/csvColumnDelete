#!/usr/bin/env bash

curl -o Adtaxi.csv ftp://ftp.adacado.com/Adtaxi.csv --user felec:apkqbfuyz

./abtElectronics -csv=Adtaxi.csv -columnsToDelete=name,description -delimiter=,

python csv2xml.py -i Adtaxi.csv -o ADCO_ABTFeed.xml -d ,

curl -T ADCO_ABTFeed.xml ftp://ftp.adacado.com/ADCO_ABTFeed.xml --user felec:apkqbfuyz