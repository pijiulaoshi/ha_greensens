# ha_greensens
 GreenSens plant sensors in Home Assistant
 
 Still a work in progress. Feel free to help out :)
 
 ## Configuration:
```
greensens:
  username: (req) [greensens username]
  password: (req) [greensens password]
  add_main_sensor: (optional, boolean, default = True) [Sets up a main sensor with all data per sensor]
  name_language: (optional, default = "LA", options = "LA", "EN", "DE") [ sets plant name language]
  monitored_conditions: (optional, default = all see below) [sets up a sensor per plant per condition]
    - temperature
    - moisture
    - illumination
```
