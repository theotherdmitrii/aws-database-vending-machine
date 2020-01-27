#!/usr/bin/env bash

pulumi destroy --skip-preview

pulumi stack rm dev -y &>/dev/null;