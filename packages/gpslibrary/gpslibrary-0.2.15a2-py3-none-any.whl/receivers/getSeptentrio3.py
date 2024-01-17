# -*- coding: utf-8 -*-

# ------------------------------- #
#
# getSeptentrio.py 0.5
# Code made by bgo@vedur.is modified from fjalar@vedur.is
# Iceland Met Office
# 2018
#
# ------------------------------- #

#----------# IMPORT LIBRARIES #-----------#
# Common modules
import sys, signal, argparse, os, time
import os.path as path
from datetime import datetime as datetime
import urllib.request, urllib.parse, urllib.error, shutil, subprocess

import gtimes.timefunc as gt

import os
import shutil
import sys
import re
from ftplib import FTP
from datetime import datetime
import gtimes.timefunc as gpstime

def check_for_file(doyo, year, archive_path, station_id):
    """
    Checks if the file for a given day number of the year and year exists in the data archive.

    Args:
        doyo (int): Day number of the year.
        year (int): Year to check the file for.
        archive_path (str): Path to the archive where files are stored.
        station_id (str): Station ID to check the file for.

    Returns:
        bool: True if the file exists, False otherwise.
    """
    file_name = get_file_name(doyo, year, station_id)
    full_path = os.path.join(archive_path, file_name)
    print(f" >> Checking for file {full_path}")
    file_found = os.path.isfile(full_path)
    if not file_found:
        print(" ---> File not found. Will be downloaded.")
    return file_found

def download_file(file_name, filedir_name, location_dir, ip_number, ip_port):
    """
    Downloads a file from a specified IP address and port using FTP into a given directory.

    Args:
        file_name (str): The name of the file to download.
        filedir_name (str): The directory name on the FTP server where the file is located.
        location_dir (str): The local directory where the file will be saved.
        ip_number (str): The IP address of the FTP server.
        ip_port (int): The port number of the FTP server.

    Returns:
        bool: True if the file was successfully downloaded, False otherwise.
    """
    file_downloaded = False
    os.chdir(location_dir)
    try:
        ftp = FTP()
        ftp.connect(ip_number, ip_port)
        ftp.login('anonymous')
        # Special handling for certain station names
        if re.search('ROTH|SVIN|SVIE', file_name):
            ftp.set_pasv(False)
        ftp.cwd(f'/DSK1/SSN/LOG1_15s_24hr/{filedir_name}')
        with open(file_name, 'wb') as fhandle:
            ftp.retrbinary(f'RETR {file_name}', fhandle.write)
        file_downloaded = True
    except Exception as e:
        print(f"Failed to download {file_name}: {e}")
    finally:
        ftp.quit()
    return file_downloaded

def archive_file(file_name, formatted_file_name, archive_path_dict, tmp_dir, year):
    """
    Moves the downloaded file from a temporary directory to the archive directory.

    Args:
        file_name (str): The name of the file in the temporary directory.
        formatted_file_name (str): The name for the file in the archive directory.
        archive_path_dict (dict): A dictionary containing the components of the archive path.
        tmp_dir (str): The temporary directory where the file is initially downloaded.
        year (int): The year associated with the file.

    Returns:
        bool: True if the file was successfully archived, False otherwise.
    """
    file_archived = False
    if not os.path.isdir(archive_path_dict['full_path']):
        make_directory(archive_path_dict)
    source_path = os.path.join(tmp_dir, file_name)
    destination_path = os.path.join(archive_path_dict['full_path'], formatted_file_name)
    if not os.path.isfile(destination_path):
        shutil.move(source_path, destination_path)
        file_archived = True
    else:
        print(f" >> File {destination_path} already exists!")
    return file_archived

def get_archive_path(doyo, year, station_id):
    """
    Generates the path to the archive based on the day of the year, year, and station ID.

    Args:
        doyo (int): Day of the year.
        year (int): Year for the archive path.
        station_id (str): Station ID for the archive path.

    Returns:
        dict: A dictionary containing the components and the full path to the archive.
    """
    month_dict = {
        '01': 'jan', '02': 'feb', '03': 'mar', '04': 'apr',
        '05': 'may', '06': 'jun', '07': 'jul', '08': 'aug',
        '09': 'sep', '10': 'oct', '11': 'nov', '12': 'dec'
    }
    file_date = gpstime.toDatetime(f"{year}-{doyo}", "%Y-%j")
    month = month_dict[file_date.strftime("%m")]
    full_path = f"/data/{year}/{month}/{station_id}/15s_24hr/raw/"
    archive_path_dict = {
        'root': '/data',
        'year': year,
        'month': month,
        'station_id': station_id,
        'frequency': '15s_24hr',
        'data_type': 'raw',
        'full_path': full_path
    }
    return archive_path_dict

def get_file_name(doyo, year, station_id):
    """
    Generates a file name based on the day of the year, year, and station ID.

    Args:
        doyo (int): Day of the year.
        year (int): Year for the file name.
        station_id (str): Station ID to include in the file name.

    Returns:
        str: The generated file name.
    """
    file_date = gpstime.toDatetime(f"{year}-{doyo}", "%Y-%j")
    return f"{station_id}{year}{file_date.strftime('%m%d')}0000a.sbf.gz"

def make_directory(archive_path_dict):
    """
    Creates the archive directory based on the provided path dictionary.

    Args:
        archive_path_dict (dict): A dictionary containing the components of the archive path.

    Returns:
        None: This function does not return any values but creates directories as needed.
    """
    root = archive_path_dict['root']
    for folder in [archive_path_dict['year'], archive_path_dict['month'], archive_path_dict['station_id'], archive_path_dict['frequency'], archive_path_dict['data_type']]:
        root = os.path.join(root, folder)
        if not os.path.isdir(root):
            os.makedirs(root)

def program_info_screen():
    """
    Prints software information.
    """
    print('')
    print("Copyright (c) 2016 Icelandic Met Office")
    print("getLeica 0.1 (Jul 2016)")
    print('')

def exit_gracefully(signum, frame):
    """
    Handles a graceful exit when Ctrl-C is pressed.

    Args:
        signum (int): Signal number.
        frame (frame): Current stack frame.

    Returns:
        None: This function does not return any values but exits the program if the user confirms.
    """
    original_sigint = signal.getsignal(signal.SIGINT)
    signal.signal(signal.SIGINT, original_sigint)
    try:
        if input("\nReally quit? (y/n)> ").lower().startswith('y'):
            sys.exit(1)
    except KeyboardInterrupt:
        print('Ok ok, quitting')
        sys.exit(1)
    signal.signal(signal.SIGINT, exit_gracefully)

#def sync_data(sta, start=None, end=None, session="15s_24hr", ffrequency="24hr", afrequency="15s", clean_tmp=True, sync=False, compression=".gz"):
#    """
#    This is the main loop in the program.. and could be moved to the main loop: REFACTORING
#    
#    1) Takes in the number of days to check backwards
#    2) Loops backwards, calls check_for_file and collects the files that are missing in a list
#    3) Loops through the list and downloads the files into a temp directory
#    """
#    
#    from datetime import datetime as dt
#    from datetime import timedelta as td
#
#    import cparser
#    import re
#    import os
#    
#    from gtimes.timefunc import currDatetime
#
#    print(("Start: {}, end: {}".format(start, end)))
#
#    # Get date today
#    station_id = sta 
#    
#    # handling default Time
#    hoursession = re.compile("1hr",re.IGNORECASE)
#    if ffrequency.lower == "1hr": # for downloading hourly data
#        if not end:
#            end =  (dt.now() - td(hours=1))
#        end = end.replace(minute=0, second=0, microsecond=0)
#    else: # Daily data
#        if not end:
#            end = currDatetime(-1)
#        end = end.date()
#
#    if hoursession.search(session): # for downloading hourly data
#        if not start:
#            start = end - td(hours=24)
#        start = start.replace(minute=0,second=0, microsecond=0)
#    else: # and for daily
#        if not start:
#            start = end - td(days=10)
#        start = start.date()
#
#
#
#    today = gt.currDatetime()
#    today_fancy = today.strftime("%A %d. %B %Y")
#    today_start_time = today.strftime("%H:%M:%S")
#
#    # Time the process
#    start_time = time.time()
#    
#
#    download_file_dict = {}
#    tmp_dir = "/home/gpsops/tmp/download/{}/".format(station_id)
#
#    predir="/DSK1/SSN/"
#    #session="LOG1_15s_24hr"
#    sessionn = "0"
#    sessionl = "a"
#    suffix = "sbf.gz"
#
#
#    parser = cparser.Parser()
#    station_info = parser.getStationInfo(station_id.upper())
#    if station_info:
#        ip_number = station_info["router"]["ip"]
#        print(ip_number)
#        ip_port = station_info['receiver']['ftpport']
#        print(("USING CPARSER: station {0} has IP:FTP_PORT {1}:{2}".format(station_id, ip_number, ip_port)))
#    else:
#        print('')
#        print(('__main__ ERROR: Unknown station ID {0}. Use "info" to query station info.'.format(station_id)))
#        exit()
#
#    # Quick fix as ftp may not be passive for imo APN server should go into config
#    regexp = re.compile("10\.4\.1")
#
#    if regexp.search(ip_number):
#        pasv = False
#        print(("SET pasv=False for IP: {}".format(ip_number)))
#    else:
#        pasv = True
#
#    # Boolean switches for function execution success
#    downloaded_files_dict = {}
#    file_archived = False
#
#    
#    #--------------------------------#
#    # 2) Create the temp directory if not already existing
#    #--------------------------------#
#
#    if os.path.isdir(tmp_dir):
#        pass
#    else:
#        print("STATUS > Temp directory {0} for downloading is missing".format(tmp_dir))
#        print("         creating it ....")
#        os.mkdir(tmp_dir)
#
#
#    #--------------------------------#
#    # 3) Print report header
#    #--------------------------------#
#
#    print("Program run on {}".format(today_fancy))
#    print("Time started: {}".format(today_start_time))
#    print("Current day number (doy): {}".format(gt.DayofYear())) 
#    print("checking for {0} sessions: from {1} to {2}".format(session, start, end))
#
#
#    #print(make_file_name(station_id, gt.currDatetime(-2), session, receiver_type="POLARX5", ftype="IMOstd"))
#    stringformat = "#datelist"
#    lfrequency = "1D"
#    file_datetime_list = gt.datepathlist(stringformat, lfrequency, starttime=start, endtime=end, datelist=[], closed=None)
#
#    stringformat = "/data/%Y/#b/{0}/{1}/raw/{0}%Y%m%d%H00a.sbf{2}".format(sta, session, compression)
#    archive_file_list = gt.datepathlist(stringformat, lfrequency, datelist=file_datetime_list, closed=None)
#    print(archive_file_list)
#
#    stringformat1 = "{}#Rin2_{}".format(sta,compression)
#    IGS_file_name_list = gt.datepathlist(stringformat1, lfrequency, datelist=file_datetime_list, closed=None)
#    file_date_dict = dict(list(zip(file_datetime_list, list(zip(archive_file_list, IGS_file_name_list)) )))
#
#    # checking if file is in archive
#    print("constructing a list for files missing from archive")
#    #missing_file_dict = { key:value for (key,value) in file_date_dict.items() if not os.path.isfile(value[0]) }
#    missing_file_dict = { key:value for (key,value) in list(file_date_dict.items()) }
#    
#    if len(list(missing_file_dict.keys())) == 0:
#        print('*-------------------------------------------------------------------------*')
#        print("")
#        print("STATUS > Archive is up to date.")
#        sync = False
#    else:
#        print('*-------------------------------------------------------------------------*')
#        print("")
#        print("STATUS > Missing files: ")
#        for key,value in list(missing_file_dict.items()):
#            print(("{0}: {1}".format(key,value) ))
#        print("")
#
#
#    if sync:
#
#
#        print((Session(session)[1]))
#        stringformat2 = "{}{}/%y%j/".format(predir,Session(session)[1])
#        print(stringformat2)
#        remote_path_list = gt.datepathlist(stringformat2, lfrequency, datelist=list(missing_file_dict.keys()), closed=None) 
#
#        # packing files and paths in a dict for downloading
#        download_file_dict = dict(list(zip( list(zip(*list(missing_file_dict.values())))[1], remote_path_list )))
#
#        # Connecting to server
#        ftp = ftp_open_connection(ip_number,ip_port,pasv=pasv, timeout=10)
#        print( " >> Now downloading and archiving missing files ...")
#        downloaded_files_list = ftp_download(download_file_dict, tmp_dir, clean_tmp=clean_tmp, ftp=ftp, ftp_close=True)
#
#        downloaded_files_dict = dict(list(zip( missing_file_dict, downloaded_files_list)))
#
#        #archiving
#        if downloaded_files_dict:
#            for ddate , tmp_file in list(downloaded_files_dict.items()):
#                print(("File to archive {}".format(os.path.basename(tmp_file))))
#                tmp_file_size = os.path.getsize(tmp_file)
#
#                if os.path.isfile(missing_file_dict[ddate][0]):
#                    archive_file_size = os.path.getsize(missing_file_dict[ddate][0])
#
#                    if tmp_file_size == archive_file_size:
#                        print(("Files dated {0}:\n {1} and {2}\nhave the same size {3} bytes.\nAborting"
#                                .format(ddate, tmp_file, missing_file_dict[ddate][0], tmp_file_size)))
#                else:
#                    archive_path, archive_file_name =  os.path.split(missing_file_dict[ddate][0]) 
#                    if not os.path.isdir(archive_path):
#                        print(("Directory {0} does not exist creating it ...".format(archive_path)))
#                    print(("Move file dated {0} from {1} to {2}".format(ddate, tmp_file, missing_file_dict[ddate][0])))
#                    os.rename(tmp_file,missing_file_dict[ddate][0])
#                    archive_file_size = os.path.getsize(missing_file_dict[ddate][0])
#                    if tmp_file_size == archive_file_size:
#                        print("File succsessfully moved")
#
#            
#        if file_archived:
#            print("STATUS > File downloaded and archived!")
#        else:
#            print("STATUS > Error in downloading and archiving. File might be missing on the receiver.")
#
#    #--------------------------------#
#    # 5) Output end time
#    #--------------------------------#
#
#    today_end_time = today.strftime("%H:%M:%S")
#    print("")
#    print("PROCESS DURATION: {0:.2f} seconds".format(time.time()-start_time))
#    return downloaded_files_dict
#
#def Session(session):
#    """
#    """
#
#    Session = {
#            "15s_24hr": ("a","LOG1_15s_24hr"),
#            "1Hz_1hr":  ("b","LOG2_1Hz_1hr"),
#            }
#
#    return Session[session]
#
#def make_file_name(station_id, day, session="15s_24hr", receiver_type="POLARX5", ftype="IMOstd", compression=".gz"):
#    """
#    """
#
#    import gtimes.timefunc as gt
#    import re
#
#    file_name = ""
#    suff_dict={
#            "POLARX5": "sbf",
#            }
#
#    
#    daysession = re.compile("24hr",re.IGNORECASE)
#    hoursession = re.compile("1hr",re.IGNORECASE)
#    
#    if ftype == "IMOstd":
#
#        print(("Session name: {}".format(session)))
#        if daysession.search(session): filedate = day.strftime("%Y%m%d0000a")
#
#        if hoursession.search(session): filedate = day.strftime("%Y%m%d%H00b")
#
#        file_name = "{0}{1}.{2}{3}".format(station_id, filedate, suff_dict[receiver_type], compresssion)
#
#    if not file_name:
#        print(("The fromat {0} is unknown".format(ftype)))
#        
#    return file_name
#
#
#def ftp_open_connection(ip_number,ip_port,pasv=True, timeout=10):
#
#    """
#        open ftp connection
#    """
#
#    from ftplib import FTP
#    
#    ## Try to connect to the server
#
#   # TEMP stuff sometimes we need passive ftp will go to config
#
#    try:
#        print("Connection to station...")
#        ftp = FTP()
#        ftp.connect(ip_number, ip_port, timeout=timeout)
#        ftp.login('anonymous')
#        ftp.set_pasv(pasv)
#        print("Connection successful!")
#    except: 
#        print("Connection failed")
#
#        ftp = None 
#
#    return ftp
#
#
#def ftp_download(files_dir_to_download_dict, local_dir, clean_tmp=True,
#                 ftp=None, ip_number=None, ip_port=None,  pasv=True, ftp_close=True):
#    """
#    download a list of files from an ftp server
#    """
#
#    import os
#    import re
#    from ftplib import FTP
#
#    if not ftp:
#        ftp = ftp_open_connection(ip_number ,ip_port, pasv=pasv)
#
#    if not ftp:
#        print(( "Can't connect to {}:{}, nothing downloaded".format(ip_number ,ip_port) ))
#        return []
#  
#    downloaded_files = []
#    remote_file_size = {}
#
#    # Execute file download if connection was succsesfull 
#    for file_name, remote_dir in sorted(list(files_dir_to_download_dict.items()),reverse=True):
# 
#        print("=====================================")
#        print(("File name: {}".format(file_name)))
#        print(("Remote directory: {}".format(remote_dir)))
#        print(("Download directory: {}".format(local_dir)))
#        print("-------------------------------------")
#        print(">")
#
#
#        local_file = "{0}{1}".format(local_dir,file_name)
#        if clean_tmp is True and os.path.isfile(local_file):
#            os.remove(local_file)
#
#        remote_file= "{0}{1}".format(remote_dir,file_name)
#    
#        offset = 0 
#        if os.path.isfile(local_file):
#            # check how much has alread been downloaded
#                offset = os.path.getsize(local_file)
#
#        
#        # Download the file
#        print('Downloading ' + file_name)
#
#        # remote_file
#        try:
#            remote_file_size = ftp.size(remote_file)
#        except:
#                remote_file_dict = ftp_list_dir([remote_dir], ftp=ftp, ftp_close=False)
#                print(remote_file_dict)
#                basename = file_name[0:11]
#                base_regexp = re.compile(basename)
#
#                
#                print(("File {} not on recever listing remote files".format(remote_file)))
#                print(">>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>")
#                for rdir, rfile_list in list(remote_file_dict.items()):
#                    for rfile in rfile_list:
#                        print(rfile) 
#                print(">>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>")
#                print(">")
#
#                for rdir, rfile_list in list(remote_file_dict.items()):
#                    for rfile in rfile_list:
#                        file_name=rfile.split()[-1]
#                        
#                        local_file = "{0}{1}".format(local_dir,file_name)
#                        if os.path.isfile(local_file):
#                            # check how much has alread been downloaded
#                            offset = os.path.getsize(local_file)
#    
#                        if base_regexp.search(file_name):
#                            remote_file="{0}{1}".format(rdir,file_name)
#                            print(("Found file {0} on receiver will download to \n {1}".format(remote_file, local_file) +
#                                  " File will not be archived automatically." )) 
#                            remote_file_size = ftp.size(remote_file)
#                            diff = _download_with_progressbar(ftp, remote_file,local_file, remote_file_size, offset=offset)
#                        else:
#                            print(("Did not find any file matching {0} on the receiver, \n".format(basename) + 
#                                  "check if the receiver or station info is configured correctly"))
#                    
#                
#                continue
#
#        diff = _download_with_progressbar(ftp, remote_file,local_file, remote_file_size, offset=offset)
#        print(("Difference between remote and downloaded file: {0:d}".format(diff)))
#        if diff == 0:
#            downloaded_files.append(local_file)
#
#    if ftp_close:
#        ftp.close()
#
#    return downloaded_files 
#
#
#def ftp_list_dir(dir_list, ftp, ip_number=None, ip_port=None, pasv=True, ftp_close=True):
#    """
#    """
#
#    import os
#    import re
#    from ftplib import FTP
#
#    if not ftp:
#        ftp = ftp_open_connection(ip_number ,ip_port, pasv=pasv)
#
#    if not ftp:
#        print(( "Can't connect to {}:{}, nothing downloaded".format(ip_number ,ip_port) ))
#        return []
#    
#    remote_file_dict = {}
#    for remote_dir in dir_list:
#        remote_dir_list=[]
#        ftp.dir(remote_dir, remote_dir_list.append)
#        remote_file_dict[remote_dir] = remote_dir_list
#    
#
#    if ftp_close:
#        ftp.close()
#
#    return remote_file_dict
#
#
#def is_gz_file(filepath):
#    """
#    Check if a file is a gzip file
#    """
#
#    import binascii
#    
#    with open(filepath, 'rb') as test_f:
#        return binascii.hexlify(test_f.read(2)) == b'1f8b'
#
#
#def _download_with_progressbar(ftp, remote_file,local_file, remote_file_size, offset=0):
#    """
#    Download a file using a process bar. 
#    Returns a the difference in bytes between the remote file and the downloaded file
#    """
#
#    import progressbar
#    
#    progress = progressbar.AnimatedProgressBar(start=offset,end=remote_file_size, width=50)
#
#    with open(local_file, 'ab') as f:
#        def callback(chunk):
#            f.write(chunk)
#            progress + len(chunk)
#
#            # Visual feedback of the progress!
#            progress.show_progress()
#
#        ftp.retrbinary('RETR {0}'.format(remote_file), callback,rest=offset)
#        print("")
#    # print( remote_file_size )
#    local_file_size = os.path.getsize(local_file)    
#
#    return local_file_size-remote_file_size
#
#
#def program_info_screen():
#    ''' Print software info.'''
#    # Only splash screen info here
#
#    current_func = sys._getframe().f_code.co_name + '() >> '
#
#    print('')
#    print("Copyright (c) 2016 Icelandic Met Office")
#    print("getLeica 0.1 (Jul 2016)")
#    print('')
#
#def exit_gracefully(signum, frame):
#    ''' Exit gracefully on Ctrl-C '''
#
#    current_func = sys._getframe().f_code.co_name + '() >> '
#
#    # restore the original signal handler as otherwise evil things will happen
#    # in raw_input when CTRL+C is pressed, and our signal handler is not re-entrant
#    signal.signal(signal.SIGINT, original_sigint)
#
#    try:
#        if input("\nReally quit? (y/n)> ").lower().startswith('y'):
#            sys.exit(1)
#
#    except KeyboardInterrupt:
#        print('Ok ok, quitting')
#        sys.exit(1)
#
#    # restore the exit gracefully handler here
#    signal.signal(signal.SIGINT, exit_gracefully)
#
#    # Method borrowed from:
#    # http://stackoverflow.com/questions/18114560/python-catch-ctrl-c-command-prompt-really-want-to-quit-y-n-resume-executi
#
##def main():
##    ''' main '''
##
##
##    import re
##    from datetime import datetime as dt
##    from datetime import timedelta as td
##
##    from gtimes.timefunc import currDatetime
##
##    #start = end = None
##    dstr="%Y%m%d-%H%M" # Default input string
##
##    # Display some nice program info
##    program_info_screen()
##
##    # Instantiate argparser
##    parser = argparse.ArgumentParser()
##
##    # Setup the argument parser
##    parser.add_argument('Stations', nargs='+',
##                        help='List of stations to download')
##    parser.add_argument('-D', '--days', type=int, default=10,
##                        help="Number of days back to check for data.")
##    parser.add_argument('-s','--start', type=str , default=None,
##                        help="Start date, format ""%%Y%%m%%d-%%H%%M"".")
##    parser.add_argument('-e','--end', type=str , default=None, 
##                        help="End date, format ""%%Y%%m%%d-%%H%%M"".")
##    parser.add_argument('-se', '--session', type=str, default='15s_24hr',
##                        help="Data sampling sessions. Default is 15s_24hr, 1Hz_1hr, 20HZ_1hr.")
##    parser.add_argument('-comp', '--compression', type=str, default='.gz',
##                        help="Sefine compression type")
##    parser.add_argument('-ffr', '--ffrequency', type=str, default='',
##                        help="Data file frequency, defaults to empty string and will try to determain it from session string")
##    parser.add_argument('-afr', '--afrequency', type=str, default='',
##                        help="Aqusition frequency, defaults to empty string and will try to determain it from session string")
##    parser.add_argument('-sy', '--sync', action='store_true',
##                        help='Sync new or partal files from source.')
##    parser.add_argument('-cl', '--clean_tmp', action='store_true',
##                        help='Clean download directory and start over on partly finished downlands')
## 
##    # Fetch the arguments
##    args = parser.parse_args()
##
##    # defining sub-periods
##    if args.start: # start the plot at
##       args.start = dt.strptime(args.start,dstr)
##    if args.end: # end the plot at
##        args.end = dt.strptime(args.end,dstr)
##
##    if not args.start and args.days:
##       args.start = currDatetime(days=-args.days, refday=dt.now())
##
##    # handling aqcustions frequency 
##    if args.afrequency:
##        pass
##    else:
##        args.afrequency = args.session.split("_")[0]
##    
##    # Handling file frequency
##    if args.ffrequency:
##        pass
##    else:
##        args.ffrequency = args.session.split("_")[1]
##
##
##
##    stations = args.Stations
##    kwargs = vars(args) 
##
##    del(kwargs['days'])
##    del(kwargs['Stations'])
##    
##    #print("ARGS: {}".format(kwargs))
##    for sta in stations:
##        sync_data(sta, **kwargs)
##
##
##if __name__ == '__main__':
##    # This is used to catch Ctrl-C exits
##    original_sigint = signal.getsignal(signal.SIGINT)
##    signal.signal(signal.SIGINT, exit_gracefully)
##
##    main()
