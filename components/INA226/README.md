# INA226
Intro to component here


## Dependencies 
Install pi_ina226
```bash
cd ~/software && git clone https://github.com/e71828/pi_ina226.git && pip install ./pi_ina226 && cd - 
```

## Configuration parameters
As any other component, *INA226* needs a configuration file to start. In
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
cd <INA226's path> 
```
```
cp etc/config config
```

After editing the new config file we can run the component:

```
bin/INA226 config
```
