#Authors: Fiona Shyne and London Lowmanstone

import subprocess

#constants
TESTING = True

class CommandCenter():
    exDir = "~/rsn/umn-ros-pkg/rsn/carpMonitoring/scripts_cmd" #directory to excecute commands from
    
    @staticmethod
    def do(what, *values):
        setCommands = {"rudder":"steer_cmd.sh", "propeller":"prop_cmd.sh"}
        
        '''excecutes a command in the shell of the computer to do something
        If the parameter what is "rudder" or "propeller", then values should be [value to set the thing to, comment aka how much you want it to print]
        '''
        if what in setCommands:
            #I could make this a lot fewer lines, but then if it throws an error we have very little idea of what went wrong
            value = values[0]
            if len(values) == 2:
                comment = values[1]
            else:
                comment=1 #default
            command = "{} {}".format(setCommands[what], value)
            command = CommandCenter.add_dir_to_command(CommandCenter.exDir, command)
            CommandCenter.excecuteCommand(command, comment=comment)
            
        
    @staticmethod
    def add_dir_to_command(directory, command):
        return "cd {} && {}".format(directory, command)
        
    @staticmethod
    def excecuteCommand(command, comment=0):
        if comment==1:
            print("Running command '{}'".format(command))
        
        if not TESTING:
            output = subprocess.check_output([command], shell=True)
        else:
            output = "You are testing; no command was actually run."
            
        if comment==2:
            print("Output of the command was: '{}'".format(output))
        return output
