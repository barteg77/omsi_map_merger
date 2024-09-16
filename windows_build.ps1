# Copyright 2024 Bartosz Gajewski
#
# This file is part of OMSI Map Merger.
#
# OMSI Map Merger is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 3 of the License, or
# (at your option) any later version.
#
# OMSI Map Merger is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with OMSI Map Merger. If not, see <http://www.gnu.org/licenses/>.

# Requires Python 3.12 with pip, venv
# Requires Git
# Requires 7-Zip

$startPwd = Get-Location

# Create working directory
$datetime = Get-Date -Format "yyyy-MM-dd_HH-mm-ss"
$buildName = "omsi_map_merger_windows_package_$datetime"
New-Item -Type Directory -Name $buildName -ErrorAction Stop | Out-Null
Set-Location -Path $buildName
$buildPwd = Get-Location
Write-Output "Working directory will be $buildPwd"

# Create Python virtual environment
$venvName = "pyvenv"
Write-Output "Will create Python virtualenv $venvName..."
python -m venv $venvName
$activate = Join-Path -Path $venvName -ChildPath "Scripts\Activate.ps1"
& $activate

# Install required pip packages
pip install charset-normalizer==3.3.2 parglare==0.13.0 PySimpleGUI==4.70.1
pip install pyinstaller
Write-Output "Installed following pip packages:"
pip list

# Prepare Omsi Map Merger sources
$sourcesDir = $PSScriptRoot

# Get Omsi Map Merger version
Set-Location -Path $sourcesDir
$ommVersion = python -c "import version; print(version.version)"
Set-Location -Path $buildPwd
Write-Output "Will pack OMSI Map Merger $ommVersion"

# Create executable with PyInstaller
pyinstaller "$sourcesDir\starter_loader.spec"
deactivate
$distDir = Join-Path -Path $buildPwd -ChildPath "dist\omsi_map_merger"

# Copy user information Files
$userInfoFiles = @(
	"LICENSE.txt",
	"LICENSE_charset_normalizer.txt",
	"LICENSE_Parglare.txt",
	"LICENSE_PySimpleGUI.txt",
	"LICENSE_Python.txt",
	"CREDITS.md",
	"MANUAL_en.md",
	"MANUAL_pl.md"
)
foreach ($file in $userInfoFiles) {
	$filePath = Join-Path -Path $sourcesDir -ChildPath $file
	Write-Output "Copying file $filePath to dist directory $distDir"
	Copy-Item -Path $filePath -Destination $distDir -ErrorAction Stop
}

# Create zip package with 7-Zip
& "C:\Program Files\7-Zip\7z.exe" a "omsi_map_merger_$ommVersion.zip" $distDir
Set-Location -Path $startPwd
