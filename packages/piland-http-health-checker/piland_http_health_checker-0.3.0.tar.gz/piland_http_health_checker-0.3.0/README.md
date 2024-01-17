# `piland-http-health-checker`

A CLI application to check the health of a set of HTTP endpoints from a YAML file using the Typer library.

* Reads a selected file with a list of HTTP endpoints in YAML format. 
* Tests the health of the endpoints every 15 seconds.
* Keeps track of the availability percentage of the HTTP domain names being monitored by the program.
* Logs the cumulative availability percentage for each domain to the console after the completion of each 15-second test cycle.


**Prerequisites**

* Python: 3.12


**Installation and Quickstart**

* Installing via PyPI

You can install this application using PyPI:
```console
$ pip install piland-http-health-checker
```

Then to run it, execute the following in the terminal:
```console
$ piland-http-health-checker run-program
```


**Using the Application**

1. Select the YAML file to load in the file dialog
2. The availablity percentage of the domain(s) will log to the console every 15 seconds
3. To exit the program, press 'ctrl + C'


**Usage**:

```console
$ piland-http-health-checker [OPTIONS] COMMAND [ARGS]...
```

**Options**:

* `--install-completion`: Install completion for the current shell.
* `--show-completion`: Show completion for the current shell, to copy it or customize the installation.
* `--help`: Show this message and exit.

**Commands**:

* `rick`: Do not run this command
* `run-program`: Runs program on a loop

## `piland-http-health-checker rick`

Do not run this command

**Usage**:

```console
$ piland-http-health-checker rick [OPTIONS]
```

**Options**:

* `--help`: Show this message and exit.

## `piland-http-health-checker run-program`

Runs program on a loop

**Usage**:

```console
$ piland-http-health-checker run-program [OPTIONS]
```

**Options**:

* `--help`: Show this message and exit.
