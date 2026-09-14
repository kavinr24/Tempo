import os
import platform
import sys
import time
from typing import Dict, Tuple
import winsound
import flet as ft

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


def main(page: ft.Page) -> None:
    page.title = "Tempo"
    page.bgcolor = "#121212"
    page.padding = 20

    status_text = ft.Text(
        value="Press buttons for sounds",
        size=16,
        color="#888888",
    )

    def handle_synth_click(e: ft.ControlEvent) -> None:
        key_name = e.control.data
        if key_name in KEY_NOTE_MAP:
            freq, duration = KEY_NOTE_MAP[key_name]
            status_text.value = f"Playing Note: {key_name.upper()} ({freq} Hz)"
            page.update()
            play_frequency(freq, duration)

    def handle_drum_click(e: ft.ControlEvent) -> None:
        drum_key = e.control.data
        if drum_key in DRUM_MAP:
            drum_name = DRUM_MAP[drum_key]
            status_text.value = f"Playing Drum: {drum_name}"
            page.update()
            trigger_drum(drum_name)

    # synth keys row
    synth_buttons = []
    for key, (freq, _) in KEY_NOTE_MAP.items():
        synth_buttons.append(
            ft.Button(
                content=key.upper(),
                data=key,
                on_click=handle_synth_click,
                width=50,
                height=50,
                bgcolor="#2196F3" if len(key) == 1 else "#333333",
                color="#FFFFFF",
            )
        )

    # drum pads row
    drum_buttons = []
    drum_colors = {
        "1": "#E91E63",
        "2": "#9C27B0",
        "3": "#00BCD4",
        "4": "#4CAF50",
    }
    for key, name in DRUM_MAP.items():
        drum_buttons.append(
            ft.Button(
                content=f"{name}\n({key})",
                data=key,
                on_click=handle_drum_click,
                width=80,
            )
        )


if __name__ == "__main__":
    ft.run(main)