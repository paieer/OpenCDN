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
1. host: the host on which you like to run the application.
2. port: the port on which you like to run the application.
3. debug: Enable the debug mode (do not use it in production).
4. threaded: Every request would be running in own thread.
5. file_suffix_type: Use blacklist or whitelist mode.
6. whitelist (only active, if you use file_suffix_type whitelsit): Use list xy,xy,xy,xy.
7. blacklist (only active, if you use file_suffix_type blacklist): Use list xy,xy,xy,xy.
8. log_directory.
9. log_filename: The filename of the log file.
10. data_directory: the uploaded files would be saved here.
11. hash_algo: With this hash algo would be the file encrypting key encrypted.
12. max_file_bytes: The maximal file upload size.
13. random_key_length: The length of the random key, which been used to encrypt the file.
14. server_key: The files would be encrypted with this key partially (if you dont set it, it would be generated).
15. When you upload something, you get a response with the link to the file, which contains partially the basic_out_link.

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
