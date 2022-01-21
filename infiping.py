#!/usr/bin/env python3
# SPDX-License-Identifier: GPL-3.0-or-later
#
#    Infiping: pings a series of servers and logs the result in a csv file for analysis.
#    Copyright (C) 2022  Command_Prompt_Gamer
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with this program.  If not, see <https://www.gnu.org/licenses/>.
#

import subprocess
import time
import os.path
import os
import sys
import textwrap


def ping(address, filename, warn=False, minimumTimeUp=0, timeToWait=0):
    startTime = time.time()
    
    if not os.path.isfile(filename):  # If the file doesn't exist we create it. We are using CRLF to comply with the csv spec.
        with open(filename, "w", newline='\r\n') as file:
            file.write("timestamp,address,failed\n")

    if os.name == "nt":
        countIndicator = "-n"
    else:
        countIndicator = "-c"
    
    with open(filename, "a", newline="\r\n") as file:
        if subprocess.call("ping " + countIndicator + " 1 " + address, shell=True) == 0:  # subprocess.call() returns the exit code of the call and the ping commands exists with 0 if it succeeded, so we know the ping failed if the exit code is not 0.
            file.write(str(startTime) + "," + address + "," "0\n")
        else:
            if warn:
                with open(filename, "r") as readFile:
                    lines = readFile.readlines()
                
                for line in lines:
                    if line.endswith(",1\n"):
                        lastFail = line.split(",")[0]
                    
                try:  #  We have to see if lastFail exists, it won't exist if there was never a failure on record.
                    lastFail
                except NameError:
                    lastFail = 0  # We set it to zero so it will warn about the error in the first time (unless you go back in time to before minimumTimeUp after January 1st, 1970, 00:00:00 UTC 👀).
                
                if time.time() >= float(lastFail) + minimumTimeUp:  # We ring the bell if the last failure was more than minimumTimeUp ago, we don't ring it every time because it would keep ringing every timeToWait seconds if the network goes down.
                    print(textwrap.fill("\033[91mPing to " + address + " failed!\033[0m\a", os.get_terminal_size().columns))
                
            file.write(str(startTime) + "," + address + "," "1\n")

    timeToSleep = float(timeToWait) - (time.time() - startTime)
    if timeToSleep < 0:
        timeToSleep = 0
        
    time.sleep(timeToSleep)


if __name__ == "__main__":
    
    # Default settings, these will apply if they are not provided in the command.
    addresses = ["1.1.1.1", "1.0.0.1", "8.8.8.8", "8.8.4.4", "9.9.9.9", "149.112.112.112", "208.67.222.222", "208.67.220.220", "185.228.168.9", "185.228.169.9", "76.76.19.19", "76.223.122.150", "94.140.14.14", "94.140.15.15"]  # The default addresses to ping. These are all DNS servers that should be fine to ping a lot.
    filename = "ping.csv"  # The filename to export the ping results to.
    timeToWait = 10  # How long we should wait between each ping.
    warn = False  # Whether we should send a warning (both visual and auditive) when a ping fails.
    minimumTimeUp = 60  # How long it has to have passed since the last failure for the warning to be sent. This is used to avoid getting warned over and over again when the network goes down. For example, a time of 60 means that the network has to have been up for at least 60 seconds since the last failure for a new warning to be sent when it goes down again.

    args = sys.argv[1:]

    for iteration, option in enumerate(args):
        if option in ["-a", "--addresses"]:
            addresses = []
            if args[iteration + 1].startswith("["):
                
                end = False
                for argument in args[iteration + 1:]:
                        if argument != argument.removesuffix("]"):
                            addresses.append(argument.removesuffix("]"))
                            end = True
                        
                        argument = argument.removesuffix("]")
                        argument = argument.removeprefix("[")
                        argument = argument.removesuffix(",")
                        
                        if not end:
                            addresses.append(argument)

        if option in ["-o", "--output"]:
            filename = args[iteration + 1]

        if option in ["-t", "--time-to-wait"]:
            timeToWait = args[iteration + 1]

        if option in ["-w", "--warn"]:
            warn = True
        
        if option in ["-m", "--minimum-time-up"]:
            minimumTimeUp = args[iteration + 1]

        if option in ["-h", "--help", "h", "help"]:
            print(textwrap.fill("Infiping pings a series of servers and logs the result in a csv file for analysis.", os.get_terminal_size().columns))
            print()
            print(textwrap.fill("These are the usable options, note that all of them are optional and suitable values are used by default when they are not provided:"))
            print()
            print(textwrap.fill("-a or --addresses:", os.get_terminal_size().columns))
            print(textwrap.fill("Defines the list of addresses to be pinged.", os.get_terminal_size().columns, initial_indent="    ", subsequent_indent="    "))
            print(textwrap.fill("Default: many, see line 68 in the the source code for the list.", os.get_terminal_size().columns, initial_indent="    ", subsequent_indent="    "))
            print()
            print(textwrap.fill("-o or --output:", os.get_terminal_size().columns))
            print(textwrap.fill("Defines the file where the ping results should be exported to.", os.get_terminal_size().columns, initial_indent="    ", subsequent_indent="    "))
            print(textwrap.fill("Default: " + filename + ".", os.get_terminal_size().columns, initial_indent="    ", subsequent_indent="    "))
            print()
            print(textwrap.fill("-t or --time-to-wait:", os.get_terminal_size().columns))
            print(textwrap.fill("Defines the time between pings.", os.get_terminal_size().columns, initial_indent="    ", subsequent_indent="    "))
            print(textwrap.fill("Default: " + str(timeToWait) + " seconds.", os.get_terminal_size().columns, initial_indent="    ", subsequent_indent="    "))
            print()
            print(textwrap.fill("-w or --warn:", os.get_terminal_size().columns))
            print(textwrap.fill("Defines whether you should be notified when a ping fails.", os.get_terminal_size().columns, initial_indent="    ", subsequent_indent="    "))
            if warn:
                warnStatusName = "true."
            else:
                warnStatusName = "false."
            print(textwrap.fill("Default: " + warnStatusName, os.get_terminal_size().columns, initial_indent="    ", subsequent_indent="    "))
            print()
            print(textwrap.fill("-m or --minimum-time-up:", os.get_terminal_size().columns))
            print(textwrap.fill("Defines the minimum time the network has to have been up since the last ping failure for the network to be considered down again and a new warning issued.", os.get_terminal_size().columns, initial_indent="    ", subsequent_indent="    "))
            print(textwrap.fill("Default: " + str(minimumTimeUp) + " seconds.", os.get_terminal_size().columns, initial_indent="    ", subsequent_indent="    "))

            sys.exit()

    if os.name == "nt":  # Windows uses -n to indicate how many pings should be made, everything else uses -c.
        countIndicator = "-n"
    else:
        countIndicator = "-c"


    while True:
        for address in addresses:
            ping(address, filename, warn, minimumTimeUp, timeToWait)