import argparse

import terminaltexteffects.utils.argtypes as argtypes
from terminaltexteffects.base_character import EffectCharacter, EventHandler
from terminaltexteffects.utils.terminal import Terminal
from terminaltexteffects.utils import graphics, motion, argtypes, easing


def add_arguments(subparsers: argparse._SubParsersAction) -> None:
    """Adds arguments to the subparser.

    Args:
        subparser (argparse._SubParsersAction): subparser to add arguments to
    """
    effect_parser = subparsers.add_parser(
        "effect_name",
        formatter_class=argtypes.CustomFormatter,
        help="effect_description",
        description="effect_description",
        epilog=f"""{argtypes.EASING_EPILOG}

Example: effect_example""",
    )
    effect_parser.set_defaults(effect_class=NamedEffect)
    effect_parser.add_argument(
        "-a",
        "--animation-rate",
        type=argtypes.valid_animationrate,
        default=0.01,
        help="Minimum time, in seconds, between animation steps. This value does not normally need to be modified. Use this to increase the playback speed of all aspects of the effect. This will have no impact beyond a certain lower threshold due to the processing speed of your device.",
    )
    effect_parser.add_argument(
        "--color-single",
        type=argtypes.valid_color,
        default=0,
        metavar="(XTerm [0-255] OR RGB Hex [000000-ffffff])",
        help="Color for the ___.",
    )
    effect_parser.add_argument(
        "--color-list",
        type=argtypes.valid_color,
        nargs="*",
        default=0,
        metavar="(XTerm [0-255] OR RGB Hex [000000-ffffff])",
        help="Space separated, unquoted, list of colors for the ___.",
    )
    effect_parser.add_argument(
        "--final-color",
        type=argtypes.valid_color,
        default="ffffff",
        metavar="(XTerm [0-255] OR RGB Hex [000000-ffffff])",
        help="Color for the final character.",
    )
    effect_parser.add_argument(
        "--movement-speed",
        type=argtypes.valid_speed,
        default=1,
        metavar="(float > 0)",
        help="Speed of the ___. Note: Speed effects the number of steps in the easing function. Adjust speed and animation rate separately to fine tune the effect.",
    )
    effect_parser.add_argument(
        "--easing",
        default="IN_OUT_SINE",
        type=argtypes.valid_ease,
        help="Easing function to use for character movement.",
    )


class NamedEffect:
    """Effect that ___."""

    def __init__(self, terminal: Terminal, args: argparse.Namespace):
        self.terminal = terminal
        self.args = args
        self.pending_chars: list[EffectCharacter] = []
        self.animating_chars: list[EffectCharacter] = []

    def prepare_data(self) -> None:
        """Prepares the data for the effect by ___."""

        for character in self.terminal.characters:
            pass
            # do something with the data if needed (sort, adjust positions, etc)

    def run(self) -> None:
        """Runs the effect."""
        self.prepare_data()
        while self.pending_chars or self.animating_chars:
            self.terminal.print()
            self.animate_chars()

            # remove completed chars from animating chars
            self.animating_chars = [
                animating_char
                for animating_char in self.animating_chars
                if not animating_char.animation.active_scene_is_complete()
                or not animating_char.motion.movement_is_complete()
            ]

    def animate_chars(self) -> None:
        """Animates the characters by calling the move method and step animation. Move characters prior to stepping animation
        to ensure waypoint synced animations have the latest waypoint progress information."""
        for animating_char in self.animating_chars:
            animating_char.motion.move()
            animating_char.animation.step_animation()
