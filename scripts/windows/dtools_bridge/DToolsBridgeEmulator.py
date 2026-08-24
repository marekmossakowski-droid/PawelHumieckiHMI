from __future__ import annotations

import argparse
import json
import os
from pathlib import Path
import sys
import tkinter as tk


class Emulator:
    def __init__(
        self,
        project: str,
        command_file: Path | None,
        ready_file: Path | None,
    ) -> None:
        self.root = tk.Tk()
        self.root.title(f"{project} - [HMI0.whe]")
        self.root.geometry("720x480")
        self.command_file = command_file
        self.bitmap_dialog: tk.Toplevel | None = None
        self.graphics_dialog: tk.Toplevel | None = None

        menu = tk.Menu(self.root)
        components = tk.Menu(menu, tearoff=False)
        graph = tk.Menu(components, tearoff=False)
        graph.add_command(label="Bitmap", command=self.open_bitmap_component)
        components.add_cascade(label="Graph And Animation", menu=graph)
        menu.add_cascade(label="Components", menu=components)
        draw = tk.Menu(menu, tearoff=False)
        draw.add_command(label="Load Image", command=self.open_bitmap_component)
        menu.add_cascade(label="Draw", menu=draw)
        self.root.config(menu=menu)

        tk.Label(
            self.root,
            text="DTools Bridge Emulator — synthetic/test-only",
            font=("Segoe UI", 18, "bold"),
        ).pack(pady=32)
        tk.Button(
            self.root,
            text="Bitmap Component",
            command=self.open_bitmap_component,
        ).pack(pady=12)
        if command_file is not None:
            self.root.after(200, self.poll_commands)
        if ready_file is not None:
            self.root.update_idletasks()
            ready_file.write_text(
                json.dumps(
                    {
                        "pid": os.getpid(),
                        "hwnd": self.root.winfo_id(),
                        "title": self.root.title(),
                        "executable": sys.executable,
                    }
                ),
                encoding="utf-8",
            )

    def open_bitmap_component(self) -> None:
        dialog = tk.Toplevel(self.root)
        dialog.title("Bitmap Component Attribute")
        dialog.geometry("480x300")
        tk.Label(dialog, text="Synthetic bitmap component").pack(pady=30)
        tk.Button(dialog, text="Edit Graphics", command=self.open_graphics).pack()
        self.bitmap_dialog = dialog

    def open_graphics(self) -> None:
        dialog = tk.Toplevel(self.root)
        dialog.title("Graphics Library")
        dialog.geometry("520x340")
        tk.Button(dialog, text="Import Graphics", command=self.show_g1).pack(pady=30)
        self.graphics_dialog = dialog

    def show_g1(self) -> None:
        if self.graphics_dialog is not None:
            tk.Label(self.graphics_dialog, text="G1-00.bmp").pack(pady=20)

    def show_unknown_dialog(self) -> None:
        dialog = tk.Toplevel(self.root)
        dialog.title("Unexpected Dialog")
        tk.Label(dialog, text="Synthetic unexpected dialog").pack(padx=30, pady=30)

    def poll_commands(self) -> None:
        if self.command_file is not None and self.command_file.exists():
            command = self.command_file.read_text("utf-8").strip()
            self.command_file.unlink(missing_ok=True)
            if command == "show_unknown_dialog":
                self.show_unknown_dialog()
        self.root.after(200, self.poll_commands)

    def run(self) -> None:
        self.root.mainloop()


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--project", required=True)
    parser.add_argument("--command-file", type=Path)
    parser.add_argument("--ready-file", type=Path)
    args = parser.parse_args()
    Emulator(args.project, args.command_file, args.ready_file).run()


if __name__ == "__main__":
    main()
