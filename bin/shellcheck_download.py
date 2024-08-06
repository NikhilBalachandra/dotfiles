#!/usr/bin/env python3

import os
import argparse
from nik_dotfile_helper import get_arch, get_platform, download_tool_from_archive

DEFAULT_VERSION = "0.10.0"

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Download shellcheck binary")
    parser.add_argument("--version", help="Version of the shellcheck to download", default=DEFAULT_VERSION)
    parser.add_argument("--force", action="store_true", help="Force re-download of the file.")
    args = parser.parse_args()

    system = get_platform(flavor="linux,darwin")
    arch = get_arch(flavor="x86_64,aarch64")
    version = args.version
    force_download = args.force

    cache_file_name = f"shellcheck-v{version}.{system}.{arch}.tar.xz"
    download_url = f"https://github.com/koalaman/shellcheck/releases/download/v{version}/{cache_file_name}"
    dest_bin_path = download_tool_from_archive(download_url, cache_file_name, "shellcheck", f"shellcheck-v{version}/shellcheck", force_download=force_download)

    # Confirm completion
    print(f"Shellcheck v{version} for {system} ({arch}) has been installed to {dest_bin_path}")

