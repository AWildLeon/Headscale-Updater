#!/usr/bin/env python3
##############################################
# Copyright (c) 2023 Leon Hubrich
# 
# MIT License:
# Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the “Software”), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED “AS IS”, WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
##############################################
#
# Requirements:
# PyGithub: pip3 install PyGithub
# headscale: github.com/juanfont/headscale
#
##############################################
#
# config:
GHTOKEN="https://github.com/settings/tokens?type=beta" # Example: "github_pat_..."
SUFFIX="_linux_amd64.deb"
#
##############################################
##############################################

from github import Github
import subprocess
import requests
import os


# login to github
g = Github(GHTOKEN)


# Get juanfont/headscale
repo = g.get_repo("juanfont/headscale")

# Get the latest release (no prereleases)
latest = repo.get_latest_release()

if latest.prerelease:
    print("Something went wrong, latest release is a prerelease, Please Contact Me")
    exit(1)


# Get the installed version: headscale version
installed = subprocess.check_output(["headscale", "version"]).decode("utf-8").strip()

print("Latest release: ", latest.title)
print("Installed: ", installed)

if latest.title == installed:
    print("Already up to date")
    exit(0)

# Get the latest release assets
assets = latest.get_assets()

# Get the latest release asset with the correct suffix
asset = next(filter(lambda x: x.name.endswith(SUFFIX), assets))


# Print the asset name
print("Downloading: ", asset.name)

# Download the asset
url = asset.browser_download_url

# Download the asset
r = requests.get(url, allow_redirects=True)

# Write the asset to a file (headscale.deb)
open('headscale.deb', 'wb').write(r.content)

print ("Installing: ", asset.name)

# Install the asset using apt-get
subprocess.check_call(["apt-get", "install", "./headscale.deb", "-y"])

# Clean up
os.remove("headscale.deb")

print("Done, Have a nice day!")