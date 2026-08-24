from pathlib import Path

from PyInstaller.utils.hooks import collect_submodules, is_module_or_submodule


repository_root = Path(SPECPATH).resolve().parents[2]
hidden_imports = collect_submodules(
    "mcp",
    filter=lambda name: not is_module_or_submodule(name, "mcp.cli"),
) + collect_submodules("pywinauto")

a = Analysis(
    [str(repository_root / "src/hoofcare/dtools_bridge/__main__.py")],
    pathex=[str(repository_root / "src")],
    binaries=[],
    datas=[(str(repository_root / "dtools/gl100e/bridge/allowlist.json"), ".")],
    hiddenimports=hidden_imports,
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    noarchive=False,
)
pyz = PYZ(a.pure)

exe = EXE(
    pyz,
    a.scripts,
    [],
    exclude_binaries=True,
    name='HoofCare.DToolsBridge',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    console=True,
)

bundle = COLLECT(
    exe,
    a.binaries,
    a.datas,
    strip=False,
    upx=True,
    name='HoofCare.DToolsBridge',
)
