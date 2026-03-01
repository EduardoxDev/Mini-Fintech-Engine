import urllib.request
import zipfile
import os

url = "https://archive.apache.org/dist/maven/maven-3/3.9.8/binaries/apache-maven-3.9.8-bin.zip"
print("Downloading Maven...")
urllib.request.urlretrieve(url, "maven.zip")
print("Extracting Maven...")
with zipfile.ZipFile("maven.zip", 'r') as zip_ref:
    zip_ref.extractall(".")
print("Done!")
