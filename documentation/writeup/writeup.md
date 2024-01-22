# Reverse Engineering of YoLink Hub

# Reason
- Solar Flood Lights
  - _use IR remote to control_
  - _may eventyally hardwire_

# How to control from Home Assistant?
## Options
**WiFi IR Blaster**
- Not enough range
- Running WiFi back there would be expensive

**BLE IR blaster**
- Not enough range

**433Mhz IR blaster**
- DIY Solution
  - Doubted ability to build a waterproof DIY solution

**Need something waterproof with long range, is battery powered, and can be controlled locally with Home Assistant**

# Enter YoLink
## Benefits
- Long Range (1/4 mile)
- Battery Powered
  - Long Battery Life
- Have an IR blaster (May or may not be waterproof)
- Additional Sensor Types
  - Vibration
    - Monitor train activity
  - Motion
    - Perimeter Alarm
    - Animal Life
    - Camera Triggering
  
## Downsides
- YoLink App/Cloud
  - No Local Control
  - Home Assistant integration relies on their cloud

# Hardware Teardown
## Hubs
| Nickname    | Top                                        | Bottom                                        |
|:------------|:------------------------------------------:|:---------------------------------------------:|
| ns_hub_mini |![P1603_M_V1.0](images/P1603_M_V1.0/top.jpg)|![P1603_M_V1.0](images/P1603_M_V1.0/bottom.jpg)|
| ns_hub_big  |![P1603_V2.4](images/P1603_V2.4/top.jpg)    |![P1603_V2.4](images/P1603_V2.4/bottom.jpg)    |
| s_hub       |![TBD](images/TBD/top.jpg)                  |![TBD](images/TBD/bottom.jpg)                  |

### Non-Speaker Hubs
- For ease of reference, the hubs are given nicknames
- Analysis will be done on ns_hub_mini
- _smaller hub looks to be a refinement and more compact_
- _get board revs from pics_

- Chips/Part Numbers of Interest
  - **esp32-wroom-32**
    - _get pic_
  - **llcc68**
    - _get pic of 'module'_
    - semtech
    - similar to SX126x/SX127x
    - _later call out the strings output indicating hal file_
    - _looks to be COTS module with balun and modulation circuitry_
    - Comms w/ esp32 over SPI
- _include external/internal pics_

### Speaker Hub
- Not purchased yet
- _get info from FCC registration_
  - _include link_
- _no eth_

All hubs appear to be the same design, albeit more compact and with some components present in some hubs and not others. Notably, the speakerhub does not have ethernet connectivity. It is likely that the code running on the hubs are the same.
- _verify the software is the same_

## Sensors
- _get pics of some sensor internals_
- _show the YL09 chip_
  - Find some documentation of the YL09 chip
  - Uses YoLink branded chip
    - Based on semtech STM w/ LoRa integrated chip

# Reverse Engineering and Understanding of YoLink's Architecture
## Hardware investigation
### Debug headers
  - 1.27mm spacing
  - VCC(3.3v), GND, RX, TX, EN?, GPIO0?
    - Probed via continuity
    - Eventually bought logic analyzer which would have been easier
  - _include pics of debug header_

### Serial Logs
- Seems pretty verbose
  - Clearly indicates the `esp-idf` version as `3.2-dirty`
  - Initial boot process (from factory) appears to be:
    - Start ethernet interface and broadcast an AP
    - If ethernet is UP
      - Attempt dhcp
      - If dhcp succeeds
        - Get configuration from api.yolink.com
      - ElseIf DHCP fails
        - Continue with wifi setup
    - ElseIf ethernet is DOWN
      - Wait for device to connect to WiFi AP
      - Once a device connects, start web server and wait for WiFi credentials
      - Once WiFi credentials are received, attempt to connect to specified WiFi AP
      - If connection is unsuccessful
        - Restart broadcasting AP and repeat
      - ElseIf connection is successful
        - Get configuration from api.yolink.com
    - Once configuration is received from api.yolink.com, register with api.yolink.com MQTT server
    - Once registered with api.yolink.com MQTT, begin listening for LoRa messages
    - Once a LoRa message is received, forward it to api.yolink.com MQTT
      - api.yolink.com MQTT appears to respond with ACK message that may or may not be forwarded to reporting sensor via LoRa
  - Hub appears to send ALL LoRa messages via MQTT
    - Meaning that if a sensor that belongs to someone else's account sends a LoRa message, a hub that is not registered to that user still forwards the message to YoLink's servers. 
      - This could be beneficial as it could allow a hub to receive all LoRa traffic without needing to be registered (more investigation needed)
  - MQTT
    - YoLink's MQTT server appears to use some form of authentication (password)
  - Hub gets a "configuration" from a URL that appears to be unauthenticated and appears to be generated from the UUID/SN of the hub
    - Potential to host a local webserver where the hub gets this config from
      - Only thing here is to trick the hub to look at local server instead of yolink's for the config url
        - Would require arp poisoning/DNS cache poisoning, OR modifying the firmware
          - Local server might need to implement some logic to reply with ACK message as seen in some of the serial logs

## Flash Dumping

### Flash Dump Analysis
- Strings
  - Indicated mqtt
  - Line indicating `SX126x hal`
    - `Show image of terminal line showing this`
  - `api.yolink.com`
    - Yolink's URL appears 4 times in flash dump
    - Modifying flash might trip security mechanisms, thus making a local server mechanism possibly preferable
- Binwalk
  - Binwalk reveals mostly nothing of note
    - Some linux paths
    - Some Encryption related strings
- _Look for how to analyze esp32 flash dump_
  - _**cite multi-article on loading esp32 into ghidra**_
  - esp32-flash-loader (ghidra)
  - esp32-flash-parser (command line, dump partitions)
- Ghidra
  - Initial load not promising
  - Found article with esp32-flash-loader, esp32-flash-parser, etc.
  - Cloned repo's
    - Found that repo's needed more work
    - Found PR for xtensa that was stale
    - Describe method for combining forks
    - Describe work involved for addressing feedback in stale PR
    - Link new PR that is ours and pending inclusion
  - Describe function ID
    - Go down the rabit hole of building esp-idf
      - Link repo
    - Go down rabit hole of rizzo signatures
      - Link repo
  - Describe ghidra data types
    - Go down rabit hole of building esp-idf
      - Link repo
    - Go down rabit hole of generating gdt's
      - Link repo
  - Go through process of loading everything into ghidra to get a pretty good start for reversing dump
  - Talk about SVD loader and multiple addresses for peripherals
  - Talk overall about the work done to improve the tools for analyzing esp32 images


# Brain Dump
- Need to re-create repo with only necessary files?
- Need to include images
  - Terminal output lines from strings
  - Board pictures
    - _in progress_
  - Debug pictures
- Need to separate analysis portion to indicate which hub/process (large hub first, then smaller hub)

- ~~Need to buy speaker hub~~ ORDERED

- Need to include links to
  - Blog specifying ghidra and loading esp32
  - Amazon link to products?
- Mention products used (Serial interface, jtag interface, etc.)
- Need to get board revisions from pictures
- Need to get model numbers (from pics or elsewhere)
- Need pics of hubs/sensors from outside (before opening them up)
- Include commands used (for dumping flash, strings, binwalk, etc)
- Talk about trying to find the hal.c file
- Talk about OpenMQTTGateway
- Talk about heltec and RNode for monitoring lora traffic
- Talk about esphome
  - Mention flauviut tutorial about emporia vue 2
- 


# Other stuff
Use this for MITM of yolink hub
- https://www.dinofizzotti.com/blog/2022-04-24-running-a-man-in-the-middle-proxy-on-a-raspberry-pi-4/