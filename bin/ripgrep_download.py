#!/usr/bin/env python3

import os
import argparse
from nik_dotfile_helper import get_arch, get_platform, download_tool, link_tool_bin

DEFAULT_VERSION = "14.1.0"

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Download ripgrep")
    parser.add_argument("--version", help="Version of the ripgrep to download", default=DEFAULT_VERSION)
    parser.add_argument("--force", action="store_true", help="Force re-download of the file.")
    args = parser.parse_args()

    system = get_platform(flavor="linux,darwin")
    arch = get_arch(flavor="x86_64,aarch64")
    version = args.version
    force_download = args.force

    if system == "linux":
        system1 = "unknown-linux"
    elif system == "darwin":
        system1 = "apple-darwin"
    elif system == "windows":
        system1 = "pc-windows"
    else:
        raise NotImplementedError(f"Not implemented for platform {system}")

    cache_file_name = f"ripgrep-{version}-{arch}-{system1}.tar.gz"
    download_url = f"https://github.com/BurntSushi/ripgrep/releases/download/{version}/{cache_file_name}"

    dest_bin_path = download_tool(download_url, cache_file_name, "ripgrep", version, subdir=f"ripgrep-{version}-{arch}-{system1}", force_download=force_download)
    link_tool_bin("ripgrep", version, "rg", "rg")

    # Confirm completion
    print(f"Ripgrep v{version} for {system} ({arch}) has been installed to {dest_bin_path}")

