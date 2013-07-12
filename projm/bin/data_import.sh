#! /bin/bash
/usr/local/Cellar/mongodb/2.4.5-x86_64/bin/mongoimport --dbpath ../data --db proj_m_d --collection infos < "../export/all.json"