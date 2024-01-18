#!/usr/bin/python3
#
# WeatherFlow listener
#
#  - this listens for WeatherFlow UDP broadcasts
#    and prints the decoded info to standard out (optionally)
#    or publishes the decoded data to MQTT (also optionally)
#
# IMPORTANT - this is tested versus v91 of the hub firmware
#             and coded versus the matching API docs at
#             https://weatherflow.github.io/SmartWeather/api/udp
#
#             While it 'might' work for different firmware,
#             your mileage might vary....
#
# this is updated to v114 of the firmware as documented in
#   https://weatherflow.github.io/SmartWeather/api/udp/v114/
#
# as of 2023-0127 threading has been removed for simplicity reasons
# so you 'might' miss a reading occasionally, but the intent of this
# utility is to be somewhat less perfect in never missing a broadcast
# and merely permitting you to diagnose more routine issues.
#
#----------------

"""

usage: python3 listener.py [-h] [-r] [-q] [-d] [-s] [-l LIMIT] [-x EXCLUDE] [-i] [-m] [-n]
                 [-w] [-b MQTT_BROKER] [-t MQTT_TOPIC]

optional arguments:
  -h, --help            show this help message and exit
  -r, --raw             print raw data to stddout
  -q, --quiet           print only the JSON to stdout (requires -r)
  -d, --decoded         print decoded data to stdout
  -s, --syslog          syslog unexpected data received
  -o, --output, --output DIRNAME
                        write output files in --raw mode to DIRNAME
  -l LIMIT, --limit LIMIT
                        limit obs type(s) processed
  -x EXCLUDE, --exclude EXCLUDE
                        exclude obs type(s) from being processed
  -i, --indent          indent raw data to stdout (requires -d)
  -m, --mqtt            publish to MQTT (one air/sky)
  -M, --multisensor     specify there are multiple air/sky/tempest present
  -n, --no_pub          report but do not publish to MQTT
  -b MQTT_BROKER, --mqtt_broker MQTT_BROKER
                        MQTT broker hostname
  -t MQTT_TOPIC, --mqtt_topic MQTT_TOPIC
                        MQTT topic to post to
  -a ADDRESS, --address ADDRESS
                        address to listen on
  --influxdb            publish to influxdb
  --influxdb_host INFLUXDB_HOST
                        hostname or ip of InfluxDb HTTP API
  --influxdb_port INFLUXDB_PORT
                        port of InfluxDb HTTP API
  --influxdb_user INFLUXDB_USER
                        InfluxDb username
  --influxdb_pass INFLUXDB_PASS
                        InfluxDb password
  --influxdb_db INFLUXDB_DB
                        InfluxDb database name
  --influxdb2           publish to InfluxDB v2
  --influxdb2_url INFLUXDB2_URL
                        InfluxDB v2 HTTP API root URL
  --influxdb2_org INFLUXDB2_ORG
                        InfluxDB v2 Organization
  --influxdb2_bucket INFLUXDB2_BUCKET
                        InfluxDB v2 Bucket
  --influxdb2_token INFLUXDB2_TOKEN
                        InfluxDB v2 Token
  --influxdb2_debug     Debug InfluxDB v2 publisher
  --mqtt_user MQTT_USER
                        MQTT username (if needed)
  --mqtt_pass MQTT_PASS
                        MQTT password (if MQTT_USER has a password)
  -v, --verbose         verbose output to watch the threads

for --limit, possibilities are:
   rapid_wind, obs_sky, obs_air, obs_st
   hub_status, device_status, evt_precip, evt_strike
   wind_debug, light_debug, rain_rebug

"""

#----------------
#
# compatibility notes:
#   - The v91 API uses 'timestamp' in one place and 'time_epoch' in all others
#     For consistency, this program uses 'timestamp' everywhere in decoded output

# uncomment for python2
from __future__ import print_function

import datetime
import json
import sys
import syslog
import time
import threading
import os
from socket import *

# python3 renamed it to 'queue'
try:
  from queue import Queue
except:
  from Queue import Queue

PY3 = sys.version_info[0] == 3

# weatherflow broadcasts on this port
MYPORT = 50222

# by default listen on all interfaces and addresses
ADDRESS = ''                       # supersede this with --address

# FQDN of the host to publish mqtt messages to
MQTT_HOST = "mqtt"                 # supersede this with --mqtt-broker
MQTT_TOPLEVEL_TOPIC = "wf"         # supersede this with --mqtt-topic
MQTT_CLIENT_ID = "weatherflow"
MQTT_PORT = 1883

# syslog routines (reused with thanks from weewx examples)
#   severity low->high:
#          DEBUG INFO WARNING ERROR CRITICAL
#

def logmsg(level, msg):
    syslog.syslog(level, '[wf-udp-listener]: %s' % msg)

def logdbg(msg):
    logmsg(syslog.LOG_DEBUG, msg)

def loginf(msg):
    logmsg(syslog.LOG_INFO, msg)

def logerr(msg):
    logmsg(syslog.LOG_ERR, msg)

#----------------
#
# process the various types of events or observations
#
# these routines are in the order shown in __main__ which
# should match up with the order in the WeatherFlow UDP API docs online
#

def process_evt_precip(data,args):
    if args.exclude and ("evt_precip" in args.exclude): return
    if args.limit and ("evt_precip" not in args.limit): return
    if args.raw: print_raw(data,args)

    evt_precip = {}
    serial_number = data["serial_number"]
                                                      # skip hub_sn
    evt_precip["timestamp"] = data["evt"][0]

    if args.decoded:
        print ("evt_precip     => ", end='')
        print (" ts  = " + str(evt_precip["timestamp"]), end='')
        print ('')

    topic = MQTT_TOPLEVEL_TOPIC + "/evt/precip"
    if args.mqtt_multisensor:
        topic = "sensors/" + serial_number + "/" + topic

    if args.mqtt:
        mqtt_publish(MQTT_HOST, topic, evt_precip, args)

    if args.influxdb:
        influxdb_publish(topic, evt_precip, args)

    if args.influxdb2:
        influxdb2_publish(topic, evt_precip, args)

    if args.verbose:
        print("finished publishing %s" % topic)

    return data

#----------------

def process_evt_strike(data,args):
    if args.exclude and ("evt_strike" in args.exclude): return
    if args.limit and ("evt_strike" not in args.limit): return
    if args.raw: print_raw(data,args)

    evt_strike = {}
    serial_number = data["serial_number"]
                                                      # skip hub_sn
    evt_strike["timestamp"] = data["evt"][0]
    evt_strike["distance"]  = data["evt"][1]          # km
    evt_strike["energy"]    = data["evt"][2]          # no units documented

    if args.decoded:
        print ("evt_strike     => ", end='')
        print (" ts  = "       + str(evt_strike["timestamp"]), end='')
        print (" distance  = " + str(evt_strike["distance"]), end='')
        print (" energy  = "   + str(evt_strike["energy"]), end='')
        print ('')

    topic = MQTT_TOPLEVEL_TOPIC + "/evt/strike"
    if args.mqtt_multisensor:
        topic = "sensors/" + serial_number + "/" + topic

    if args.mqtt:
        mqtt_publish(MQTT_HOST, topic, evt_strike, args)

    if args.influxdb:
        influxdb_publish(topic, evt_strike, args)

    if args.influxdb2:
        influxdb2_publish(topic, evt_strike, args)

    if args.verbose:
        print("finished publishing %s" % topic)

    return data

#----------------

def process_rapid_wind(data,args):
    if args.exclude and ("rapid_wind" in args.exclude): return
    if args.limit and ("rapid_wind" not in args.limit): return
    if args.raw: print_raw(data,args)

    rapid_wind = {}
    serial_number = data["serial_number"]
                                                      # skip hub_sn
    rapid_wind['timestamp']  = data["ob"][0]
    rapid_wind['speed']      = data["ob"][1]          # meters/second
    rapid_wind['direction']  = data["ob"][2]          # degrees

    if args.decoded:
        print ("rapid_wind     => ", end='')
        print (" ts  = " + str(rapid_wind['timestamp']), end='')
        print (" mps = " + str(rapid_wind['speed']), end='')
        print (" dir = " + str(rapid_wind['direction']), end='')
        print ('')

    topic = MQTT_TOPLEVEL_TOPIC + "/rapid_wind"
    if args.mqtt_multisensor:
        topic = "sensors/" + serial_number + "/" + topic

    if args.mqtt:
        mqtt_publish(MQTT_HOST, topic, rapid_wind, args)

    if args.influxdb:
        influxdb_publish(topic, rapid_wind, args)

    if args.influxdb2:
        influxdb2_publish(topic, rapid_wind, args)

    if args.verbose:
        print("finished publishing %s" % topic)

    return data

#----------------

def process_obs_air(data,args):
    if args.exclude and ("obs_air" in args.exclude): return
    if args.limit and ("obs_air" not in args.limit): return
    if args.raw: print_raw(data,args)

    obs_air = {}
    serial_number = data["serial_number"]
                                                                        # skip hub_sn
    obs_air["timestamp"]                     = data["obs"][0][0]
    obs_air["station_pressure"]              = data["obs"][0][1]        # MB
    obs_air["temperature"]                   = data["obs"][0][2]        # deg-C
    obs_air["relative_humidity"]             = data["obs"][0][3]        # %
    obs_air["lightning_strike_count"]        = data["obs"][0][4]
    obs_air["lightning_strike_avg_distance"] = data["obs"][0][5]        # km
    obs_air["battery"]                       = data["obs"][0][6]        # volts
    obs_air["report_interval"]               = data["obs"][0][7]        # minutes
    obs_air["firmware_revision"]             = data["firmware_revision"]

    if args.decoded:
        print ("obs_air        => ", end='')
        print (" ts  = "               + str(obs_air["timestamp"]), end='')
        print (" station_pressure = "  + str(obs_air["station_pressure"]), end='')
        print (" temperature = "       + str(obs_air["temperature"]), end='')
        print (" relative_humidity = " + str(obs_air["relative_humidity"]), end='')
        print (" lightning_strikes = " + str(obs_air["lightning_strike_count"]), end='')
        print (" lightning_avg_km  = " + str(obs_air["lightning_strike_avg_distance"]), end='')
        print ('')

    topic = MQTT_TOPLEVEL_TOPIC + "/obs_air"
    if args.mqtt_multisensor:
        topic = "sensors/" + serial_number + "/" + topic

    if args.mqtt:
        mqtt_publish(MQTT_HOST, topic, obs_air, args)

    if args.influxdb:
        influxdb_publish(topic, obs_air, args)

    if args.influxdb2:
        influxdb2_publish(topic, obs_air, args)

    if args.verbose:
        print("finished publishing %s" % topic)

    return data

#----------------

def process_obs_st(data,args):
    if args.exclude and ("obs_st" in args.exclude): return
    if args.limit and ("obs_st" not in args.limit): return
    if args.raw: print_raw(data,args)

    obs_st = {}
    serial_number = data["serial_number"]
                                                                         # skip hub_sn
    obs_st["timestamp"]                     = data["obs"][0][0]
    obs_st["wind_lull"]                     = data["obs"][0][1]          # meters/second min 3 sec sample
    obs_st["wind_avg"]                      = data["obs"][0][2]          # meters/second avg over report interval
    obs_st["wind_gust"]                     = data["obs"][0][3]          # meters_second max 3 sec sample
    obs_st["wind_direction"]                = data["obs"][0][4]          # degrees
    obs_st["wind_sample_interval"]          = data["obs"][0][5]          # seconds
    obs_st["station_pressure"]              = data["obs"][0][6]          # MB
    obs_st["temperature"]                   = data["obs"][0][7]          # deg-C
    obs_st["relative_humidity"]             = data["obs"][0][8]          # %
    obs_st["illuminance"]                   = data["obs"][0][9]          # lux
    obs_st["uv"]                            = data["obs"][0][10]         # index
    obs_st["solar_radiation"]               = data["obs"][0][11]         # W/m^2
    obs_st["rain_accumulated"]              = data["obs"][0][12]         # mm (in this reporting interval)
    obs_st["precipitation_type"]            = data["obs"][0][13]         # 0=none, 1=rain, 2=hail
    obs_st["lightning_strike_avg_distance"] = data["obs"][0][14]         # km
    obs_st["lightning_strike_count"]        = data["obs"][0][15]
    obs_st["battery"]                       = data["obs"][0][16]         # volts
    obs_st["report_interval"]               = data["obs"][0][17]         # minutes
    obs_st["firmware_revision"]             = data["firmware_revision"]

    if args.decoded:
        print ("obs_st        => ", end='')
        print (" timestamp  = "                     + str(obs_st["timestamp"]) ,  end='')
        print (" wind_lull  = "                     + str(obs_st["wind_lull"]) ,  end='')
        print (" wind_avg  = "                      + str(obs_st["wind_avg"]) ,  end='')
        print (" wind_gust  = "                     + str(obs_st["wind_gust"]) ,  end='')
        print (" wind_direction  = "                + str(obs_st["wind_direction"]) ,  end='')
        print (" wind_sample_interval  = "          + str(obs_st["wind_sample_interval"]) ,  end='')
        print (" station_pressure  = "              + str(obs_st["station_pressure"]) , end='')
        print (" temperature  = "                   + str(obs_st["temperature"]) , end='')
        print (" relative_humidity  = "             + str(obs_st["relative_humidity"]) , end='')
        print (" illuminance  = "                   + str(obs_st["illuminance"]) , end='')
        print (" uv  = "                            + str(obs_st["uv"]) , end='')
        print (" solar_radiation  = "               + str(obs_st["solar_radiation"]) , end='')
        print (" rain_accumulated  = "              + str(obs_st["rain_accumulated"]) , end='')
        print (" precipitation_type  = "            + str(obs_st["precipitation_type"]) , end='')
        print (" lightning_strike_avg_distance  = " + str(obs_st["lightning_strike_avg_distance"]) , end='')
        print (" lightning_strike_count  = "        + str(obs_st["lightning_strike_count"]) , end='')
        print (" battery = "                        + str(obs_st["battery"]) , end='')
        print (" report_interval = "                + str(obs_st["report_interval"]) , end='')
        print (" firmware_revision = "              + str(obs_st["firmware_revision"]) , end='')
        print ('')

    topic = MQTT_TOPLEVEL_TOPIC + "/obs_st"
    if args.mqtt_multisensor:
        topic = "sensors/" + serial_number + "/" + topic

    if args.mqtt:
        mqtt_publish(MQTT_HOST, topic, obs_st, args)

    if args.influxdb:
        influxdb_publish(topic, obs_st, args)

    if args.influxdb2:
        influxdb2_publish(topic, obs_st, args)

    if args.verbose:
        print("finished publishing %s" % topic)

    return data

#----------------

def process_obs_sky(data,args):
    if args.exclude and ("obs_sky" in args.exclude): return
    if args.limit and ("obs_sky" not in args.limit): return
    if args.raw: print_raw(data,args)

    obs_sky = {}
    serial_number = data["serial_number"]
                                                                     # skip hub_sn
    obs_sky["timestamp"]                   = data["obs"][0][0]
    obs_sky["illuminance"]                 = data["obs"][0][1]       # lux
    obs_sky["uv"]                          = data["obs"][0][2]       # index
    obs_sky["rain_accumulated"]            = data["obs"][0][3]       # mm (in this reporting interval)
    obs_sky["wind_lull"]                   = data["obs"][0][4]       # meters/second min 3 sec sample
    obs_sky["wind_avg"]                    = data["obs"][0][5]       # meters/second avg over report interval
    obs_sky["wind_gust"]                   = data["obs"][0][6]       # meters_second max 3 sec sample
    obs_sky["wind_direction"]              = data["obs"][0][7]       # degrees
    obs_sky["battery"]                     = data["obs"][0][8]       # volts
    obs_sky["report_interval"]             = data["obs"][0][9]       # minutes
    obs_sky["solar_radiation"]             = data["obs"][0][10]      # W/m^2
                                                                     # local_rain_day_accumulation does not work in v91 of their firmware
    obs_sky["precipitation_type"]          = data["obs"][0][12]      # 0=none, 1=rain, 2=hail
    obs_sky["wind_sample_interval"]        = data["obs"][0][13]      # seconds
    obs_sky["firmware_revision"]           = data["firmware_revision"]

    if args.decoded:
        print ("obs_sky        => ", end='')
        print (" serial_number  = "    + str(serial_number) ,  end='')
        print (" timestamp  = "        + str(obs_sky["timestamp"]) ,  end='')
        print (" uv  = "               + str(obs_sky["uv"]) , end='')
        print (" rain_accumulated  = " + str(obs_sky["rain_accumulated"]) , end='')
        print (" wind_lull = "         + str(obs_sky["wind_lull"]) , end='')
        print (" wind_avg = "          + str(obs_sky["wind_avg"]) , end='')
        print (" wind_gust = "         + str(obs_sky["wind_gust"]) , end='')
        print (" wind_direction = "    + str(obs_sky["wind_direction"]) , end='')
        print (" battery = "           + str(obs_sky["battery"]) , end='')
        print (" report_interval = "   + str(obs_sky["report_interval"]) , end='')
        print (" solar_radiation = "   + str(obs_sky["solar_radiation"]) , end='')
        print ('')

    topic = MQTT_TOPLEVEL_TOPIC + "/obs_sky"
    if args.mqtt_multisensor:
        topic = "sensors/" + serial_number + "/" + topic

    if args.mqtt:
        mqtt_publish(MQTT_HOST, topic, obs_sky, args)

    if args.influxdb:
        influxdb_publish(topic, obs_sky, args)

    if args.influxdb2:
        influxdb2_publish(topic, obs_sky, args)

    if args.verbose:
        print("finished publishing %s" % topic)

    return data

#----------------

def process_light_debug(data,args):
    if args.exclude and ("light_debug" in args.exclude): return
    if args.limit and ("light_debug" not in args.limit): return
    if args.raw: print_raw(data,args)

def process_wind_debug(data,args):
    if args.exclude and ("wind_debug" in args.exclude): return
    if args.limit and ("wind_debug" not in args.limit): return
    if args.raw: print_raw(data,args)

def process_rain_debug(data,args):
    if args.exclude and ("rain_debug" in args.exclude): return
    if args.limit and ("rain_debug" not in args.limit): return
    if args.raw: print_raw(data,args)

#----------------

def process_device_status(data,args):
    if args.exclude and ("device_status" in args.exclude): return
    if args.limit and ("device_status" not in args.limit): return
    if args.raw: print_raw(data,args)

    # both outside devices use the same status schema
    if "AR-" in data["serial_number"]:
            device_type = "air"
    elif "SK-" in data["serial_number"]:
            device_type = "sky"
    elif "ST-" in data["serial_number"]:
            device_type = "tempest"
    else:
            device_type = "unknown_type"

    device_status = {}
    serial_number = data["serial_number"]
                                                                   # skip hub_sn
    device_status["device"]            = device_type
    device_status["timestamp"]         = data["timestamp"]
    device_status["uptime"]            = data["uptime"]            # seconds
    device_status["voltage"]           = data["voltage"]           # volts
    device_status["firmware_revision"] = data["firmware_revision"]
    device_status["rssi"]              = data["rssi"]
    device_status["hub_rssi"]          = data["hub_rssi"]
    device_status["sensor_status"]     = data["sensor_status"]     # enumerated - see API for details
    device_status["debug"]             = data["debug"]             # 0=disabled, 1=enabled

    # sensor_status is an encoded enumeration
    #    0x00000000    all = sensors ok
    #    0x00000001    air = lightning failed
    #    0x00000002    air = lightning noise
    #    0x00000004    air = lightning disturber
    #    0x00000008    air = pressure failed
    #    0x00000010    air = temperature failed
    #    0x00000020    air = rh failed
    #    0x00000040    sky = wind failed
    #    0x00000080    sky = precip failed
    #    0x00000100    sky = light/uv failed

    if args.decoded:
        print ("device_status  => ", end='')
        print (" serial_number  = "    + str(serial_number) ,  end='')
        print (" device_type = "        + str(device_type), end='')
        print (" ts  = "                + str(device_status["timestamp"]), end='')
        print (" uptime  = "            + str(device_status["uptime"]), end='')
        print (" voltage  = "           + str(device_status["voltage"]), end='')
        print (" firmware_revision  = " + str(device_status["firmware_revision"]), end='')
        print (" rssi  = "              + str(device_status["rssi"]), end='')
        print (" hub_rssi  = "          + str(device_status["hub_rssi"]), end='')
        print (" sensor_status  = "     + str(device_status["sensor_status"]), end='')
        print (" debug  = "             + str(device_status["debug"]), end='')
        print ('')

    # construct the status topic to publish to
    # this one is unusual as two device_type(s) might be present

    topic = MQTT_TOPLEVEL_TOPIC + "/status/" + device_type
    if args.mqtt_multisensor:
        topic = "sensors/" + serial_number + "/" + topic

    if args.mqtt:
        mqtt_publish(MQTT_HOST, topic, device_status, args)

    if args.influxdb:
        influxdb_publish('device_status', device_status, args)

    if args.influxdb2:
        influxdb2_publish('device_status', device_status, args)

    if args.verbose:
        print("finished publishing %s" % topic)

    return data

#----------------

def process_hub_status(data,args):
    if args.exclude and ("hub_status" in args.exclude): return
    if args.limit and ("hub_status" not in args.limit): return
    if args.raw: print_raw(data,args)

    hub_status = {}
    serial_number = data["serial_number"]
    hub_status["device"]              = "hub"                      # (future use for this program)
    hub_status["firmware_revision"]   = int(data["firmware_revision"])
    hub_status["uptime"]              = data["uptime"]             # seconds
    hub_status["rssi"]                = data["rssi"]
    hub_status["timestamp"]           = data["timestamp"]
    hub_status["reset_flags"]         = data["reset_flags"]
    hub_status["seq"]                 = data["seq"]
    # skip - array    hub_status["fs"]                  = data["fs"]                 # internal use only
    hub_status["radio_stats_version"] = data["radio_stats"][0]
    hub_status["reboot_count"]        = data["radio_stats"][1]
    hub_status["i2c_bus_error_count"] = data["radio_stats"][2]
    hub_status["radio_status"]        = data["radio_stats"][3]     # 0=off, 1=on, 3=active
    # skip - array hub_status["mqtt_stats"]          = data["mqtt_stats"]         # internal use only

    # reset flags are a comma-delimited string with values:
    #   BOR = brownout reset
    #   PIN = PIN reset
    #   POR = power reset
    #   SFT = software reset
    #   WDG = watchdog reset
    #   WWD = window watchdog reset
    #   LPW = low-power reset

    if args.decoded:
        print ("hub_status     => ", end='')
        print (" ts  = "                + str(hub_status["timestamp"]), end='')
        print (" firmware_revision  = " + str(hub_status["firmware_revision"]), end='')
        print (" uptime  = "            + str(hub_status["uptime"]), end='')
        print (" rssi  = "              + str(hub_status["rssi"]), end='')
        print ('')

    topic = MQTT_TOPLEVEL_TOPIC + "/status_hub"
    if args.mqtt_multisensor:
        topic = "sensors/" + serial_number + "/" + topic

    if args.mqtt:
        mqtt_publish(MQTT_HOST, topic, hub_status, args)

    if args.influxdb:
        influxdb_publish(topic, hub_status, args)     # careful here, might need to hub_status.pop("foo", None) for arrays

    if args.influxdb2:
        influxdb2_publish(topic, hub_status, args)     # careful here, might need to hub_status.pop("foo", None) for arrays

    if args.verbose:
        print("finished publishing %s" % topic)

    return data

#----------------

def influxdb_publish(event, data, args):
    from influxdb import InfluxDBClient

    try:
        client = InfluxDBClient(host=args.influxdb_host,
                                port=args.influxdb_port,
                                username=args.influxdb_user,
                                password=args.influxdb_pass,
                                database=args.influxdb_db)
        payload = {}
        payload['measurement'] = event

        payload['time']   = data['timestamp']
        payload['fields'] = data

        if args.verbose:
            print ("publishing %s to influxdb [%s:%s]: %s" % (event,args.influxdb_host, args.influxdb_port, payload))

        # write_points() allows us to pass in a precision with the timestamp
        client.write_points([payload], time_precision='s')

    except Exception as e:
        print("Failed to connect to InfluxDB: %s" % e)
        print("  Payload was: %s" % payload)

#----------------

def influxdb2_publish(event, data, args):
    # influxdb_client supports InfluxDB backends 1.8/2.0+ - v1.8 includes a v2 API layer.
    from influxdb_client import InfluxDBClient, Point, WritePrecision
    from influxdb_client.client.write_api import SYNCHRONOUS

    if 'influxdb_client' not in sys.modules:
        print("you have not imported influxdb_client succcessfully")
        return

    try:
        client = InfluxDBClient(url=args.influxdb2_url,
                                    token=args.influxdb2_token,
                                    org=args.influxdb2_org,
                                    debug=args.influxdb2_debug)

        # WritePrecision.S necessary since we are using the report's timestamp, which is epoch in seconds.
        point = Point(event).tag("source", "weatherflow-udp-listener").time(data['timestamp'], WritePrecision.S)

        # add all keys / values to data point
        for key in data.keys():
            point.field(key, data[key])
            if args.influxdb2_debug:
                print("added field %s : %s" % (key, data[key]))

        if args.influxdb2_debug or args.verbose:
            print ("publishing %s to influxdb v2 [%s:%s]: %s" % (event,args.influxdb_host, args.influxdb_port, point))

        # write to API
        write_api = client.write_api(write_options=SYNCHRONOUS)
        write_api.write(bucket=args.influxdb2_bucket, record=point)

    except Exception as e:
        print("Failed to connect to InfluxDB: %s" % e)
        print("  Payload was: %s" % payload)

#----------------

def mqtt_publish(mqtt_host, mqtt_topic, data, args):
    import paho.mqtt.client  as mqtt
    import paho.mqtt.publish as publish
    if args.verbose:
        print ("publishing to mqtt://%s/%s" % (mqtt_host, mqtt_topic))

    if args.no_pub:
        print ("    ", json.dumps(data,sort_keys=True));

    if not args.no_pub:

        if args.mqtt_user:
            if args.mqtt_pass:
                AUTH = dict(username = args.mqtt_user, password = args.mqtt_pass)
            else:
                AUTH = dict(username = args.mqtt_user)
        else:
            AUTH = None

        broker_address=mqtt_host
        client_id=MQTT_CLIENT_ID
        topic=mqtt_topic
        payload=json.dumps(data,sort_keys=True)
        port=MQTT_PORT

        # ref: https://www.eclipse.org/paho/clients/python/docs/#single
        publish.single(
            topic,
            payload=payload,
            hostname=broker_address,
            client_id=client_id,
            port=port,
            auth=AUTH,
            protocol=mqtt.MQTTv311)

    return

#----------------
#
# if -q -r -o outdir this will save the observation
# to a file $outdir/$serial_number.$type
def print_raw(data,args):
        if args.raw:
            if args.indent:
                print ("")
                print (json.dumps(data,sort_keys=True,indent=2));
            else:
                if args.quiet:
                    if args.output:
                        try:
                            filename = args.output + "/" + data['serial_number'] + "." + data['type']
                            f = open(filename,"w")
                            f.write(json.dumps(data,sort_keys=True))
                            f.close()
                        except Exception as e:
                            print(e)
                    else:
                        print (json.dumps(data,sort_keys=True));
                else:
                    print ("    raw data: ", json.dumps(data,sort_keys=True));
            next

#---------

def report_it(data):

    #
    # this matches https://weatherflow.github.io/SmartWeather/api/udp/v91/
    # in the order shown on that page....
    #
    # yes tearing apart the pieces could be done 'cooler' via enumerating
    # a sensor map ala the WeatherflowUDP weewx driver, but lets go for
    # readability for the time being.....
    #

    if   data["type"] == "evt_precip":    process_evt_precip(data)
    elif data["type"] == "evt_strike":    process_evt_strike(data)
    elif data["type"] == "rapid_wind":    process_rapid_wind(data)
    elif data["type"] == "obs_air":       process_obs_air(data)
    elif data["type"] == "obs_sky":       process_obs_sky(data)
    elif data["type"] == "obs_st":        process_obs_st(data)
    elif data["type"] == "device_status": process_device_status(data)
    elif data["type"] == "hub_status":    process_hub_status(data)

    # --- uncomment to skip undocumented debug types ---
    elif data["type"] == "wind_debug":    process_wind_debug(data)
    elif data["type"] == "light_debug":   process_light_debug(data)
    elif data["type"] == "rain_debug":    process_rain_debug(data)

    else:
       # this catches 'lack of' a data["type"] in the data as well
       print ("ERROR: unknown data type in", data)
       if args.syslog:
         message = "unknown data type in " + json.dumps(data,sort_keys=True)
         loginf(message);

#---------


def main():
    # we set these globals away from defaults only if they are passed as arguments
    global ADDRESS, MQTT_HOST, MQTT_TOPLEVEL_TOPIC, MQTT_CLIENT_ID, MQTT_PORT

    import argparse

    # argument parsing is u.g.l.y it ain't got no alibi, it's ugly !
    parser = argparse.ArgumentParser(
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
for --limit, possibilities are:
   rapid_wind, obs_sky, obs_air, obs_st
   hub_status, device_status, evt_precip, evt_strike
       """,
    )

    parser.add_argument("-r", "--raw",     dest="raw",     action="store_true", help="print raw data to stddout")
    parser.add_argument("-q", "--quiet",   dest="quiet",   action="store_true", help="print only the JSON to stdout (requires -r)")
    parser.add_argument("-o", "--output",  dest="output",  action="store",      help="write STDOUT to output dir (requires -r -q)")
    parser.add_argument("-d", "--decoded", dest="decoded", action="store_true", help="print decoded data to stdout")
    parser.add_argument("-s", "--syslog",  dest="syslog",  action="store_true", help="syslog unexpected data received")
    parser.add_argument("-l", "--limit",   dest="limit",   action="store",      help="limit obs type(s) processed")
    parser.add_argument("-x", "--exclude", dest="exclude", action="store",      help="exclude obs type(s) from being processed")

    parser.add_argument("-i", "--indent",  dest="indent",  action="store_true", help="indent raw data to stdout (requires -d)")

    parser.add_argument("-m", "--mqtt",       dest="mqtt",             action="store_true", help="publish to MQTT")
    parser.add_argument("-M", "--multisensor", dest="mqtt_multisensor", action="store_true", help="specify there are multiple air/sky present")

    parser.add_argument("-n", "--no_pub",  dest="no_pub",  action="store_true", help="report but do not publish to MQTT")

    parser.add_argument("-b", "--mqtt_broker", dest="mqtt_broker", action="store", help="MQTT broker hostname")
    parser.add_argument("-t", "--mqtt_topic",  dest="mqtt_topic",  action="store", help="MQTT topic to post to")
    parser.add_argument("-a", "--address",     dest="address",     action="store", help="address to listen on")

    parser.add_argument("--influxdb",      dest="influxdb",      action="store_true",                                 help="publish to influxdb")
    parser.add_argument("--influxdb_host", dest="influxdb_host", action="store",      default="localhost",            help="hostname of InfluxDB HTTP API")
    parser.add_argument("--influxdb_port", dest="influxdb_port", action="store",      default=8086,         type=int, help="hostname of InfluxDB HTTP API")
    parser.add_argument("--influxdb_user", dest="influxdb_user", action="store",                                      help="InfluxDB username")
    parser.add_argument("--influxdb_pass", dest="influxdb_pass", action="store",                                      help="InfluxDB password")
    parser.add_argument("--influxdb_db",   dest="influxdb_db",   action="store",      default="smartweather",         help="InfluxDB database name")

    parser.add_argument("--influxdb2",        dest="influxdb2",    action="store_true", help="publish to InfluxDB v2")
    parser.add_argument("--influxdb2_url",    dest="influxdb2_url",    action="store", help="InfluxDB v2 HTTP API root URL", default="http://localhost:8086/")
    parser.add_argument("--influxdb2_org",    dest="influxdb2_org", action="store", help="InfluxDB v2 Organization")
    parser.add_argument("--influxdb2_bucket", dest="influxdb2_bucket", action="store", help="InfluxDB v2 Bucket")
    parser.add_argument("--influxdb2_token", dest="influxdb2_token", action="store", help="InfluxDB v2 Token")
    parser.add_argument("--influxdb2_debug", dest="influxdb2_debug", action="store_true", help="Debug InfluxDB v2 publisher")

    parser.add_argument("--mqtt_user", dest="mqtt_user", action="store", help="MQTT username (if needed)")
    parser.add_argument("--mqtt_pass", dest="mqtt_pass", action="store", help="MQTT password (if MQTT_USER has a password)")

    parser.add_argument("-v", "--verbose", dest="verbose", action="store_true", help="verbose mode - show threads")

    args = parser.parse_args()

    if (args.indent) and (not args.raw):
        print ("\n# exiting - must also specify --raw")
        parser.print_usage()
        print ()
        sys.exit(1)

    if (not args.mqtt) and (not args.decoded) and (not args.raw) and (not args.influxdb) and (not args.influxdb2):
        print ("\n#")
        print ("# exiting - must specify at least one option")
        print ("#           --raw, --decoded, --mqtt, --influxdb, --influxdb2")
        print ("#\n")
        parser.print_usage()
        print ()
        sys.exit(1)

    if args.mqtt_broker:
        MQTT_HOST = args.mqtt_broker

    if args.mqtt_topic:
        MQTT_TOPLEVEL_TOPIC = args.mqtt_topic

    if args.address:
        ADDRESS = args.address
    else:
        ADDRESS = ''

    if not args.quiet:
        print ("setting up socket - ", end='')
    s = socket(AF_INET, SOCK_DGRAM)
    s.setsockopt(SOL_SOCKET, SO_BROADCAST, 1)
    s.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
    s.bind((ADDRESS, MYPORT))
    if not args.quiet:
        print ("done")
        print ("listening for broadcasts..")
        if args.syslog:
            loginf("starting to process messages")

    while 1:

        msg=s.recvfrom(1024)
        data=json.loads(msg[0])      # this is the JSON payload

        #
        # this matches https://weatherflow.github.io/SmartWeather/api/udp/v91/
        # in the order shown on that page....
        #
        # yes tearing apart the pieces could be done 'cooler' via enumerating
        # a sensor map ala the WeatherflowUDP weewx driver, but lets go for
        # readability for the time being.....
        #

        if   data["type"] == "evt_precip":    process_evt_precip(data,args)
        elif data["type"] == "evt_strike":    process_evt_strike(data,args)
        elif data["type"] == "rapid_wind":    process_rapid_wind(data,args)
        elif data["type"] == "obs_air":       process_obs_air(data,args)
        elif data["type"] == "obs_sky":       process_obs_sky(data,args)
        elif data["type"] == "obs_st":        process_obs_st(data,args)
        elif data["type"] == "device_status": process_device_status(data,args)
        elif data["type"] == "hub_status":    process_hub_status(data,args)
        else:
           # this catches 'lack of' a data["type"] in the data as well
           print ("ERROR: unknown data type in", data)
           if args.syslog:
             message = "unknown data type in " + json.dumps(data,sort_keys=True)
             loginf(message);

        time.sleep(0.01)

if __name__ == "__main__":
    main()

