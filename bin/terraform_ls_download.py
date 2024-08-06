#!/usr/bin/env python3

import os
import argparse
from nik_dotfile_helper import get_arch, get_platform, download_tool_from_archive

DEFAULT_VERSION = "0.34.2"

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Download terraform LSP binary")
    parser.add_argument("--version", help="Version of the terraform LSP to download", default=DEFAULT_VERSION)
    parser.add_argument("--force", action="store_true", help="Force re-download of the file.")
    args = parser.parse_args()

    system = get_platform(flavor="linux,darwin")
    arch = get_arch(flavor="amd64,arm64")
    version = args.version
    force_download = args.force

    cache_file_name = f"terraform-ls_{version}_{system}_{arch}.zip"
    download_url = f"https://releases.hashicorp.com/terraform-ls/{version}/{cache_file_name}"
    dest_bin_path = download_tool_from_archive(download_url, cache_file_name, "terraform-ls", "terraform-ls", force_download=force_download)

    # Confirm completion
    print(f"Terraform Language Server v{version} for {system} ({arch}) has been installed to {dest_bin_path}")

