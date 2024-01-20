<br/>
<p align="center">
  <a href="https://github.com/ChrisBuilds/terminaltexteffects">
    <img src="https://github.com/ChrisBuilds/terminaltexteffects/assets/57874186/66388e57-e95e-4619-b804-1d8d7ebd124f" alt="TTE" width="80" height="80">
  </a>

  <h3 align="center">Terminal Text Effects</h3>

  <p align="center">
    Inline Visual Effects in the Terminal
    <br/>
    <br/>
  </p>
</p>

[![PyPI - Version](https://img.shields.io/pypi/v/terminaltexteffects?style=flat&color=green)](http://https://pypi.org/project/terminaltexteffects/ "![PyPI - Version](https://img.shields.io/pypi/v/terminaltexteffects?style=flat&color=green)")  ![PyPI - Python Version](https://img.shields.io/pypi/pyversions/terminaltexteffects) ![License](https://img.shields.io/github/license/ChrisBuilds/terminaltexteffects) 

## Table Of Contents

* [About](#tte)
* [Requirements](#requirements)
* [Installation](#installation)
* [Usage](#usage)
* [Options](#options)
* [Examples](#examples)
* [In-Development Preview](#in-development-preview)
* [Recent Changes](#recent-changes)
* [License](#license)


## TTE
![unstable_demo](https://github.com/ChrisBuilds/terminaltexteffects/assets/57874186/2e4b6e51-2b65-4765-a41c-92542981c77c)


TerminalTextEffects is a collection of visual effects that run inline in the terminal. The underlying visual effect framework supports the following:
* Xterm 256 color and RBG hex color support                 
* Color gradients                                           
* Runs inline, preserving terminal state and workflow       
* Dynamic character movement with motion easing             
* Dynamic animations with symbol and color changes and animation easing          
* Effect customization through command line arguments 

## Requirements

TerminalTextEffects is written in Python and does not require any 3rd party modules. Terminal interactions use standard ANSI terminal sequences and should work in most modern terminals.

Note: Windows Terminal performance is slow for some effects.

## Installation


```pip install terminaltexteffects```
OR
```pipx install terminaltexteffects```

## Usage
```cat your_text | tte <effect> [options]```

OR

``` cat your_text | python -m terminaltexteffects <effect> [options]```

* All effects support adjustable animation speed using the ```-a``` option.
* Use ```<effect> -h``` to view options for a specific effect, such as color or movement direction.
  * Ex: ```tte decrypt -h```

## Options
```
options:
  -h, --help            show this help message and exit
  --xterm-colors        Convert any colors specified in RBG hex to the closest XTerm-256 color.
  --no-color            Disable all colors in the effect.
  --tab-width TAB_WIDTH
                        Number of spaces to use for a tab character.
  --no-wrap             Disable wrapping of text.

Effect:
  Name of the effect to apply. Use <effect> -h for effect specific help.

  {blackhole,bouncyballs,bubbles,burn,columnslide,crumble,decrypt,errorcorrect,expand,fireworks,middleout,pour,rain,randomsequence,rings,rowmerge,rowslide,scattered,spray,swarm,test,unstable,verticalslice,vhstape,waves}
                        Available Effects
    blackhole           Characters are consumed by a black hole and explode outwards.
    bouncyballs         Characters are bouncy balls falling from the top of the output area.
    bubbles             Characters are formed into bubbles that float down and pop.
    burn                Burns vertically in the output area.
    columnslide         Slides each column into place from the outside to the middle.
    crumble             Characters lose color and crumble into dust, vacuumed up, and reformed.
    decrypt             Display a movie style decryption effect.
    errorcorrect        Some characters start in the wrong position and are corrected in sequence.
    expand              Expands the text from a single point.
    fireworks           Characters launch and explode like fireworks and fall into place.
    middleout           Text expands in a single row or column in the middle of the output area then
                        out.
    pour                Pours the characters into position from the given direction.
    rain                Rain characters from the top of the output area.
    randomsequence      Prints the input data in a random sequence.
    rings               Characters are dispersed and form into spinning rings.
    rowmerge            Merges rows of characters.
    rowslide            Slides each row into place.
    scattered           Move the characters into place from random starting locations.
    spray               Draws the characters spawning at varying rates from a single point.
    swarm               Characters are grouped into swarms and move around the terminal before settling
                        into position.
    test                effect_description
    unstable            Spawn characters jumbled, explode them to the edge of the output area, then
                        reassemble them in the correct layout.
    verticalslice       Slices the input in half vertically and slides it into place from opposite
                        directions.
    vhstape             Lines of characters glitch left and right and lose detail like an old VHS tape.
    waves               Waves travel across the terminal leaving behind the characters.

Ex: ls -a | python -m terminaltexteffects --xterm-colors decrypt -a 0.002 --ciphertext-color 00ff00
--plaintext-color ff0000 --final-color 0000ff
```


## Examples
#### Fireworks
![fireworks_demo](https://github.com/ChrisBuilds/terminaltexteffects/assets/57874186/e3788e25-758b-43e1-827f-42066fb29f91)

#### Rain
![rain_demo](https://github.com/ChrisBuilds/terminaltexteffects/assets/57874186/ed94a21f-503d-46f3-8510-7a1e83b28314)

#### Decrypt
![decrypt_demo](https://github.com/ChrisBuilds/terminaltexteffects/assets/57874186/586224f3-6a03-40ae-bdcf-067a6c96cbb5)

#### Spray
![spray_demo](https://github.com/ChrisBuilds/terminaltexteffects/assets/57874186/d39b4caa-7393-4357-8e27-b0ef9dce756b)

#### Scattered
![scattered_demo](https://github.com/ChrisBuilds/terminaltexteffects/assets/57874186/ddcf3c65-a91b-4e42-84fc-0c2508a85be5)

#### Expand
![expand_demo](https://github.com/ChrisBuilds/terminaltexteffects/assets/57874186/9b319e77-d2b7-489e-b59c-c87277ea1285)

#### Burn
![burn_demo](https://github.com/ChrisBuilds/terminaltexteffects/assets/57874186/ddc8ca36-4157-448b-b10d-573f108361c7)

#### Pour
![pour_demo](https://github.com/ChrisBuilds/terminaltexteffects/assets/57874186/d5b827a5-3267-47ad-88c7-6fb0b2dbb478)

#### Rowslide
![rowslide_demo](https://github.com/ChrisBuilds/terminaltexteffects/assets/57874186/fc62bbe3-d75f-4757-b1ef-c14abff2666b)

#### Rowmerge
![rowmerge_demo](https://github.com/ChrisBuilds/terminaltexteffects/assets/57874186/5cd4d5a1-e82d-42ed-b91c-6ac8061cab44)

#### Columnslide
![columnslide_demo](https://github.com/ChrisBuilds/terminaltexteffects/assets/57874186/f2ecdc42-415d-47d3-889d-8e8993657b8f)

#### Randomsequence
![randomsequence_demo](https://github.com/ChrisBuilds/terminaltexteffects/assets/57874186/8ee83d75-6c22-4c0b-8f96-a12301d7a4eb)

#### Verticalslice
![verticalslice_demo](https://github.com/ChrisBuilds/terminaltexteffects/assets/57874186/237e36c5-cb4e-4866-9a33-b7f27a2907dc)

#### Unstable
![unstable_demo](https://github.com/ChrisBuilds/terminaltexteffects/assets/57874186/2e4b6e51-2b65-4765-a41c-92542981c77c)

#### Bubbles
![bubbles_demo](https://github.com/ChrisBuilds/terminaltexteffects/assets/57874186/1ae892fb-0525-4308-8e0b-382e7c079cb2)

#### Bouncyballs
![bouncyballs_demo](https://github.com/ChrisBuilds/terminaltexteffects/assets/57874186/bb62112c-a6b7-466f-a7c8-ee66f528616b)

#### Middleout
![middleout_demo](https://github.com/ChrisBuilds/terminaltexteffects/assets/57874186/a69d4164-851e-4668-b2d0-8ee08e2dc5e3)

#### Errorcorrect
![errorcorrect_demo](https://github.com/ChrisBuilds/terminaltexteffects/assets/57874186/7e63d3f0-6e7f-4145-9886-fd54633896be)

#### Waves
![waves_demo](https://github.com/ChrisBuilds/terminaltexteffects/assets/57874186/ed057ac5-4cbb-4f8b-a47b-255574614965)

#### Blackhole
![blackhole_demo](https://github.com/ChrisBuilds/terminaltexteffects/assets/57874186/e8c9a3d5-6160-4cdb-9f3b-dc2d8a6a1a7f)

#### Swarm
![swarm_demo](https://github.com/ChrisBuilds/terminaltexteffects/assets/57874186/133a3e7d-b493-48c3-ace3-3848c89e6e39)

#### Crumble
![crumble_demo](https://github.com/ChrisBuilds/terminaltexteffects/assets/57874186/b052ff86-2920-4067-8a47-2713c43257cc)

#### Rings
![rings_demo](https://github.com/ChrisBuilds/terminaltexteffects/assets/57874186/2d97ba47-bf85-4727-9257-45a5b2a9dddd)

#### VHStape
![vhstape_demo](https://github.com/ChrisBuilds/terminaltexteffects/assets/57874186/ff11e292-4bfd-4989-ab81-1a624b2c0822)


## In-Development Preview
Any effects shown below are in development and will be available in the next release.


## Recent Changes

## 0.5.0

### New Features
 * New effect, Vhstape. Lines of characters glitch left and right and lose detail like an old VHS tape.
 * New effect, Crumble. Characters lose color and fall as dust before being vacuumed up and rebuilt.
 * New effect, Rings. Characters are dispersed throughout the output area and form into spinning rings.
 * motion.Motion.chain_paths(list[Paths]) will automatically register Paths with the EventHandler to create
   a chain of paths. Looping is supported.
 * motion.Motion.find_coords_in_rect() will return a random selection of coordinates within a rectangular area. This is faster than using
   find_coords_in_circle() and should be used when the shape of the search area isn't important.
 * Terminal.OutputArea.coord_in_output_area() can be used to determine if a Coord is in the output area.
 * Paths have replaced Waypoints as the motion target specification object. Paths group Waypoints together and allow for easing
   motion and animations across an arbitrary number of Waypoints. Single Waypoint Paths are supported and function the same as
   Waypoints did previously. Paths can be looped with the loop argument. 
 * Quadratic and Cubic bezier curves are supported. Control points are specified in the Waypoint object signature. When a control point
   is specified, motion will be curved from the prior Waypoint to the Waypoint with the control point, using the control point
   to determine the curve. Curves are supported within Paths.
 * New EventHandler.Event PATH_HOLDING is triggered when a Path enters the holding state.
 * New EventHandler.Action SET_CHARACTER_ACTIVATION_STATE can be used to modify the character activation state based on events.
 * New EventHandler.Action SET_COORDINATE can be used to set the character's current_coordinate attribute.
 * Paths have a layer attribute that can be used to automatically adjust the character's layer when the Path is activated.
   Has no effect when Path.layer is None, defaults to None.
 * New EventHandler.Events SEGMENT_ENTERED and SEGMENT_EXITED. These events are triggered when a character enters or exits a segment
   in a Path. The segment is specified using the end Waypoint of the segment. These events will only be called one time for each run
   through the Path. Looping Paths will reset these events to be called again. 


### Changes
 * graphics.Animation.random_color() is now a static method.
 * motion.Motion.find_coords_in_circle() now generates 7*radius coords in each inner-circle.
 * BlackholeEffect uses chain_paths() and benefits from better circle support for a much improved blackhole animation.
 * BlackholeEffect singularity Paths are curved towards center lines.
 * EventHandler.Event.WAYPOINT_REACHED removed and split into two events, PATH_HOLDING and PATH_COMPLETE.
 * EventHandler.Event.PATH_COMPLETE is triggered when the final Path Waypoint is reached AND holding time reaches 0.
 * Fireworks effect uses Paths and curves to create a more realistic firework explosion.
 * Crumble effect uses control points to create a curved vacuuming phase.
 * graphics.Gradient accepts an arbitrary number of color stops. The number of steps applies between each color stop.
 * motion.find_coords_in_circle() and motion.find_coords_in_rect() no longer take a num_points argument. All points in the area are returned.

### Bug Fixes
 * Fixed looping animations when synced to Path not resetting properly.

## License

Distributed under the MIT License. See [LICENSE](https://github.com/ChrisBuilds/terminaltexteffects/blob/main/LICENSE.md) for more information.
