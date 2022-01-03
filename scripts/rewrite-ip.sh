#!/usr/bin/env bash

ipAddr=$(hostname -i)
export DISPLAY=$ipAddr:0.0
