import winsound
from typing import Dict, Tuple
import keyboard


# sound test stuff
# remmber add mac support

KEY_NOTE_MAP: Dict[str, Tuple[int, int]] = {
    "a": (261, 150),  # c4
    "w": (277, 150),  # c#4
    "s": (293, 150),  # d4
    "e": (311, 150),  # d#4
    "d": (329, 150),  # e4
    "f": (349, 150),  # f4
    "t": (370, 150),  # f#4
    "g": (392, 150),  # g4
    "y": (415, 150),  # g#4
    "h": (440, 150),  # a4
    "u": (466, 150),  # a#4
    "j": (493, 150),  # b4
    "k": (523, 200),  # c5
}

DRUM_MAP: Dict[str, str] = {
    "1": "KICK",
    "2": "SNARE",
    "3": "HI-HAT",
    "4": "CLAP",
}


def play_frequency(freq: int, duration: int) -> None:
    # beep beep
    winsound.Beep(freq, duration)



def trigger_drum(drum_type: str) -> None:
    if drum_type == "KICK":
        play_frequency(80, 100)
    elif drum_type == "SNARE":
        play_frequency(400, 80)
    elif drum_type == "HI-HAT":
        play_frequency(1200, 40)
    elif drum_type == "CLAP":
        play_frequency(800, 60)


def on_key_event(event: keyboard.KeyboardEvent) -> None:
    # keypress handler
    if event.event_type != keyboard.KEY_DOWN:
        return

    key = event.name.lower()

    if key in KEY_NOTE_MAP:
        freq, duration = KEY_NOTE_MAP[key]
        print(f"-> hit note: {key.upper()} ({freq} Hz)")
        play_frequency(freq, duration)

    elif key in DRUM_MAP:
        drum = DRUM_MAP[key]
        print(f"-> hit drum: {key} [{drum}]")
        trigger_drum(drum)


def main() -> None:
    keyboard.hook(on_key_event)
    keyboard.wait("esc")
    print("closing")


main()