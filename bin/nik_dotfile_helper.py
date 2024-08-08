#!/usr/bin/env python3

import sys
import os
import urllib.request
import platform as plt
import zipfile
import tarfile
import stat

def get_platform(flavor=""):
    """
    Determine the platform of the current system.

    Args:
        flavor (str): Optional flavor to specify a particular platform variant.
            For example, to get "linux" and "macos" (instead of darwin) as
            platforms, use flavor="linux,macos".


    Returns:
        str: The platform name ('macos', 'win32', etc.).
    """
    system = plt.system().lower()
    
    # Handle macOS flavors
    if system == "darwin" and "macos" in flavor:
        system = "macos"
    # Handle Windows flavors
    elif system == "windows" and "win32" in flavor:
        system = "win32"

    return system

def get_arch(flavor=""):
    """
    Determine the architecture of the current system.

    Args:
        flavor (str): Optional flavor to specify a particular architecture variant.
            For example, to get "amd64" and "arm64" (instead of aarch64)
            as architectures, use flavor="amd64,arm64".

    Returns:
        str: The architecture name ('amd64', 'aarch64', etc.).
    """

    # Determine the architecture
    arch = plt.machine().lower()
    
    # Handle architecture flavors
    if arch == "x86_64":
        arch = "amd64"
        if "x86_64" in flavor:
            arch = "x86_64"
    elif arch in ["aarch64", "arm64"]:
        arch = "aarch64"
        if "arm64" in flavor:
            arch = "arm64"
        elif "aarch64" in flavor:
            arch = "aarch64"

    return arch


def _show_progress(block_num, block_size, total_size):
    """
    Display download progress.
    """

    print(round(block_num * block_size / total_size *100,2), end="\r", file=sys.stderr)


def download_file(url, cache_dir, file_name, force_download=False):
    """
    Download a file, cache it, and optionally force a re-download.

    Args:
        url (str): The URL of the file to download.
        cache_dir (str): Directory to cache the downloaded file.
        file_name (str): Name of the file to save.
        force_download (bool): Whether to force re-download of the file.

    Returns:
        str: Path to the downloaded file.
    """

    # Create cache directory if it doesn't exist
    os.makedirs(cache_dir, exist_ok=True)

    dest_file = os.path.join(cache_dir, file_name)

    if force_download or not os.path.exists(dest_file):
        print(f"Downloading file from {url}...", file=sys.stderr)
        urllib.request.urlretrieve(url, dest_file, _show_progress)
    return dest_file


def create_local_bin():
    """
    Create a directory for executable files (creates ~/.local/bin/).

    Returns:
        str: Path to the created local bin directory.
    """
    home_dir = os.path.expanduser("~")
    local_bin_dir = os.path.join(home_dir, ".local/bin/")
    os.makedirs(local_bin_dir, exist_ok=True)
    return local_bin_dir


def create_cache_dir_for(dir_name):
    """
    Create a cache directory under ~/.local/cache/.

    Args:
        dir_name (str): Name of the cache directory.

    Returns:
        str: Path to the created cache directory.
    """
    home_dir = os.path.expanduser("~")
    dest_dir = os.path.join(home_dir, ".local/cache/", dir_name)
    os.makedirs(dest_dir, exist_ok=True)
    return dest_dir


def get_opt_dir_for(name, version):
    home_dir = os.path.expanduser("~")
    return os.path.join(home_dir, ".local/opt/", name, version)


def create_opt_dir_for(name, version):
    """
    Create a directory for executable files (creates ~/.local/bin/).

    Returns:
        str: Path to the created local bin directory.
    """
    opt_dir = get_opt_dir_for(name, version)
    os.makedirs(opt_dir, exist_ok=True)
    return opt_dir


def extract_archive(archive_file, dest_dir, subdir=None):
    """
    Extract all files from a zip/xz archive to ~/.local/opt.

    Args:
        archive_file (str): Path to the zip/xz archive.
    """

    def remove_prefix(text, prefix):
        return text[text.startswith(prefix) and len(prefix):]

    def strip_prefix_and_extract(z, members):
        if subdir is None:
            z.extractall(dest_dir)
            return

        for file in members:
            # Look for prefix in the file path
            if file.path.startswith(subdir + '/'):
                # Note: Cannot use os.path.join without leading slash
                file.path = remove_prefix(file.path, subdir + '/')

                # Skip if file is directory itself (which has empty path after stripping)
                if len(file.path) == 0:
                    continue

                z.extract(file, dest_dir)

    _, ext = os.path.splitext(archive_file)
    if len(ext) == 0:
        raise ValueError(f"No extension found in the archive file {archive_file}")

    if ext == ".zip":
        with zipfile.ZipFile(archive_file) as z:
            strip_prefix_and_extract(z, z.filelist)
    elif ext == ".xz":
        with tarfile.open(archive_file, 'r:xz') as z:
            strip_prefix_and_extract(z, z.getmembers())
    elif ext == ".gz":
        with tarfile.open(archive_file, 'r:gz') as z:
            strip_prefix_and_extract(z, z.getmembers())
    else:
        raise NotImplementedError(f"{ext} archive file is unsupported")


def make_file_exec(path):
    """
    Make a file executable.

    Args:
        path (str): Path to the file.
    """
    st = os.stat(path)
    os.chmod(path, st.st_mode | stat.S_IEXEC)


def download_tool(url, cache_file_name, name, version, subdir=None, force_download=False):
    """
    Download an archive file, extract a tool from it, and move it to ~/.local/bin/.

    Args:
        url (str): URL of the archive file.
        cache_dir_name (str): Name of the cache directory. Directory is created as
            ~/.local/cache/{cache_dir_name}
        cache_file_name (str): Name of the archive file. File is saved as
            ~/.local/cache/{cache_dir_name}/{cache_file_name}
        name (str): Path to the tool within the archive.
        name (str): Name of the tool to be placed in ~/.local/bin/.
        force_download (bool): Whether to force re-download of the file.

    Returns:
        str: Path to the installed tool in ~/.local/bin/.
    """
    home_dir = os.path.expanduser("~")
    cache_dir = create_cache_dir_for(name)
    archive_file = download_file(url, cache_dir, cache_file_name, force_download=force_download)
    tool_dir = os.path.join(home_dir, ".local/opt/", name, version)
    os.makedirs(tool_dir, exist_ok=True)
    
    extract_archive(archive_file, tool_dir, subdir=subdir)
    return tool_dir


def link_tool_bin(tool_name, version, bin_name, bin_path):
    bin_dir = create_local_bin()
    tool_dir = get_opt_dir_for(tool_name, version)
    bin_path = os.path.join(tool_dir, bin_path)
    symlink_path = os.path.join(bin_dir, bin_name)
    if os.path.exists(symlink_path):
        if os.path.islink(symlink_path):
            os.remove(symlink_path)
        else:
            raise FileExistsError(f"File {symlink_path} already exists. Please remove it first.")
    os.symlink(bin_path, symlink_path)
