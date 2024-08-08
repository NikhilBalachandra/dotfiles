#!/usr/bin/env python3

import os
import argparse
from nik_dotfile_helper import get_arch, get_platform, download_tool, link_tool_bin

DEFAULT_VERSION = "1.9.3"

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Download terraform")
    parser.add_argument("--version", help="Version of the terraform to download", default=DEFAULT_VERSION)
    parser.add_argument("--force", action="store_true", help="Force re-download of the file.")
    args = parser.parse_args()

    system = get_platform(flavor="linux,darwin")
    arch = get_arch(flavor="amd64,arm64")
    version = args.version
    force_download = args.force

    cache_file_name = f"terraform_{version}_{system}_{arch}.zip"
    download_url = f"https://releases.hashicorp.com/terraform/{version}/terraform_{version}_{system}_{arch}.zip"

    dest_bin_path = download_tool(download_url, cache_file_name, "terraform", version, force_download=force_download)
    link_tool_bin("terraform", version, "terraform", "terraform")

    # Confirm completion
    print(f"Terraform version {version} for {system} ({arch}) has been installed to {dest_bin_path}")

