# Things to Test

## Test Order and Notes
1. [Testing if HUBs Can Be Flashed Back to Factory Config](#testing-if-hubs-can-be-flashed-back-to-factory-config)
2. [Testing of Default Test AP](#testing-of-default-test-ap)
3. [Testing of Custom AP](#testing-of-custom-ap)
4. [Testing if Hubs See All LORA Messages](#testing-if-hubs-see-all-lora-messages)
5. New Flash Dumps
    - Perform `factory reset` (via reset button)
    - Since hubs have connected to YoLink Servers, perform new flash dumps in case a firmware update was taken
6. [Testing of Custom gwConfig Without YoLink Activation](#testing-of-custom-gwconfig-without-yolink-activation)
    - If Step 6 passes, then local MQTT is possible without activation from YoLink first.
    - If Step 6 fails, then proceed with Step 7
7. [Testing of Custom gwConfig With YoLink Activation](#testing-of-custom-gwconfig-with-yolink-activation)
    - If Step 7 passes, then local MQTT is possible with activation from YoLink first
8. [Testing of Custom gwConfig With MQTT Broker as Bridge to YoLink](#testing-of-custom-gwconfig-with-mqtt-broker-as-bridge-to-yolink)
    - If Step 8 passes, then local MQTT is possible and without a second hub being required

## Testing if HUBs Can Be Flashed Back to Factory Config - PASS/Confirmed
### Notes
### Test Procedure
- Perform new flash dump from HUB1
- Compare new flash dump to original flash dump for differences
  - **Note:** there could have been a firmware update which would obscure findings
- Reflash `original_flash_dump`
- If reflash is successful, then assume restoring to a `factory state` is possible

## Testing of Default Test AP - PASS/Confirmed
### Notes
- From factory config, device appears to try to connect to `YoSmart_Test` AP
### Test Procedure
- Set up a `YoSmart_Test` AP on network with password found in nvs
- With serial logging connected, power up HUB
- Verify if device connects to `YoSmart_Test` AP
- Analyze serial log and "on the wire", determine next testing steps

## Testing of Custom AP
### Notes
- Previous testing should identify which HUB to use for this test
### Test Procedure
- Set up a new `custom_ap` on network
- Create new NVS/flash file containing `custom_ap` information
- Flash new NVS/flash file to HUB1
- With serial logging connected, power up HUB
- Verify if device connects to `custom_ap`
- Analyze serial log and "on the wire", determine next testing steps
- If findings are unremarkable, reattempt with HUB2

## Testing if Hubs See All LORA Messages - PASS/Confirmed
### Notes
- Perform only if restoring to `factory state` is possible
- Prior to beginning test, remove HUB1 from personal YoLink account
- Both hubs should start from `factory state`
- Serial logs from both hubs should be kept during this test for comparison later
### Test Procedure
- Create 2 new email accounts for testing (`email_1`, `email_2`)
- Create 2 new YoLink accounts for testing using newly created email accounts (`yolink_1`, `yolink_2`)
- Pair HUB1 to `yolink_1`
- Pair HUB2 to `yolink_2`
- Leaving both HUBs powered up and connected to network, add sensor to `yolink_1`
- Disconnect HUB1 from network/power
- See if HUB2 sees messages from sensor despite HUB1 being offline
- If HUB2 sees messages from sensor linked to `yolink_`
  - In YoLink App for `yolink_1`, monitor to see if sensor data is updated despite HUB1 being offline

## Testing of Custom gwConfig Without YoLink Activation
### Notes
- HUB must be receiving LORA messages
  - Possible issue with this could exist and be related to an activation procedure performed with YoLink servers
### Test Procedure
- Set up a local MQTT broker
- Create new NVS/flash file containing WiFi information and new `gwConfig`
  - Use the `gwConfig` python file to aid in creating the `gwConfigMD5` entry
  - Configure `gwConfig` to point to a local MQTT broker
- Flash new NVS/flash file to HUB2
- With serial logging connected, power up HUB2
- Analyze serial log and "on the wire", determine next testing steps
- Monitor MQTT broker logs to see if messages are being received

## Testing of Custom gwConfig With YoLink Activation
### Notes
- HUB must be receiving LORA messages
  - Possible issue with this could exist and be related to an activation procedure performed with YoLink servers
### Test Procedure
- Set up a local MQTT broker
- Connect HUB to a yolink account (`yolink_1` or `yolink_2`)
- Add a sensor to the account
- Create new NVS/flash file containing WiFi information and new `gwConfig`
  - Use the `gwConfig` python file to aid in creating the `gwConfigMD5` entry
  - Configure `gwConfig` to point to a local MQTT broker
- Flash new NVS/flash file to HUB2
- With serial logging connected, power up HUB2
- Analyze serial log and "on the wire", determine next testing steps
- Monitor MQTT broker logs to see if messages are being received

## Testing of Custom gwConfig With MQTT Broker as Bridge to YoLink
### Notes
- Should not matter which HUB to use
### Test Procedure
- Configure MQTT broker as bridge to YoLink servers (using information from stock `gwConfig`)
- Create new NVS/flash file containing WiFi information and new `gwConfig`
  - Use the `gwConfig` python file to aid in creating the `gwConfigMD5` entry
  - Configure `gwConfig` to point to a local MQTT broker
  - Configure with `custom_ap` information
- Flash new NVS/flash file to HUB
- With serial logging connected, power up HUB
- Analyze serial log and "on the wire", as well as MQTT broker logs to verify if messages are being received locally and forwarded to YoLink servers
- If bridging is working, attempt to add sensor via YoLink app
- If sensor is successfully added, stop MQTT broker from forwarding to YoLink servers and verify MQTT messages are still being received locally

# Theories
- Like with the Emporia Vue, does the hub use BLE to configure for initial config?
  - Could BLE be used to update the AP info and `gwConfig` info without soldering to the board?
- Hubs act as LORA->MQTT bridges for all LORA devices, regardless of registered account - CONFIRMED
