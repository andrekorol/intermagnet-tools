from urlget import download_from_url
import os
import zipfile
import shutil
import gzip

if not os.path.isdir("data"):
    os.makedirs("data")

download_from_url("https://raw.githubusercontent.com/andrekorol/intermagnet-tools/master/data/quietest.zip",
                  "data")

zip_ref = zipfile.ZipFile("data/quietest.zip", 'r')
zip_ref.extractall("data")
zip_ref.close()

quietest_days = [20, 21]

for root, dirs, files in os.walk("data"):
    for file in files:
        ext = file.split('.')[-1]
        if ext == 'gz':
            with gzip.open(os.path.join(root, file), 'rb') as fin:
                for line in fin:
                    decoded_line = line.decode("utf-8")
                    print(decoded_line)
shutil.rmtree("data")
