# sensors
Intro to component here

## Dependencies 
```bash
cd ~/software && git clone https://github.com/alfiTH/vl6180x_multi && pip3 install vl6180x_multi
pip3 install adafruit-circuitpython-tcs34725
```

## Configuration parameters
As any other component, *sensors* needs a configuration file to start. In
```
etc/config
```
you can find an example of a configuration file. We can find there the following lines:
```
EXAMPLE HERE
```

## Starting the component
To avoid changing the *config* file in the repository, we can copy it to the component's home directory, so changes will remain untouched by future git pulls:

```
cd <sensors's path> 
```
```
cp etc/config config
```

After editing the new config file we can run the component:

```
bin/sensors config
```
