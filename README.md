# Infiping
Infiping pings a series of servers and logs the result to a csv file for analysis.

# Usage
You can simply run the python script and it will work, saving the results to ping.csv. However, you can set a couple of options by adding certain arguments to the execution of the script as described below.

## Options

### -a or --address
Defines the list of addresses to be pinged.
E.g. `[1.1.1.1, 1.0.0.1, 8.8.8.8, 8.8.4.4]`.  
The default option is a list with some DNS servers, see line 73 of [infiping.py](infiping.py) for the list.
### -o or --output:
Defines the file where the ping results should be exported to.  
Default: ping.csv.
### -t or --time-to-wait:
Defines the time between pings.  
Default: 10 seconds.
### -w or --warn:
Add this argument to get warned when a ping fails.
### -m or --minimum-time-up:
Defines the minimum time the network has to have been up since the last ping failure for the network to be considered down again and a new warning issued. Only applicable when the option above has been used.  
Default: 60 seconds.

## Help
You may run \`-h', \`--help', \`h', \`help' to get help inside the program.

# Interpreting the csv file
Each line in the csv file is a ping and its characteristics are defined by the rows. There are 3 rows: timestamp, address and failed.  
The timestamp is the timestamp in UNIX Time (how many seconds have passed since January 1, 1970, 00:00:00 UTC).  
The address is the address that was pinged in that specific ping.  
The failed value indicates whether the ping failed: 0 for success and 1 for failure.  

# Usage as a module
You may use this tool inside another python script by using the ping() function inside infiping after importing it.  
The ping function has 5 parameters: address, filename, minimumTimeUp, warn and timeToWait.

## address:
The address to be pinged (string).

## filename:
The csv file to export the result to (string or path-like object).

## warn:
Indicates whether a warning should be sent when a ping fails (boolean).  
Optional, the default is False.

## minimumTimeUp:
Indicates the minimum time in seconds the network has been up for a new warning to be issued (float or int).  
Optional, the default is 0 seconds.

## timeToWait:
How much time should the ping() function take to run. It will pause the script for the remaining time after running the ping, making the function take this parameter much time to run. This is useful when running repeated pings to make them equally spaced in time even with pings taking different amounts of time each (float or int).  
Optional, the default is 0 seconds.

# License
This program is free software: you can redistribute it and/or modify it under the terms of the GNU General Public License as published by the Free Software Foundation, either version 3 of the License, or (at your option) any later version. See [LICENSE](LICENSE), for more details.
