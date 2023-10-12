import network
import urequests
import os
import json
import machine
from time import sleep

mainfilename = ""
bootfilename = ""
repo_url = ""
mainversion_url = ""
mainfirmware_url = ""
bootversion_url = ""
bootfirmware_url = ""
latest_bootversion = ""
latest_mainversion = ""

class OTAUpdater:
    """ This class handles OTA updates. It connects to the Wi-Fi, checks for updates, downloads and installs them."""
    def __init__(self, repo_url,mainfile,bootfile):
        self.mainfilename = mainfile
        self.bootfilename = bootfile
        self.repo_url = repo_url
        
        self.mainversion_url = self.process_version_url(repo_url, self.mainfilename)     # Process the new version url
        self.mainfirmware_url = repo_url + self.mainfilename                             # Removal of the 'main' branch to allow different sources
        self.bootversion_url = self.process_version_url(repo_url, self.bootfilename)     # Process the new version url
        self.bootfirmware_url = repo_url + self.bootfilename                             # Removal of the 'main' branch to allow different sources
        
        # get the current version (stored in bootversion.json)
        if 'bootversion.json' in os.listdir():    
            with open('bootversion.json') as f:
                self.current_bootversion = json.load(f)['version']
            print(f"Current device boot firmware version is '{self.current_bootversion}'")
        else:
            self.current_bootversion = "0"
            # save the current version
            with open('bootversion.json', 'w') as f:
                json.dump({'version': self.current_bootversion}, f)
        # get the current version (stored in mainversion.json)
        if 'mainversion.json' in os.listdir():    
            with open('mainversion.json') as f:
                self.current_mainversion = json.load(f)['version']
            print(f"Current device main firmware version is '{self.current_mainversion}'")
        else:
            self.current_mainversion = "0"
            # save the current version
            with open('mainversion.json', 'w') as f:
                json.dump({'version': self.current_mainversion}, f)    

    def process_version_url(self, repo_url, filename):
        """ Convert the file's url to its assoicatied version based on Github's oid management."""

        # Necessary URL manipulations
        version_url = repo_url.replace("raw.githubusercontent.com", "github.com")  # Change the domain
        version_url = version_url.replace("/", "§", 4)                             # Temporary change for upcoming replace
        version_url = version_url.replace("/", "/latest-commit/", 1)                # Replacing for latest commit
        version_url = version_url.replace("§", "/", 4)                             # Rollback Temporary change
        version_url = version_url + filename                                       # Add the targeted filename
        
        return version_url
      
    def fetch_latest_bootcode(self)->bool:
        """ Fetch the latest code from the repo, returns False if not found."""
        
        # Fetch the latest code from the repo.
        response = urequests.get(self.bootfirmware_url)
        if response.status_code == 200:
            print(f'Fetched latest firmware code, status: {response.status_code}, -  {response.text}')
    
            # Save the fetched code to memory
            self.latest_code = response.text
            return True
        
        elif response.status_code == 404:
            print('Firmware not found.')
            return False

    def fetch_latest_maincode(self)->bool:
        """ Fetch the latest code from the repo, returns False if not found."""
        
        # Fetch the latest code from the repo.
        response = urequests.get(self.mainfirmware_url)
        if response.status_code == 200:
            print(f'Fetched latest firmware code, status: {response.status_code}, -  {response.text}')
    
            # Save the fetched code to memory
            self.latest_code = response.text
            return True
        
        elif response.status_code == 404:
            print('Firmware not found.')
            return False

    def update_boot_no_reset(self):
        """ Update the code without resetting the device."""

        # Save the fetched code and update the version file to latest version.
        with open('latest_code.py', 'w') as f:
            f.write(self.latest_code)
        
        # update the version in memory
        self.current_bootversion = self.latest_bootversion

        # save the current version
        with open('bootversion.json', 'w') as f:
            json.dump({'version': self.current_bootversion}, f)
        
        # free up some memory
        self.latest_code = None
       
        # Overwrite the old code.
        os.rename('latest_code.py', self.bootfilename)

    def update_main_no_reset(self):
        """ Update the code without resetting the device."""

        # Save the fetched code and update the version file to latest version.
        with open('latest_code.py', 'w') as f:
            f.write(self.latest_code)
        
        # update the version in memory
        self.current_mainversion = self.latest_mainversion

        # save the current version
        with open('mainversion.json', 'w') as f:
            json.dump({'version': self.current_mainversion}, f)
        
        # free up some memory
        self.latest_code = None
       
        # Overwrite the old code.
        os.rename('latest_code.py', self.mainfilename)
        
    def update_boot_and_reset(self):
        """ Update the code and reset the device."""

        print('Updating device...')

        # Overwrite the old code.
        os.rename('latest_code.py', self.bootfilename)  

        # Restart the device to run the new code.
        print("Restarting device... (don't worry about an error message after this")
        sleep(0.25)
        machine.reset()  # Reset the device to run the new code.
        
    def update_main_and_reset(self):
        """ Update the code and reset the device."""

        print('Updating device...')

        # Overwrite the old code.
        os.rename('latest_code.py', self.mainfilename)  

        # Restart the device to run the new code.
        print("Restarting device... (don't worry about an error message after this")
        sleep(0.25)
        machine.reset()  # Reset the device to run the new code.
        
    def check_for_bootupdates(self):
        """ Check if updates are available."""
        
        print('Checking for latest boot version...')
        headers = {"accept": "application/json"} 
        bootresponse = urequests.get(self.bootversion_url, headers=headers)
        bootdata = json.loads(bootresponse.text)       
        
        print (self.bootfirmware_url)
        self.latest_bootversion = bootdata['oid']                   # Access directly the id managed by GitHub
        print(f'latest version is: {self.latest_bootversion}')
               
        # compare versions
        newer_bootversion_available = True if self.current_bootversion != self.latest_bootversion else False
        
        print(f'Newer version available: {newer_bootversion_available}')    
        return newer_bootversion_available
     
    def check_for_mainupdates(self):
        print('Checking for latest main version...')
        headers = {"accept": "application/json"}
        mainresponse = urequests.get(self.mainversion_url, headers=headers)
        maindata = json.loads(mainresponse.text)
        
        print (self.mainfirmware_url)
        self.latest_mainversion = maindata['oid']                   # Access directly the id managed by GitHub
        print(f'latest version is: {self.latest_mainversion}')
        
        # compare versions
        newer_mainversion_available = True if self.current_mainversion != self.latest_mainversion else False
        
        print(f'Newer version available: {newer_mainversion_available}')    
        return newer_mainversion_available
    
    def download_and_install_update_if_available(self):
        """ Check for updates, download and install them."""
        if self.check_for_bootupdates():
            if self.fetch_latest_bootcode():
                self.update_boot_no_reset()
                self.update_boot_and_reset()
        else:
            print('No new boot updates available.')
        if self.check_for_mainupdates():
            if self.fetch_latest_maincode():
                self.update_main_no_reset()
                self.update_main_and_reset()
        else:
            print('No new main updates available.')