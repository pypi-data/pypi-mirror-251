#!/bin/bash

pytest
coverage xml -o reports/coverage/coverage.xml
flake8 --exit-zero --output-file reports/flake8/flake8stats.txt

genbadge tests -o reports/assets/tests_badge.svg
genbadge coverage -o reports/assets/coverage_badge.svg
genbadge flake8 -o reports/assets/flake8_badge.svg

