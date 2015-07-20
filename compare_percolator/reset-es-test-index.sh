#!/bin/sh

curl -XDELETE localhost:9200/test
curl -XPUT localhost:9200/test -d'
    {
        "settings" : {
            "number_of_shards" : 1
        },
        "mappings" : {
            "doc" : {
                "properties" : {
                    "text" : { "type" : "string", "analyzer" : "standard" }
                }
            }
        }
    }'