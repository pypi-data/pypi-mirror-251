#!/usr/bin/python
"""
This module contains some useful functions for gps data processing such as:

convllh(llh,radians=True)
extractfromGamitBakf(cfile, stations)
savedisp(dataDict,fname=None, header="")
"""
import subprocess

def run_cmd(check_cmd):
    """
    Function that executes a system command and capture its output and return code. It runs a given system command using the subprocess module, waits for it to complete, and then captures its outputs and return code.

    Args:
        check_cmd (str): The system command to be executed.

    Returns:
        (int, str): A tuple containing two elements: 1. proc_check_returncode (int): The return code of the command. A return code of 0 typically indicates that the command was executed successfully. 2. proc_check_comm (bytes): The output of the command as a byte string. If the command produces no output, this will be an empty byte string.

    """
    ## Run command

    process = subprocess.Popen(check_cmd,shell=True,stdout=subprocess.PIPE)
    process.wait()

    proc_check_returncode = process.returncode
    proc_check_comm = process.communicate()[0].strip('\n'.encode())
    
    
    return proc_check_returncode,proc_check_comm

def run_syscmd(check_cmd,p_args):
    """
    Function executing a system command and capturing its output and return code.

    This function runs a given system command using the subprocess module,
    waits for it to complete, and then captures its output and return code.
    It also logs debug information if specified in the parameters.

    Parameters:
        check_cmd (str): The system command to be executed.
        p_args (dict): A dictionary containing various parameters, including 'debug' (bool): If True, print debug information to the console.

    Returns:
        (int, str):  A tuple containing two elements:  1. proc_check_returncode (int): The return code of the command. A return code of 0 typically indicates that the command was executed successfully, 255 indicates a timeout, and other values indicate failure. 2. proc_check_comm (str): The output of the command as a string. If the command  produces no output, this will be an empty string.
    
    """

    ## Run command
    import sys, re, subprocess, getopt, logging, copy, socket, types
    import gpstime

    currfunc=__name__+'.'+sys._getframe().f_code.co_name+' >>' # module.object name
    if p_args['debug']: print('%s Starting ...' % currfunc)

    process = subprocess.Popen(check_cmd,shell=True,stdout=subprocess.PIPE)
    process.wait()

    proc_check_returncode = process.returncode
    proc_check_comm = process.communicate()[0].strip('\n')
    
    
    #(3)# Make desicions according to output...
    if p_args['debug']: print('%s process.returncode:' % currfunc, proc_check_returncode)
    if p_args['debug']: print(currfunc,'process.communicate():\n---------------\n', proc_check_comm,'\n-------------')
    if proc_check_returncode == 0:
        if p_args['debug']: print("%s Command went well.." % currfunc)
    elif proc_check_returncode == 255:
        if p_args['debug']: print("%s Timeout..." % currfunc)
    else:
        if p_args['debug']: print("%s Command failed... " % currfunc)


def run_netcmd(netcmd, port, station, p_args):
    """
    Execute a network command based on the connection type and capture its output and return code.

    This function formats a network command string based on the connection type specified in the
    station dictionary and then executes the command using the `run_syscmd` function. It logs
    debug information if specified in the arguments.

    Args:
        netcmd (str): The network command template to be executed, with placeholders for the IP and port.
        port (int): The port number to be used in the network command.
        station (dict): A dictionary containing station configuration, including:
            - 'conn_type' (str): The connection type, which can be 'tunnel', 'sil', 'direct', or 'serial'.
            - 'rout_ip' (str): The routing IP address used for 'tunnel' connections.
            - 'recv_httpport' (str): The receiver HTTP port used for 'tunnel' connections.
            - 'sil_httpport' (str): The SIL HTTP port used for 'sil' connections.
            - 'recv_ip' (str): The receiver IP address used for 'direct' connections.
            - 'sil_computer' (bool): Indicates if a SIL computer is used for 'serial' connections.
        p_args (dict): A dictionary containing various arguments, including:
            - 'debug' (bool): If True, print debug information to the console.

    Returns:
        (int, str): A tuple where the first element is the return code of the command,
        and the second element is the output of the command as a string. A return code
        of 0 typically indicates that the command was executed successfully, and other
        values indicate failure. If the command produces no output, the second element
        will be an empty string.

    """
    currfunc=__name__+'.'+sys._getframe().f_code.co_name+' >>'
    if p_args['debug']: print('%s Starting ...' % currfunc)

    conntype=station['conn_type'].split(',') # methods defined by conn_type

    #(1)# define how to handle differennt communication types
    if 'tunnel' in conntype:
        # direct ip connection through tunnels 
        if p_args['debug']: print('%s connecting through %s on port %s' % (currfunc,station['rout_ip'], station['recv_httpport']))
        netcmd = netcmd % '%s:%s' % (station['rout_ip'], port )
        if p_args['debug']: print('%s netcmd=' % currfunc,netcmd)

    elif 'sil' in conntype:
        # direct ip connection through sil computer using port forwarding
        if p_args['debug']: print('%s NetRS/NetR9 receiver on a SIL station' % currfunc)
        netcmd = netcmd % '%s:%s' % ('localhost',station['sil_httpport'])
        if p_args['debug']: print('%s netcmd=' % currfunc,netcmd)

    elif 'direct' in conntype:
        # direct ip connection 
        if p_args['debug']: print('%s Direct connection' % currfunc)
        netcmd = netcmd % station['recv_ip']
        if p_args['debug']: print('%s netcmd=' % currfunc,netcmd)
				
    elif 'serial' in conntype:
        if station['sil_computer']:
            pass
					
        elif '3G' in station['conn_type']:
            pass

    #(2)# run the command and return the output to proc_checktemp_comm
    proc_checktemp_returncode, proc_checktemp_comm=run_syscmd(netcmd, p_args)
    
    # Return
    return proc_checktemp_returncode, proc_checktemp_comm


def checkError(proc_check_returncode, proc_check_comm, searchres, p_args):
    """
    Check for errors in the output of a system command.

    This function evaluates the return code and output of a system command to determine if an error occurred.
    It also searches for a specific string in the output to confirm successful execution.

    Args:
        proc_check_returncode (int): The return code from the system command.
        proc_check_comm (str): The output from the system command.
        searchres (bool): The result of a search operation, typically a boolean indicating if a specific string was found.
        p_args (dict): A dictionary containing various arguments, including:
            - 'debug' (bool): If True, print debug information to the console.

    Returns:
        int: An error code representing the status of the check:
            - 0 if no errors were found and the search result is True.
            - 11 if 'ERROR' is found in the output.
            - 1 for any other case indicating something is wrong.
    """
    currfunc = __name__ + '.' + sys._getframe().f_code.co_name + ' >>'
    if p_args.get('debug'): print('%s Starting ...' % currfunc)

    if proc_check_returncode == 0 and searchres:
        if p_args.get('debug'): print("%s all is OK" % currfunc)
        return 0
    elif 'ERROR' in proc_check_comm:
        if p_args.get('debug'): print("%s proc_check_comm returned: %s" % (currfunc, proc_check_comm))
        return 11
    else:
        if p_args.get('debug'): print("%s Something is wrong" % currfunc)
        print("ERROR in matching proc_check_comm =\n", proc_check_comm,
              "\nand proc_check_returncode=", proc_check_returncode,
              "\nsearchres=", searchres)
        return 1


def changeDictKeys(session, chdict, p_args):
    """
    Change the keys of dictionaries within a list according to a mapping.

    This function iterates over a list of dictionaries and renames keys according to a provided mapping.
    The changes are made in place.

    Args:
        session (list of dict): The list of dictionaries to process.
        chdict (dict): A dictionary containing the mapping of old keys to new keys.
        p_args (dict): A dictionary containing various arguments, including:
            - 'debug' (bool): If True, print debug information to the console.

    Returns:
        list of dict: The list of dictionaries with updated keys.
    """
    currfunc = __name__ + '.' + sys._getframe().f_code.co_name + ' >>'
    if p_args.get('debug'): print('%s Starting inplace key change ...\n--\nChanging keys: %s\n--\nIn: %s\n--\nTo: %s'
                                  % (currfunc, chdict.keys(), session, chdict.values()))

    for sess in session:
        for key in set(chdict.keys()) & set(sess.keys()):
            sess[chdict[key]] = sess.pop(key)

    return session

import socket
import re
import sys

def checkPort(host, port, p_args):
    """
    Check if a network port on a given host is open and accepting connections.

    Args:
        host (str): The hostname or IP address to check.
        port (int): The port number to check.
        p_args (dict): A dictionary containing various arguments, including:
            - 'debug' (bool): If True, print debug information to the console.

    Returns:
        int: Returns 0 if the connection to the port is successful, 1 otherwise.
    """
    # variable port needs to be of type int
    currfunc=__name__+'.'+sys._getframe().f_code.co_name+' >>'
    if p_args['debug']: print('%s Starting...' % currfunc)

    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        s.connect((host, port))
        s.shutdown(2)
        #if p_args['debug']:
        print("%s Success connecting to %s on port: %s" % (currfunc, host, port))
        return 0
    except:
        #if p_args['debug']:
        print("%s Cannot connect to %s on port: %s" % (currfunc, host, port))
        return 1

import re

def getportdict(pref, station, p_args):
    """
    Extract port definitions from a station configuration dictionary based on a prefix.

    This function searches through the station configuration dictionary for keys that match
    a given prefix followed by '_port' and constructs a new dictionary with the results.

    Args:
        pref (str): The prefix used to identify port definitions in the station configuration.
        station (dict): A dictionary containing station configuration.
        p_args (dict): A dictionary containing various arguments, including:
            - 'debug' (bool): If True, print debug information to the console.

    Returns:
        (dict): A dictionary containing the extracted port definitions, where each key is the port type (derived from the original key) and the value is the port number as a string.
    """
    # Search string to check for defined ports
    searchstr = re.compile(r'\s*%s_(\w+)port=(\S+)\s*' % re.escape(pref))
    stationstr = ' '.join(['%s=%s' % (k, v) for k, v in station.items()])

    # Extracting the port definitions from the pattern pref_+port
    searchres = searchstr.findall(stationstr)
    recvport = dict(searchres)

    return recvport

import sys

def str_to_class(field):
    """
    Convert a string to a class object in the current module.

    This function takes the name of a class as a string and returns the class object with that name
    from the current module. If the class does not exist, it raises an AttributeError.

    Args:
        field (str): The name of the class to retrieve.

    Returns:
        class: The class object corresponding to the given name.

    Raises:
        AttributeError: If the class with the given name does not exist in the current module.
    """
    return getattr(sys.modules[__name__], field)

