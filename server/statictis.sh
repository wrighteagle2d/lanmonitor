#!/bin/bash

cat log | awk '{print $1}' | sort | uniq -c | sort -n
