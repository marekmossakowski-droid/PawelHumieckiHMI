from __future__ import annotations

from dataclasses import dataclass
from hashlib import sha256
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont, PngImagePlugin

from .native_build import NativeDToolsBuildPlan, NativeDToolsScreen


@dataclass(frozen=True)
class NativeScreenAsset:
    screen_id: str
    path: Path
    sha256: str


def render_native_screen_assets(
    plan: NativeDToolsBuildPlan, output_directory: Path
) -> tuple[NativeScreenAsset, ...]:
    output_directory.mkdir(parents=True, exist_ok=True)
    assets = tuple(
        _render_screen(plan, screen, output_directory)
        for screen in plan.screens
    )
    return assets


def _render_screen(
    plan: NativeDToolsBuildPlan,
    screen: NativeDToolsScreen,
    output_directory: Path,
) -> NativeScreenAsset:
    image = Image.new("RGB", plan.canvas, "#F2F4F7")
    draw = ImageDraw.Draw(image)
    title_font = ImageFont.load_default(size=30)
    body_font = ImageFont.load_default(size=22)
    meta_font = ImageFont.load_default(size=16)

    draw.rectangle((0, 0, plan.canvas[0] - 1, 63), fill="#FFFFFF")
    draw.line((0, 63, plan.canvas[0], 63), fill="#D8DEE6", width=2)
    draw.text((24, 14), screen.label_pl, font=title_font, fill="#17212B")
    identifier_width = draw.textlength(screen.screen_id, font=body_font)
    draw.text(
        (plan.canvas[0] - identifier_width - 24, 20),
        screen.screen_id,
        font=body_font,
        fill="#5F6B7A",
    )

    for widget in screen.widgets:
        x, y, width, height = widget.geometry
        bounds = (x, y, x + width - 1, y + height - 1)
        if widget.primary_action:
            fill = "#1477FF"
            outline = "#1477FF"
            text_color = "#FFFFFF"
        else:
            fill = "#FFFFFF"
            outline = "#D8DEE6"
            text_color = "#17212B"
        draw.rounded_rectangle(bounds, radius=10, fill=fill, outline=outline, width=2)

        label_box = draw.textbbox((0, 0), widget.label_pl, font=body_font)
        label_width = label_box[2] - label_box[0]
        label_height = label_box[3] - label_box[1]
        label_x = x + max(12, (width - label_width) // 2)
        label_y = y + max(8, (height - label_height) // 2)
        draw.text(
            (label_x, label_y),
            widget.label_pl,
            font=body_font,
            fill=text_color,
        )
        if not widget.primary_action and height >= 72:
            draw.text(
                (x + 16, y + height - 24),
                widget.binding_id,
                font=meta_font,
                fill="#5F6B7A",
            )

    metadata = PngImagePlugin.PngInfo()
    metadata.add_text("project", plan.project_name)
    metadata.add_text("screen_id", screen.screen_id)
    metadata.add_text("manifest_sha256", plan.source_sha256)
    path = output_directory / f"{screen.screen_id}.png"
    temporary = path.with_suffix(".png.tmp")
    image.save(temporary, format="PNG", pnginfo=metadata, optimize=False)
    temporary.replace(path)
    return NativeScreenAsset(
        screen_id=screen.screen_id,
        path=path,
        sha256=sha256(path.read_bytes()).hexdigest(),
    )
