#!/usr/bin/env bash

# Make the config dir
mkdir -p /tmp/config


# Symlink the custom_components dir
if [ -d "/tmp/config/custom_components" ]; then
  rm -rf /tmp/config/custom_components
fi
ln -sf "${PWD}/custom_components" /tmp/config/custom_components

ln -sf "${PWD}/config/configuration.yaml" /tmp/config/configuration.yaml


# Start Home Assistant
hass -c /tmp/config