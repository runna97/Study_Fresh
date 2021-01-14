###################################################################
#
#   Study Fresh Project - Monitoring Program
#
#   Using Citizen Science to Engage Children with Indoor Air Quality
#
#   Recipient of Queensland Citizen Science Grant from
#   Queensland Department of Environment and Science
#
#   Project Lead: Dr Steven Snow
#
#   Project Members: Dr Lisa Ottenhaus, Dr Mashhuda Glencross
#                    Dr Paola Leardini, Brett Beeson,
#                    Rohith Nunna
#
###################################################################

###################################################################
# Peripheral File for the MH-Z19C CO2 Sensor
###################################################################

###################################################################
# File Imports
###################################################################
# Import library for function
import mh_z19

###################################################################
# Global Classes
###################################################################
class CO2Sensor:

    """
        Purpose: Class to manage the DFRobot Display
        Inputs:  None
        Outputs: None
    """

    def __init__(self):

        """
            Purpose: Class to manage the DFRobot Display
            Inputs:  None
            Outputs: None
        """

        self.Co2 = 0

    def read(self):
        
        """
            Purpose: Read CO2 value from the sensor
            Inputs:  None
            Outputs: Return the CO2 value
        """
        
        try:

            self.Co2 = mh_z19.read_all()['co2']

        except:

            self.Co2 = 0
            pass

        return self.Co2
