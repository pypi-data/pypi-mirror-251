#!/usr/bin/env bash
(
  cd src || exit 1
  xsdata --config ../.xsdata.xml momotor/bundles/schema/
)
