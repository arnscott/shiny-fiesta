import subprocess
import os

BASE_DIR = os.environ['PATH'].split(os.pathsep)[0]



def run_dinosaur(mzml_file):
    command = 'java -jar {base_dir}/Dinosaur-1.1.3.free.jar --verbose {mzml}'.format(base_dir=BASE_DIR,
                                                                                     mzml=mzml_file)
    result = subprocess.run(command)
    return result 



def run_msgf(mzml_file):
    pass
