import os
import shutil
from pathlib import Path

processed_data = os.listdir('Z:\\katech\\polar_data\\annotation data prosessed')

for file in processed_data:
    full_filename = 'Z:\\katech\\polar_data\\annotation data prosessed\\' + file
    fileObj = Path(full_filename)
    print(fileObj.is_file())