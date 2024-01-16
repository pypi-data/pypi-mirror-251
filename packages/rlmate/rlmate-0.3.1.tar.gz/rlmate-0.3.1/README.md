# RLMate

Project under development. 

The RLMate is a package designed to take over parts of Reinforcement Learning that are needed frequently. 
It comes together with the command line tool 'Hermes'. 

The idea is to have a tool
- to organize RL tasks and carry out several scripts,
- to execute common RL tasks, e.g., plot training curves, 
- have commonly shared code as a python package instead of reimplementing it over and over again.  


## Installation
Simply install the current version with
* `pip install  rlmate`

Further instructions will be added when the package involves. 


## Installation

todo
## Command Line Tool

All available commands can also be seen by using the help function `hermes -h`

Available commands:
* ``exec -f file``: execute the specified Hermesfile. 
* ``exec -e command``: execute the specified command. __Not supported yet!__
* ``exec -n name``: give the execution file a name to make the results directory more human readable.
* ``create``: create an example Hermes files
* ``help command``: show a detailed help of the specified command.
* `-ho`: show help for hermes options used in .hermes files (also see below) 

### Settings
Settings in this context means something that is not set for a particular execution/hermesfile, but for the __git repository__ that is currently used. 
The settings are saved in the root if the repository in the ``.hermes_settings`` file. 
The current settings (with the default value if there is no settings file) are:
* `path_to_experiment ('./')`: specifies the path where to store the results of the experiment in. Takes the repository root as entry point.
* `threads (1)`: specifies how many of the specified jobs should be executed parallel.

The syntax is as follow: `setting:value` and only one setting should be specified per line.

### Hermes-options 
For each job, different Hermes options can be specified. Currently, these options are:
* `-ca file`: the `file` is copied to the experiment folder after the execution of the job.
* `-cb file`: the `file` is copied to the experiment folder before the execution of the job.
* `-ma file`: the `file` is moved to the experiment folder after the execution of the job.
* `-l/--log (True | False)`: if `True` the stdout and stderr of the job will not be printed to console, but stored in log files. Defaults to `True`.
* `-m`: if set, a telegram message will be sent to the chat_ids specified in the `.hermes_settings` file. 


### Hermesfile

The Hermesfile specifies the experiments that should be ran. 
Hermesfiles have the ending `.hermes`.
Each file is divided into 3 parts:

#### 1. PRE
In the PRE part of the Hermesfile, the settings can be adjustet *for the given Hermesfile only*.
So if you generally want to process the files by using two threads, and thereforce specified so in the `.hermes_settings` file, you can change this for the current hermesfile only by specifying it in the PRE section. 
This is done linewise per setting. 
The syntax is the same as for the settings file.  

#### 2. STD-H
Sometimes, some Hermes options should be applied to all jobs of the Hermes file. 
Hermes-options specified in the STD-H section will be applied to all jobs. 
The syntax is one Hermes-option per line with `-flag file`

#### 3. STD-E
Also, there sometimes are script arguments that should be applied to all jobs while just a few are about to be varied. 
Such arguments specified in the STD-E section will be applied to all jobs. 
The syntax in one argument per line, e.g. `-ne 100` or `-n`.

This standard arguments will be added _before_ the arguments specified in the exec lines. 
Note that this order may be important for your script. 
#### 4. EXEC
In this section the jobs are specified with the following syntax:
```
[[cmd],[Hermes-options]]
```
whereby the Hermes-options are separated by comma.
In each line, one job can be specified. 
All settings that should be saved automatically must be set in the cmd. 
### Storage

All files will be saved in the directory `experiments/script_name/uniqe_name`, where
* `script_name` is the name of the script specified in the job
* `unique_name` is the unique combination of date and time, commit number, and name that may have been specified with the `-n` flag

and the experiments directory will be created on the first call in the directory as specified in the settings. 

If during the execution of the script new files or directories will be created, they are automatically moved to the storage if they include the `unique_name`. 
How this name is given to the script will be specified in the next section. 

Additionally, in the future there will be an overview file giving detailed information about all the made experiments. 



### Script Compatibility
For your script to be compatible with Hermes, there are basically two things you need to consider:
1. All the parameters that should be saved must be specified by command line. 
If you want to save additional parameters, make sure to specify it by archiving the files by using the Hermes-options.
2. This is the only strong requirement: The first argument of the executed script must be the unique name, that is determined by Hermes. 
You must not do anything with that identifier except for saving additional files as specified in the Storage section.

