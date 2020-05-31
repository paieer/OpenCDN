# OpenCDN
A upload-download sharing cdn, which encrypt all uploaded files.

## Installation

### Pipenv (recommend)
Install pipenv with: ``pip install pipenv``  
Install required packages with: ``pipenv install``
Run app with: ``pipenv run python run.py``

### Raw pip
Install required packages with: ``pip install -r requirements.txt``  
Run app with: ``python run.py``

### Docker
Run it with: ``docker up -d --build``  

## Configuration

The config file is located at ./opencdn.conf by default.  
For configuration help look at the wiki and the resources/config.py.

## CLI Help
```
usage: run.py [-h] [--reset-configuration] [--configuration-file CONFIGURATION_FILE] [-v] [--clear-all-logs] [--clear-today-log]

OpenCDN

optional arguments:
  -h, --help            show this help message and exit
  --reset-configuration
                        Resets the configuration file
  --configuration-file CONFIGURATION_FILE
  -v, --verbose         stdout info logs
  --clear-all-logs      Delete all files in the log directory
  --clear-today-log     Clear the today log file

```

## Contribution
If you have an idea, code it yourself and create a pull request or create a issue, thank you very much!  
