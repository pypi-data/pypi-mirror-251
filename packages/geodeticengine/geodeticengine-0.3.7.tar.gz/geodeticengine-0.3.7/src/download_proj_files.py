import pyproj
import subprocess
import os

def main():
    ''' Download Proj grid files '''
    url = "https://cdn.proj.org/"
    output_folder = "proj_files"
    if not os.path.exists(os.path.join(os.getcwd(), output_folder)):
        os.mkdir(os.path.join(os.getcwd(), output_folder))

    subprocess.run(["wget", "-r", "--no-parent", "-P", output_folder, url])

if __name__ == "__main__":
    main()