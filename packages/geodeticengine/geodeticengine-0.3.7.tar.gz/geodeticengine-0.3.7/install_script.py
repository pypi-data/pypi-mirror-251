import pyproj
import subprocess

def main():
    print(pyproj.datadir.get_user_data_dir())

    url = "https://cdn.proj.org/"
    output_folder = pyproj.datadir.get_user_data_dir()

    subprocess.run(["wget", "-r", "--no-parent", "-P", output_folder, url])

if __name__ == "__main__":
    main()