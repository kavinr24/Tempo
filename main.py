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

TRACKS = ["Kick", "Snare", "Hi-Hat", "Synth"]
STEPS = 16


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

    grid_state = [[False for _ in range(STEPS)] for _ in range(len(TRACKS))]

    step_buttons = {}

    def toggle_step(e, track_idx, step_idx):
        grid_state[track_idx][step_idx] = not grid_state[track_idx][step_idx]
        is_active = grid_state[track_idx][step_idx]
        btn = step_buttons[(track_idx, step_idx)]
        btn.bgcolor = "#00E676" if is_active else "#2A2A2A"
        btn.border = ft.border.Border.all(1, "#00E676" if is_active else "#3A3A3A")
        page.update()

    def build_sequencer_grid():
        grid_rows = []

        header_cells = [ft.Container(width=80)]
        for step in range(STEPS):
            header_cells.append(
                ft.Container(
                    content=ft.Text(f"{step + 1}", size=11, color="#777777", weight=ft.FontWeight.BOLD),
                    width=36,
                    height=24,
                    alignment=ft.alignment.Alignment.CENTER,
                )
            )
        grid_rows.append(ft.Row(controls=header_cells, spacing=4))

        for t_idx, track_name in enumerate(TRACKS):
            row_cells = [
                ft.Container(
                    content=ft.Text(track_name, size=13, weight=ft.FontWeight.BOLD, color="#EEEEEE"),
                    width=80,
                    alignment=ft.alignment.Alignment.CENTER_LEFT,
                )
            ]

            for s_idx in range(STEPS):
                measure_offset = (s_idx // 4) % 2 == 0
                bg_color = "#2A2A2A" if measure_offset else "#222222"

                btn = ft.Container(
                    width=36,
                    height=44,
                    bgcolor=bg_color,
                    border_radius=4,
                    border=ft.border.Border.all(1, "#333333"),
                    on_click=lambda e, t=t_idx, s=s_idx: toggle_step(e, t, s),
                )
                step_buttons[(t_idx, s_idx)] = btn
                row_cells.append(btn)

            grid_rows.append(ft.Row(controls=row_cells, spacing=4))

        return ft.Column(controls=grid_rows, spacing=8)

    play_btn = ft.IconButton(icon=ft.Icons.PLAY_ARROW_ROUNDED, icon_color="#00E676", icon_size=32)
    bpm_field = ft.TextField(value="120", label="BPM", width=80, dense=True, text_align=ft.TextAlign.CENTER)

    header = ft.Row(
        controls=[
            ft.Text("Tempo", size=24, weight=ft.FontWeight.BOLD, color="#FFFFFF"),
            ft.Row(controls=[play_btn, bpm_field], spacing=10),
        ],
        alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
    )

    page.add(
        header,
        status_text,
        ft.Row(controls=synth_buttons, wrap=True, spacing=4),
        ft.Row(controls=drum_buttons, spacing=8),
        build_sequencer_grid(),
    )


if __name__ == "__main__":
    ft.run(main)