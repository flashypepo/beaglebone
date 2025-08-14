# Experiments on Beaglebone microcomputers

### Work-in-progress

[PocketBeagle-2](https://www.beagleboard.org/boards/pocketbeagle-2) placed upon
[Techlab cape](https://www.beagleboard.org/boards/techlab).


## PocketBeagle 2 Python Examples

The examples are based upon the original workshop `vsx-examples` Python examples. 
I've modified them from an application point of view.

The folder `pocketbeagle-2` provides [Python](https://www.python.org/) examples 
for PocketBeagle 2 on best effort basis. A TechLab cape is required to run the examples.

- `usrled.py`: example to control USR LED of the PocketBeagle. Replaced workshop `blinky.py`.
- `rgbled.py`: Examples to control the RGB-LED on the TechLab cape.
- `buttons.py`: Simple example to detect button release (or pressed which does not work yet).
- `light_sensor.py`: Simple example logging light sensor data.
- `seven_segment.py`: Simple example to demonstrate 2 seven segments on TechLab Cape.
- `tonal_buzzer.py`: Simple example to play Harry Potter melody on a buzzer.
- `heartbeat.py`: workshop example to control the trigger of a USR-LED.

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
              |rgb_led
                 hue.py
              heartbeat.py
              ... (other Python files)

```

## Initial Prep

Add some Python library folders to the path
I've added a specific pocketbeagle-2 `lib` folder, for libraries only for a PocketBeagle-2
and a common `libraries` folder, for libraries in common with Beaglebone Black.

```console
export PYTHONPATH=$HOME/projects/workshop/vsx-examples/pocketbeagle-2/lib:$PYTHONPATH
export PYTHONPATH=$HOME/projects/workshop/vsx-examples/libraries:$PYTHONPATH
```

## Run Examples

```console
cd ~/projects/workshop/vsx-examples/pocketbeagle-2/
python {example_name}.py
```

## History

- 2025-0814 PP - updated various Python files (rgbled.py, buttons.py)
- 2025-0805 PP - add Pocketbeagle-2 Python examples.
- 2025-0716 new setup