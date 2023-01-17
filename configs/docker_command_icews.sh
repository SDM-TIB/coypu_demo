#!/bin/bash

docker stop icews_endpoint

docker rm icews_endpoint

rm -rf /data/coypu/icews_endpoint/data/*.*

docker run -d --name icews_endpoint -v '/data/coypu/icews_endpoint/data_load/:/app/data' -v '/data/coypu/icews_endpoint/data/:/data' -p 11382:8890 --env NAMEDGRAPH=https://icews.coypu.org asakor/kglocal:latest

docker logs -f icews_endpoint