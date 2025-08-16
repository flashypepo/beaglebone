# Experiments on Beaglebone microcomputers

### Work-in-progress

[PocketBeagle-2](https://www.beagleboard.org/boards/pocketbeagle-2) placed upon
[Techlab cape](https://www.beagleboard.org/boards/techlab).


## PocketBeagle 2 Python Examples

The examples are based upon the original workshop `vsx-examples` for PocketBeagle-2 and the Techlab cape, which can be found on 
[Techlab workshop PocketBeagle-2](https://github.com/beagleboard/vsx-examples/tree/main/PocketBeagle-2),
including examples in another language [Rust](https://www.rust-lang.org/).

I've modified the Python examples into object oriented code (classes), add exception handling and main execution so the source files can be used in `import` - see `techlabcape.py`.

The folder `pocketbeagle-2` provides [Python](https://www.python.org/) examples 
for PocketBeagle 2 on best effort basis. A TechLab cape is required to run the examples.

- `usrled.py`: example to control USR LED of the PocketBeagle. Replaced workshop `blinky.py`.
- `rgbled.py`: Examples to control the RGB-LED on the TechLab cape.
- `buttons.py`: Simple example to detect button release (or pressed which does not work yet).
- `light_sensor.py`: Simple example logging light sensor data.
- `seven_segment.py`: Simple example to demonstrate 2 seven segments on TechLab Cape.
- `buzzer.py`: Simple example to play Harry Potter melody on a buzzer. Replaced workshop `tonal_buzzer.py`.
- `heartbeat.py`: workshop example to control the trigger of a USR-LED.
- `techlabcape.py`: a simple `asyncio` example for most of the devices on the Techlab cape (**work in progress**)


## My Code tree setup

```console
~/projects
  | workshop
       | vsx-examples
          | libraries
              sysfs.py
              chardev.py
              notes.py
          | pocketbeagle-2
             |lib
                 libraries specific for Pocketbeagle-2 (currently empty)
              Python sourcecode examples
              README-files
              techlabcape.py - an examples running most of the devices on the Techlab Cape
```


## Initial Prep

Add some Python library folders to the Python path.
I've added a specific pocketbeagle-2 `lib` folder, for libraries only for a PocketBeagle-2
and a common `libraries` folder, for libraries in common with Beaglebone Black.

##### Pocketbeagle-2
Add following to `.bashrc` or `.bash_aliases`:
```console
export PYTHONPATH=$HOME/projects/workshop/vsx-examples/pocketbeagle-2/lib:$PYTHONPATH
export PYTHONPATH=$HOME/projects/workshop/vsx-examples/libraries:$PYTHONPATH
```

##### Beaglebone Black
Add following to `.bashrc` or `.bash_aliases`:
```console
export PYTHONPATH=$HOME/projects/workshop/vsx-examples/beaglebone-black/lib:$PYTHONPATH
export PYTHONPATH=$HOME/projects/workshop/vsx-examples/libraries:$PYTHONPATH
```


## Run Examples

```console
cd ~/projects/workshop/vsx-examples/pocketbeagle-2/
python {example_name}.py
```


## History

- 2025-0816 PP - updated code tree setup, Python codefiles, add `techlabcape.py`
- 2025-0814 PP - updated various Python files (`rgbled.py`, `buttons.py`)
- 2025-0805 PP - add Pocketbeagle-2 Python examples.
- 2025-0716 new setup
