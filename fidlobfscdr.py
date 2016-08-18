#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Facebook idle status obfuscator for Libpurple via Pidgin/Finch

username = "zuck"
protocol_id = "prpl-facebook"

NAP_MIN = 15*60
NAP_MAX = 120*60

from pydbus import SessionBus
from time import sleep
from random import randint

bus = SessionBus()
purple = bus.get("im.pidgin.purple.PurpleService", "/im/pidgin/purple/PurpleObject")

def account_info(acc):
    #alias = purple.PurpleAccountGetAlias(acc)
    name = purple.PurpleAccountGetNameForDisplay(acc)
    user = purple.PurpleAccountGetUsername(acc)
    type = purple.PurpleAccountGetProtocolName(acc)
    id = purple.PurpleAccountGetProtocolId(acc)
    return name + " " + str(acc) + " " + user + " " + type + " " + id

acc_id = purple.PurpleAccountsFind(username, protocol_id)

if acc_id == 0:
    for acc in purple.PurpleAccountsGetAll():
        alias = purple.PurpleAccountGetAlias(acc)
        name = purple.PurpleAccountGetNameForDisplay(acc)
        user = purple.PurpleAccountGetUsername(acc)
        type = purple.PurpleAccountGetProtocolName(acc)
        id = purple.PurpleAccountGetProtocolId(acc)
        if user == username and id == protocol_id:
            acc_id = acc
            break
        print account_info(acc)

if acc_id != 0:
    print account_info(acc_id) + " OK!"

while acc_id != 0:
    nap = randint(NAP_MIN, NAP_MAX)
    print "nap " + str(nap)
    sleep(nap)
    if randint(0,1) == 0 and purple.PurpleAccountIsDisconnected(acc_id):
        purple.PurpleAccountConnect(acc_id)
        print "connected"
    elif purple.PurpleAccountIsConnected(acc_id):
        purple.PurpleAccountDisconnect(acc_id)
        print "disconnected"

print "no account '" + username + "' found"
