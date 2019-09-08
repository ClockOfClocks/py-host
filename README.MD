# ClockOfClocks host controller


## Modbus protocol specification


### Get Calibration info

| FC    | Data Address | Number of registers | 
| :---: | :---: | --- |
| 3     | 1     | 1   |


Returns calibration status for both axises: 2 bytes.

calibration done for the 1-st axis = (result & 0xFF) > 0  
calibration done for the 2-nd axis = (result & 0xFF00) > 0  


### Calibrate and Sleep 


| FC    | Start Register Number | Number of registers | Data |
| :---: | :---: | --- | --- |
| 6     | 1 or 2 | 1   | Does not matter | 
| 6     | 4 or 8 | 1   | `uint16`: microseconds to sleep for one hand | 
| 6     | 12 (4 &#124; 8) | 2   | two `uint16` microseconds to sleep for each of the hands |

#### Start Register Number encoding:
_(Bit mask)_

1 — calibrate hour hand   
2 — calibrate minute hand  

4 — hour hand sleep  
8 — minute hand sleep  


### Move Hand

| FC    | Start Register Number | Number of registers | Data | Description | 
| :---: | :---: | --- | --- | --- |
| 16     | 1 or 2 with modifications | 2   | 2 bytes with speed and degree | Move one hand |
| 16     | 3  with modifications | 4   | 4 bytes with speed and degree | Move both hands |
 

#### Start Register Number encoding:
_(Bit mask)_

1 — move hour hand  
2 — move minute hand  
4 — hour hand relative=true  
8 — minute hand relative=true  


_I.e.:_ 
* To move minute hand relatively, (2 | 8 = 10) start register number have to be specified.
* To move both hands absolutely, (1 | 2 = 3) start register number have to be specified.

#### Data Payload

**int32**: degree to move, multiplied by 10 for storing decimal fraction (+/- 3276.7)  
**uint32**: speed of move, multiplied by 10 for storing decimal fraction (max 6553.5)

For both hands rotation used 2 times by 2 bytes consistently. 



