from setuptools import setup, find_packages

with open("readme.md","r") as rd:
    long_description = rd.read()

setup(
    name='rfidpy',
    version='0.3',
    author="M.Karthickraja",
    author_email="karthickrajam8100@gmail.com",
    description="Raspberry pi 5 interface with RFID(MFR522)",
    long_description=long_description,
    long_description_content_type="text/markdown",
    packages=find_packages(),
    install_requires=[],
    keywords=['rfid', 'raspberry-pi', 'mfrc522', 'pi5', 'python',],

)
