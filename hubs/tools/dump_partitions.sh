#!/bin/bash

esp32_image_parser.py dump_partition factory_state.bin -partition otadata -output otadata.bin
esp32_image_parser.py dump_partition factory_state.bin -partition phy_init -output phy_init.bin
esp32_image_parser.py dump_partition factory_state.bin -partition ota_0 -output ota_0.bin
esp32_image_parser.py dump_partition factory_state.bin -partition ota_1 -output ota_1.bin
esp32_image_parser.py dump_partition factory_state.bin -partition nvs -output nvs.bin
esp32_image_parser.py dump_partition factory_state.bin -partition storage0 -output storage0.bin
esp32_image_parser.py dump_partition factory_state.bin -partition ktt -output ktt.bin

esp32_image_parser.py dump_nvs factory_state.bin -partition nvs -nvs_output_type json >> nvs.json