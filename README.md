# FRC2024


## Environment setup
* Download the latest Miniconda version on your computer with the following link (https://docs.conda.io/en/latest/miniconda.html)
* Open Anaconda Prompt
* Run the following commands to make sure everything is up-to-date:
```commandline
  conda config --add channels conda-forge
  conda config --set channel_priority strict
  conda update conda
  conda update python
```
* Run the following command to create an environment named "frc2024":
```commandline
  conda create -n frc2024 python=3.12
```
* Add the environment to the interpreter on PyCharm
* Run the following commands on the PyCharm terminal to install the requirements
```commandline
  pip install robotpy 
  python -m robotpy sync
```

(In a new[README.md](..%2FFRC2023%2FREADME.md) project, execute `python -m robotpy init` instead.)

## Execution

* Simulation : `python -m robotpy sim`
* Deployment : `python -m robotpy deploy`
* Run tests : `python -m robotpy test`

## Writing Conventions 
* All code must be written in the English language
* Follow PyCharm style recommendations
* Commit names must be clear and informative
* Progress must be tracked with GitHub Projects (https://github.com/orgs/Ultime5528/projects/8)
* File names use lowercase without spaces
* Class names use PascalCase
* Function names use camelCase
* Variable names use snake_case
* Function and command names start with an action verb (get, set, move, start, stop...)
* Commands and subsystems inherit from SafeCommand and SafeSubsystem
* Ports  
    * Must be added to ports.py
    * Respect the naming convention : "subsystem" _ "component type" _ "precision"
    * Example : drivetrain_motor_left
* Autoproperties 
  * Respect the naming convention : "variable type" _ "precision"
  * Example : speed_slow, height_max, distance_max
