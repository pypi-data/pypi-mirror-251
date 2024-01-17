import configparser
import os
import shutil

class ConfigParser:


    def __init__(self):
        # Setting up the working directories
        self.config = configparser.ConfigParser()
        self.mount_path = os.environ.get('MOUNT_PATH')
        current_dir = os.path.dirname(os.path.abspath(__file__))
        
        # Copying the stations.cfg from the mounted path to the current directory
        source_stations_config_path = os.path.join(self.mount_path, 'gpsconfig', 'cparser', 'stations.cfg')
        self.dest_stations_config_path = os.path.join(current_dir, 'stations.cfg')
        shutil.copy(source_stations_config_path, self.dest_stations_config_path)

        # Reading the stations.cfg file
        self.config.read(self.dest_stations_config_path)

        # Copying the postprocess.cfg from the mounted path to the current directory
        source_postprocess_config_path = os.path.join(self.mount_path, 'gpsconfig', 'cparser', 'postprocess.cfg')
        self.dest_postprocess_config_path = os.path.join(current_dir, 'postprocess.cfg')
        shutil.copy(source_postprocess_config_path, self.dest_postprocess_config_path)

        # Reading the postprocess.cfg file
        self.config.read(self.dest_postprocess_config_path)


    # Establishing the methods usable through the package to interact with the cparser module
    def get_config(self, section, option):
        """
        This function gets a configuration option from the 'stations.cfg' file.
        """
        # Getting the configuration option
        value = self.config.get(section, option)
        # Replacing /mnt/ with the MOUNT_PATH
        value = value.replace('/mnt/', self.mount_path)
        return value

    
    def get_stations_config_path(self):
        """
        This function returns the path to the 'stations.cfg' file.
        """
        return self.dest_stations_config_path

    def get_postprocess_config_path(self):
        """
        This function returns the path to the 'postprocess.cfg' file.
        """

        return self.dest_postprocess_config_path

    
    def getStationInfo(self, station_id):
      """
      This function gets station information from the 'stations.cfg' file.
      """
      # Read the 'station' section from the 'stations.cfg' file
      if self.config.has_section(station_id):
          station_info = dict(self.config.items(station_id))
          return {'station': station_info}
      else:
          raise Exception(f"Station '{station_id}' not found in 'stations.cfg' file.")

    def getPostprocessConfig(self, option):
        """
        This function gets a configuration option from the 'postprocess.cfg' file.
        """
        # Read the 'Configs' section from the 'postprocess.cfg' file
        if self.config.has_section('Configs'):
            if self.config.has_option('Configs', option):
                return self.config.get('Configs', option)
        raise Exception(f"Option '{option}' not found in 'Configs' section of the postprocess configuration file.")

