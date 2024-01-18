"""
This module contains functions for reading and returning GPS data. It includes the following functions 

"""

import numpy as np
import logging
from typing import List, Optional, Union

#
# time series filtering
#

def line(x: Union[int, float], p0: Union[int, float], p1: Union[int, float]) -> Union[int, float]:
    """
    Linear function for detrending timeseries without considering their oscillatory nature.

    Examples:
        >>> line(1, 0, 1)
        1

    Args:
        x (Union[int, float]): Input value in yearf or ordinal (or any numeric time)
        p0 (Union[int, float]): Intercept
        p1 (Union[int, float]): Slope

    Returns:
        Union[int, float]: Output value

    """
    return p0 + p1 * x


def lineperiodic(x: float, p0: float, p1: float, p2: float, p3: float, p4: float, p5: float) -> Optional[float]:
    """
    Linear function with a periodic superimposed

    Examples:
        >>> lineperiodic(1, 0, 1)
        1

    Args:
        x: Input value in yearf or ordinal (or any numeric time)
        p0: Intercept
        p1: Slope of linear term
        p2: Slope of cosine semiannual term
        p3: Slope of sine semiannual term
        p4: Slope of cosine annual term
        p5: Slope of sine annual term

    Returns:
        Output value

    """

    import numpy as np

    return (
        p0
        + p1 * x
        + p2 * np.cos(2 * np.pi * x)
        + p3 * np.sin(2 * np.pi * x)
        + p4 * np.cos(4 * np.pi * x)
        + p5 * np.sin(4 * np.pi * x)
    )


def periodic(x: float, p0: float, p1: float, p2: float, p3: float, p4: float, p5: float)->float:
    """
    Periodic function without the linear part

   
    Examples:
        >>> periodic(1, 0, 1, 1, 1, 1, 1)
        

    Args:
        x: Input value in yearf or ordinal (or any numeric time)
        p0: Coefficient
        p1: Coefficient
        p2: Coefficient
        p3: Coefficient
        p4: Coefficient 
        p5: Coefficient

    Returns:
        Output value

    """

    import numpy as np

    return (
        p2 * np.cos(2 * np.pi * x)
        + p3 * np.sin(2 * np.pi * x)
        + p4 * np.cos(4 * np.pi * x)
        + p5 * np.sin(4 * np.pi * x)
    )


def xf(x: float, p0: float, p1: float, p2: float, tau=4.8 ) -> float:

    """
    Linear + exponential function with constant tau coefficient

    Examples:
        >>> xf(1, 0, 1, 1, 1)

    Args:
        x: Input value in yearf or ordinal (or any numeric time)
        p0: Intercept
        p1: Slope
        p2: Exponential term coefficient
        tau: Exponential coefficient

    Returns:
        y: Output value


    """
    import numpy as np

    return p0 + p1 * x + p2 * np.exp(-tau * x)


def expxf(x: float, p0: float, p1: float, p2: float, p3: float)-> float:
    """

    Linear + exponential function with variable coefficient

    Examples:
        >>> expxf(1, 0, 1, 1, 1)

    Args:
        x: Input value in yearf or ordinal (or any numeric time)
        p0: Intercept
        p1: Slope
        p2: Exponential term coefficient
        p3: Exponential coefficient

    Returns:
        y: Output value

    """

    import numpy as np

    return p0 + p1 * x + p2 * np.exp(-p3 * x)


def expf(x, p0, p1, p2):
    """ 
    Exponential function 

    """
    import numpy as np

    return p0 + p1 * np.exp(-p2 * x)


def gpsvelo_df():
    """
    Dataframe for pygmt velo with three extra columns
    for date, period and boolean for vertical component.
    This is based on the output of the gpsvelo function, which estimates the gps velocity for a specific period of time.

    Examples:
        >>> gpsvelo_df()

    Returns:
        gpsvelo: Dataframe


    """
    import pandas as pd

    gpsvelo = pd.DataFrame(
        columns=[
            "longitude",
            "latitude",
            "east_velo",
            "north_velo",
            "east_sigma",
            "north_sigma",
            "coorelation_EN",
            "Station",
            "date",
            "period",
            "vertical",
        ],
    )

    return gpsvelo


def gpsvelo(sta: str, ll, vel, vertical=False, vfile=None, pheader=False):
    """
    Return gps velocities gmt velo

    Examples:
        >>> gpsvelo()

    Args:
        sta: Station name
        ll: [longitude, latitude]
        vertical: Boolean to describe
        vfile: Velocity file
        pheader: Header

    Returns:
        gpsvelo: Dataframe

    """

    gpsvelo = "{0:5.6f} {1:5.6f}\t{2:7.2f} {5:7.2f}\t{3:7.2f} {6:7.2f}\t{4:7.2f} {7:7.2f}\t\t{8:s}".format(
        ll[1], ll[0], vel[0], vel[1], vel[2], vel[3], vel[4], vel[5], sta
    )


def getDetrFit(
    STA: str,
    useSTA=None,
    useFIT=None,
    onlyPeriodic=False,
    detrFile="detrend_itrf2008.csv",
    logging_level=logging.WARNING):

    """ 
    This function defines the type of detrending to be applied. It is based on the detrending parameters file, detrFile, which is stored in the gpsconfig directory of the gpsplot server.

    Examples:
        >>> getDetrFit('GRIC', useSTA=None, useFIT=None, onlyPeriodic=False, detrFile='detrend_itrf2008.csv')

    Args:
        STA: Station name
        useSTA: Station name
        useFIT: Fit name
        onlyPeriodic: Boolean
        detrFile: Detrending file name, csv format



    """

    import logging
    import numpy as np
    import pandas as pd

    # import cparser as cp
    from cparser import ConfigParser
    
    # Create an instance for the ConfigParser
    config = ConfigParser()

    # Handling logging
    logging.basicConfig(
        format="%(asctime)-15s [%(levelname)s] %(funcName)s: %(message)s",
        level=logging_level,
    )

    logging.getLogger().setLevel(logging_level)
    module_logger = logging.getLogger()

    # Read the detrending file
    North = ["Nrate", "Nacos", "Nasin", "Nscos", "Nssin"]
    East = ["Erate", "Eacos", "Easin", "Escos", "Essin"]
    Up = ["Urate", "Uacos", "Uasin", "Uscos", "Ussin"]

    # Read the detrending file
    #Headers
    Info = ["Sitename", "Starttime", "Endtime", "UseSTA", "Fit"]
    columns = North + East + Up + Info

    # Grab the station name from the station.cfg file
    sta_name = config.getStationInfo(STA)["station"]["station_name"]

    # Initialize the table as an array with nan values
    data = [[np.nan] * 15 + [sta_name, np.nan, np.nan, np.nan, np.nan]]

    # convert to dataframe
    table = pd.DataFrame(data, index=[STA], columns=columns)

    # Read the detrending file
    try:
        table = pd.read_csv(detrFile, index_col="STA")
    except pd.errors.EmptyDataError:
        module_logger.warn("{} does not contain any data".format(detrFile))
    except FileNotFoundError:
        module_logger.warn("Detrend file not found")

    module_logger.info("Existing detrend constant table:\n{}".format(table))

    # Set the fit constants from the file within const variable
    try:
        const = pd.DataFrame(index=[STA], columns=columns)
        const.loc[STA] = tuple(table.loc[STA].values)
    except KeyError:
        module_logger.warn("{} not in table making an empty row".format(STA))
        const = pd.DataFrame(data, index=[STA], columns=table.columns)

    # Set the fit constants from the other station fit
    if useSTA:
        module_logger.warn(
            "Setting {0} {1} constants as {1} parameters for {2}".format(
                useSTA, useFIT, STA
            )
        )
        module_logger.info("current {} constants are:\n {} ".format(STA, const))

        # Set the fit constants if the fit is done from another station
        const.loc[STA, ["UseSTA", "Fit"]] = useSTA, useFIT

        # Set the fit constants
        if useFIT == "periodic":
            const.loc[STA, North[1:] + East[1:] + Up[1:]] = table.loc[
                useSTA, North[1:] + East[1:] + Up[1:]
            ]
        elif useFIT == "lineperiodic":
            const.loc[STA, North + East + Up] = table.loc[
                useSTA, North + East + Up
            ]
        elif useFIT == "line":
            const.loc[STA, North[:1] + East[:1] + Up[:1]] = table.loc[
                useSTA, North[:1] + East[:1] + Up[:1]
            ]

        module_logger.info("New parameters for {} are:\n {}".format(STA, const))

    # Set the linear part of the fit constants as nan for periodic only fit
    if onlyPeriodic is True:
        const["Nrate"] = const["Erate"] = const["Urate"] = np.nan

    return const

def convconst(const, pb=None):
    """
    This function converts detrending constants from pandas dataframe to list of the form
    [[], [], []] for optimize.curv_fit

    Examples:
        >>> convconst()

    Args:
        const: detrend constants dataframe
        pb: Periodic constants

    Returns:
        const: detrending constants

    """


    import numpy as np

    North = ["Nrate", "Nacos", "Nasin", "Nscos", "Nssin"]
    East = ["Erate", "Eacos", "Easin", "Escos", "Essin"]
    Up = ["Urate", "Uacos", "Uasin", "Uscos", "Ussin"]

    if pb:
        # const = pd.DataFrame(data, index=[STA], columns=table.columns)
        stat = const.index.tolist()[0]
        for i, dimention in zip(range(3), [North, East, Up]):
            const.loc[stat, dimention] = list(pb[i][1:])

        return const

    else:
        if const[North].isna().sum(axis=1).values == 5:
            p0 = [None, None, None]
        else:
            p0 = [[], [], []]
            p0[0] = [0] + const[North].values.tolist()[0]
            p0[1] = [0] + const[East].values.tolist()[0]
            p0[2] = [0] + const[Up].values.tolist()[0]

            p0 = np.nan_to_num(p0)

        return p0


def save_detrend_const(const, detrFile="detrend_itrf2008.csv"):
    """
    This function saves constants in a file for detrending GPS stations

    Examples:
        >>> save_detrend_const(const, detrFile='detrend_itrf2008.csv')

    Args:
        const: detrending constants dataframe
        detrFile: detrending file name

    Returns:
        None


    """
    import pandas as pd
    from pathlib import Path

    North = ["Nrate", "Nacos", "Nasin", "Nscos", "Nssin"]
    East = ["Erate", "Eacos", "Easin", "Escos", "Essin"]
    Up = ["Urate", "Uacos", "Uasin", "Uscos", "Ussin"]
    Info = ["Sitename", "Starttime", "Endtime", "UseSTA", "Fit"]

    columns = North + East + Up + Info

    stationlist = const.index.values
    path = Path(Path.cwd(), detrFile)
    if not path.is_file():
        open(path, "w").close()

    try:
        table = pd.read_csv(detrFile, index_col="STA")
    except pd.errors.EmptyDataError:
        table = pd.DataFrame(index=["STA"], columns=columns)

    if all(table.isnull().all(1)):
        print("No data in file")
        const.to_csv(detrFile, mode="w", header=True, index_label="STA")

        return

    else:
        for stat in stationlist:
            if stat in table.index:
                print("Station {} already in table updating".format(stat))
                table.loc[stat, :] = const.loc[stat]
                print("Saving the new table")
                table.to_csv(detrFile, mode="w", header=True, index_label="STA")
            else:
                print("stations {} are not in detrend file, adding it".format(stat))
                table.loc[stat, :] = const.loc[stat]
                table.to_csv(detrFile, mode="w", header=True, index_label="STA")

        return


def fitdataframe(func, df, p0=[None, None, None]):
    """ 
    This function finds the fitting parameters for a dataframe of GPS time series through the scipy.optimize.curve_fit function

    Examples:
        >>> fitdataframe(line, df, p0=[None, None, None])

    Args:
        func: fitting function (line, periodic, lineperiodic, others)
        df: dataframe of GPS time series, with x in fractional year, y the components dN, dE or dU and yD, the uncertainties DN, DE, DU.
        p0: initial guess for the fitting parameters

    Returns:
        pb: fitting parameters
        pcov: covariance matrix
        
    """
    from scipy import optimize

    x = df["yearf"].to_numpy()
    y = df[["north", "east", "up"]].to_numpy().T
    yD = df[["Dnorth", "Deast", "Dup"]].to_numpy().T

    return fittimes(func, x, y, yD, p0=p0)


def fittimes(func, x, y, yD=[None, None, None], p0=[None, None, None]):

    from scipy import optimize

    pb = [[], [], []]
    pcov = [[], [], []]

    for i in range(3):
        pb[i], pcov[i] = optimize.curve_fit(
            func, x, y[i], p0=p0[i], sigma=yD[i], maxfev=100000
        )

    return pb, pcov


# routines to extract and save coordinates and time series from gamit


def gamittooneuf(sta, outFile, mm=True, ref="plate", dstring=None, outformat=True):
    """
    extract Gamit timeseries from standard format to one file formated time string

    Examples:
        >>> gamittooneuf('GRIC', outFile, mm=True, ref='plate', dstring=None, outformat=True)

    Args:
        sta: station four letter short name
        outFile: file object
        mm: boolean True return data in mm, else in m
        ref: subtract plate velocity from the time series.
        dstring: format of the time string (e.g dstring)="%Y%m%d-%H%M%S"), defaults to decimal year (yyyy.yyyy)


    Returns: #not finished but determines the output order of the data into the file
        .outformat file

    """
    # "%Y/%m/%d 12:00:00.000"

    NEUdata = gamittoNEU(sta, mm=mm, ref=ref, dstring=dstring)

    gamittoFile(NEUdata, outFile, mm=mm, ref=ref, dstring=dstring, outformat=outformat)


def gamittoFile(NEUdata, outFile, mm=True, ref="plate", dstring=None, outformat=True):
    """ 
    This function converts gamit timeseries files to NEU files

    Examples:
        >>> gamittoFile(NEUdata, outFile, mm=True, ref='plate', dstring=None, outformat=True)

    Args:
        NEUdata: NEU data
        outFile: file object
        mm: boolean True return data in mm, else in m
        ref: subtract plate velocity from the time series if = ref.
        dstring: format of the time string (e.g dstring)="%Y%m%d-%H%M%S"), defaults to decimal year (yyyy.yyyy)
        outformat: file format (True) or string format (False)

    Returns:
        .outformat file


    """

    # formatting time column
    if dstring == "yearf":
        timef = "{0: 8.4f}\t"
        timeh = "#\"yyyy.dddd'     "
    else:
        timef = " {0:s}\t"
        timeh = "#yyyy/mm/dd HH:MM:SS.SSS          "

    # unit conversion formatting
    if mm:
        if outformat:
            header = timeh + "dN[mm] DN[mm]\tdE[mm] DE[mm]\tdU[mm]  DU[mm]"
            formatstr = (
                timef + "{1: 7.2f} {4: 7.2f}\t{2: 7.2f} {5: 7.2f}\t{3: 7.2f} {6: 7.2f}"
            )
        else:
            header = timeh + "dN[mm]  dE[mm] dU[mm]\t\t  DN[mm]  DE[mm]  DU[mm]"
            formatstr = (
                timef
                + "{1: 7.2f} {2: 7.2f} {3: 7.2f}\t\t{4: 7.2f} {5: 7.2f}\t{6: 7.2f}"
            )
    else:
        if outformat:
            header = timeh + "dN[m] DN[m]\tdE[m] DE[m]\tdU[m]  DU[m]"
            formatstr = (
                timef + "{1: 7.5f} {4: 7.5f}\t{2: 7.5f} {5: 7.5f}\t{3: 7.5f} {6: 7.5f}"
            )
        else:
            header = timeh + "dN[m]    dE[m]    dU[m]          DN[m]   DE[m]    DU[m]"
            formatstr = (
                timef + "{1: 7.5f} {2: 7.5f} {3: 7.5f}\t{4: 7.5f} {5: 7.5f} {6: 7.5f}"
            )

    print('printing header and file \n', header, file=outFile)  

    # applying formatting to each column of the NEUdata file
    for x in NEUdata:
        print(
            formatstr.format(
                x["yearf"],
                x["data[0]"],
                x["data[1]"],
                x["data[2]"],
                x["Ddata[0]"],
                x["Ddata[1]"],
                x["Ddata[2]"],
            ),
            file=outFile,
        )


def savedisp(dataDict, fname=None, header=""):
    """ 
    This function saves a dictionary of data to a file

    Examples:
        >>> savedisp(dataDict, fname=None, header="")

    Args:
        dataDict: dictionary of data
        fname: file name
        header: header of the file

    Returns:
        output file

    """

    from collections import OrderedDict

    valtype = type(dataDict.values()[0])

    dataDict = OrderedDict(sorted(dataDict.items()))

    if (valtype is list) or (valtype is np.ndarray):
        fmt = "% 3.8f\t% 2.8f\t% 2.8f\t%s" # format

        
        ab = np.zeros(
            len(dataDict.keys()),
            dtype=[
                ("var1", "float"),
                ("var2", "float"),
                ("var3", "float"),
                ("var4", "a4"),
            ],
        )

        ab["var1"] = np.squeeze(dataDict.values())[:, 0]
        ab["var2"] = np.squeeze(dataDict.values())[:, 1]
        ab["var3"] = np.squeeze(dataDict.values())[:, 2]
        ab["var4"] = dataDict.keys()


    # formatting tuples into a dictionary of arrays
    if valtype is tuple:
        fmt = "% 3.8f\t% 2.8f\t% 2.8f\t%2.8f\t%2.8f\t%s"
        ab = np.zeros(
            len(dataDict.keys()),
            dtype=[
                ("var1", "float"),
                ("var2", "float"),
                ("var3", "float"),
                ("var4", "float"),
                ("var5", "float"),
                ("var6", "a4"),
            ],
        )
        ab["var1"] = np.squeeze(zip(*dataDict.values()[:])[0])[:, 0]
        ab["var2"] = np.squeeze(zip(*dataDict.values()[:])[0])[:, 1]
        ab["var3"] = np.squeeze(zip(*dataDict.values()[:])[1])[:, 0]
        ab["var4"] = np.squeeze(zip(*dataDict.values()[:])[1])[:, 1]
        ab["var5"] = np.squeeze(zip(*dataDict.values()[:])[1])[:, 2]
        ab["var6"] = dataDict.keys()

    if fname:
        np.savetxt(fname, ab, fmt=fmt, header=header)
    return ab


def extractfromGamitBakf(cfile, stations):
    """
    Function to extract data from a GAMIT .bak file

    Examples:
        >>> extractfromGamitBakf(cfile, stations)

    Args:
        cfile: .bak file name
        stations: station name

    Returns:
        slines: list of lines
    """
    import re

    slines = []

    site = re.compile(stations)
    tim = re.compile("Solution refers to", re.IGNORECASE)
    f = open(cfile, "r")

    for line in f:
        if site.search(line):  # or tim.search(line):
            slines.append(line.rstrip())

    return slines


def openGlobkTimes(STA, Dir=None, tType="TOT"):
    """
    Function to import data from Globk time series files into a numpy arrays

    Dir is the directory containing the time series if left blank the default path will be the path
    defined in the config file postprossesing.cfg, totPath

    Args:
        STA: Station four letter short name in captial letters
        Dir: optional alternative Directory of the GAMIT time series data.

    Returns:
    
        yearf: is array with time  (usually) in fractional year format (i.e. 2014.62328)
        data:  three arrays containing GPS data in north,east, up
        Ddata: respective uncertainty values

    """

    import os
    import numpy as np
    import datetime as dt
    from gtimes.timefunc import shifTime, TimetoYearf
    from cparser import ConfigParser
    config = ConfigParser()



    # Loading the data 
    # First, if no Dir is input, find the path in the Postprocess config file in the "totpath" instance
    if Dir is None:
        Dir = config.getPostprocessConfig("totpath")

    else: # This is still in development
        # print( os.path.isdir(Dir) )
        # check if the path given as argument indeed exists
        pass

    # constructing the full path filenames and parsing parameters
    # define the file name to be looked for into Dir
    filepre = "mb_{0:s}_{1:s}.dat".format(STA, tType)

    if os.path.isfile(os.path.join(Dir, filepre + "1")): #use dat1, dat2, dat3 as file format
        pass
    else: # use TOT as file format to read in data
        filepre = "mb_{0:s}_{1:s}.dat".format(STA, "TOT")

    # Construct the file names for each component
    Datafile1 = os.path.join(Dir, filepre + "1")
    Datafile2 = os.path.join(Dir, filepre + "2")
    Datafile3 = os.path.join(Dir, filepre + "3")

    # Load the data for files and store it in arrays. Use converters defined in the __converter functions
    yearf, d1, D1 = np.loadtxt(
        Datafile1, unpack=True, skiprows=3, converters={1: __converter, 2: __converter}
    )
    d2, D2 = np.loadtxt(
        Datafile2,
        usecols=(1, 2),
        unpack=True,
        skiprows=3,
        converters={1: __converter, 2: __converter},
    )
    d3, D3 = np.loadtxt(
        Datafile3,
        usecols=(1, 2),
        unpack=True,
        skiprows=3,
        converters={1: __converter, 2: __converter},
    )

    # Stack the arrays for the three components in the data array and for their uncertainties in Ddata array
    data = np.vstack([d1, d2, d3])
    Ddata = np.vstack([D1, D2, D3])

    # Option to grab 8hr subdaily solutions from the same path
    if tType == "08h":
        shift8h = dt.timedelta(**shifTime("H8"))
        yearf = np.array(
            [
                TimetoYearf(*(item + shift8h).timetuple()[:6])
                for item in toDateTime(yearf)
            ]
        )

    return yearf, data, Ddata


def open3DataFiles(STA, Dir=None, comp=["-N", "-E", "-U"]):
    """
    This function opens data contained in 3 files, one file for each component E, N and U

    Examples:
        >>> open3DataFiles(STA, Dir=None, comp=["-N", "-E", "-U"])

    Args:
        STA: Station four letter short name in capital letters
        Dir: optional alternative Directory of the files.
        comp: list of components to be read. Default is ["-N", "-E", "-U"]
        
    Returns:
        data:  three arrays containing GPS data in north, east and up

    """

    import os
    import pandas as pd

    if Dir is None:
        Dir = os.getcwd()

    compdict = {}
    compdict[comp[0]] = ["north", "Dnorth"]
    compdict[comp[1]] = ["east", "Deast"]
    compdict[comp[2]] = ["up", "Dup"]
    components = {"north": None, "east": None, "up": None}

    for item in compdict.keys():
        dfile = "{0}{1}".format(STA, item)
        components[compdict[item][0]] = pd.read_csv(
            dfile, sep=r"\s+", index_col=0, header=None, names=compdict[item]
        )

    columnreorder = ["north", "east", "up", "Dnorth", "Deast", "Dup"]
    data = pd.concat(components.values(), axis=1)[columnreorder]
    data.set_index(pd.DatetimeIndex(toDateTime(data.index)), inplace=True)
    data.index = data.index.round("1h")

    return data


def convGlobktopandas(yearf: float, data, Ddata):
    """
    This function converts Globk files (from OpenGlobkTimes function) into pandas dataframes

    Examples:
        >>> convGlobktopandas(yearf, data, Ddata)

    Args:
        yearf: is array with time  (usually) in fractional year format (i.e. 2014.62328)
        data:  three arrays containing GPS data in north, east and up
        Ddata: respective uncertainty values for each component 

    Returns:
           Index [datetime], north, east, up, Dnorth, Deast, Dup, yearf


    """

    import pandas as pd
    from collections import OrderedDict

    # reduce(lambda x, y: pd.merge(x, y, on = 'Date'), dfList)
    names = ["north", "east", "up", "Dnorth", "Deast", "Dup", "yearf"]

    # !!!!! from_item depricated will remove
    # data = pd.DataFrame.from_items(zip(names[:3],data))
    # data = data.join( pd.DataFrame.from_items(zip(names[3:],Ddata) ) )
    # Using from_dict instead
    data = pd.DataFrame.from_dict(OrderedDict(zip(names[:3], data)))
    data = data.join(pd.DataFrame.from_dict(OrderedDict(zip(names[3:], Ddata))))
    data["yearf"] = yearf
    data.set_index(pd.DatetimeIndex(toDateTime(yearf)), inplace=True)
    data.index = data.index.round("1h")

    return data


def compGlobkTimes(stalist="any", dirConFilePath=None, freq=None):
    """
    This function joins old and new mb_ time series files

    Examples:
        >>> compGlobkTimes(stalist="any", dirConFilePath=None, freq=None)

    Args:
        stalist: list of station names in capital letters. If "any", all stations are used. Default is "any"
        dirConFilePath: optional alternative Directory of the GAMIT time series data.
        freq: optional frequency of the data. Default is None

    Returns:
        data:  three arrays containing GPS data in north, east and up
    
    """
    import glob
    import sys
    import shutil
    import os
    from cparser import ConfigParser

    config = ConfigParser()

    #totpath = config.getPostprocessConfig('totpath')
    #import cparser as cp

    if dirConFilePath:  # for custom file
        Dirs = parsedir(dirConFilePath)
    else: # grab paths from the postprocess.cfg file in gpsconfig directory that cparser reads into a dictionary
        Dirs = {
                "figDir": config.get_config("Configs", "figDir"),
                "prePath": config.get_config("Configs", "prePath"),
                "rapPath": config.get_config("Configs", "rapPath"),
                "totPath": config.get_config("Configs", "totPath")
            }

        print('Directory is \n', Dirs)

    # Reading into a string the paths
    PrePath = Dirs["prePath"]
    RapPath = Dirs["rapPath"]
    TotPath = Dirs["totPath"]

    # Setting the frequency to TOT if freq is None
    if freq == "TOT" or freq is None:
        freq = "TOT"
    else: # setting the frequency
        PrePath = PrePath + "_%s" % (freq)
        RapPath = RapPath + "_%s" % (freq)

    if stalist == "any":
        FilePreL = os.path.join(PrePath, "mb_*.dat?")
        FileRapL = os.path.join(RapPath, "mb_*.dat?")

        List = glob.glob(FilePreL) + glob.glob(FileRapL)

        # listing all stations in  the Rap and Pre directories
        stalist = sorted(set([item[-13:-9] for item in List]))

    # Set up names for files
    for STA in stalist:
        FilePre = "mb_%s_?PS.dat" % STA
        OutFilePre = "mb_%s_GPS.dat" % STA
        GPS20PS = "mb_%s_0PS.dat" % STA

        for axes in range(1, 4):
            FilePreR = os.path.join(PrePath, FilePre + "%s" % (axes,))
            FileRapR = os.path.join(RapPath, FilePre + "%s" % (axes,))

            # graping the list for files for for that station
            PreFileL = glob.glob(FilePreR)  # listing files in the pre dir
            RapFileL = glob.glob(FileRapR)  # listing files in th Rap dir

            #  Sorting the file lists
            PreFileL.sort()
            if len(PreFileL) > 1:
                PreFileL.insert(0, PreFileL.pop(-1))
            RapFileL.sort()
            if len(RapFileL) > 1:
                RapFileL.insert(0, RapFileL.pop(-1))

            TotFile = os.path.join(TotPath, "mb_%s_%s.dat%s" % (STA, freq, axes))

            print("Concatenating all the %s data to %s" % (STA, TotFile))

            if os.path.exists(TotFile):
                os.remove(TotFile)

            outf = open(TotFile, "a")

            for fil in PreFileL:
                print("Processing file %s " % fil, file=sys.stderr)
                f = open(fil)
                f.seek(61)
                shutil.copyfileobj(f, outf)
                f.close()

            outf.close()

            preexist = os.stat(TotFile).st_size != 0
            if preexist:
                outf = open(TotFile, "r")
                lastline = outf.readlines()[-1]
                lastline = lastline.split()
                outf.close()

            outf = open(TotFile, "a")
            for file in RapFileL:
                formatstr = "Processing file {0:s} ".format(file)
                print(formatstr, file=sys.stderr)
                rapfile = open(file, "r")
                rapfile.seek(61)
                lines = rapfile.readlines()
                if preexist:
                    lines = "".join(
                        [line for line in lines if line.split()[0] > lastline[0]]
                    )
                else:
                    lines = "".join([line for line in lines])

            outf.close()


def TieTimes(sta1, sta2, dirConFilePath=None, freq=None, tie=[None, None, None]):
    """
    This function joins old and new mb_ time series files

    Examples:
        >>> TieTimes(sta1, sta2, dirConFilePath=None, freq=None, tie=[None, None, None])

    Args:
        sta1: first station name in capital letters
        sta2: second station name in capital letters
        dirConFilePath: optional alternative Directory of the GAMIT time series data.
        freq: optional frequency of the data. Default is None
        tie: optional tie file. Default is [None, None, None]


    """
    import glob
    import sys
    import shutil
    from cparser import ConfigParser
    config = ConfigParser()
    #totpath = config.getPostprocessConfig('totpath')

    if dirConFilePath:  # for custom file
        Dirs = parsedir(dirConFilePath)
    else:
        # As the standard configparser works with dictionaries, use it to create the Dirs dictionaries
        Dirs = {
        "figDir": config.get_config("Configs", "figDir"),
        "prePath": config.get_config("Configs", "prePath"),
        "rapPath": config.get_config("Configs", "rapPath"),
        "totPath": config.get_config("Configs", "totPath")
    }

    # parse the paths from the Dirs dictionary
    PrePath = Dirs["prePath"]
    RapPath = Dirs["rapPath"]
    TotPath = Dirs["totPath"]

    # Setting the frequency to TOT if freq is None
    if freq == "TOT" or freq is None:
        freq = "TOT"
    else:
        PrePath = PrePath + "_%s" % (freq)
        RapPath = RapPath + "_%s" % (freq)

    # for all the stations, create the path for PreL and RapL files
    if stalist == "any":
        FilePreL = os.path.join(PrePath, "mb_*.dat?")
        FileRapL = os.path.join(RapPath, "mb_*.dat?")

        List = glob.glob(FilePreL) + glob.glob(FileRapL)

        # listing all stations in  the Rap and Pre dir
        stalist = sorted(set([item[-13:-9] for item in List]))

    for STA in stalist:
        FilePre = "mb_%s_?PS.dat" % STA
        OutFilePre = "mb_%s_GPS.dat" % STA
        GPS20PS = "mb_%s_0PS.dat" % STA

        for axes in range(1, 4):
            FilePreR = os.path.join(PrePath, FilePre + "%s" % (axes,))
            FileRapR = os.path.join(RapPath, FilePre + "%s" % (axes,))

            # graping the list for files for for that station
            PreFileL = glob.glob(FilePreR)  # listing files in the pre dir
            RapFileL = glob.glob(FileRapR)  # listing files in th Rap dir

            #  Sorting the file lists
            PreFileL.sort()
            if len(PreFileL) > 1:
                PreFileL.insert(0, PreFileL.pop(-1))
            RapFileL.sort()
            if len(RapFileL) > 1:
                RapFileL.insert(0, RapFileL.pop(-1))

            TotFile = os.path.join(TotPath, "mb_%s_%s.dat%s" % (STA, freq, axes))
            print("Concating all the %s data to %s" % (STA, TotFile))
            if os.path.exists(TotFile):
                os.remove(TotFile)
            outf = open(TotFile, "a")
            for fil in PreFileL:
                print("Processing file %s " % fil, file=sys.stderr)
                f = open(fil)
                f.seek(61)
                shutil.copyfileobj(f, outf)
                f.close()
            outf.close()

            preexist = os.stat(TotFile).st_size != 0
            if preexist:
                outf = open(TotFile, "r")
                lastline = outf.readlines()[-1]
                lastline = lastline.split()
                outf.close()

            outf = open(TotFile, "a")
            for file in RapFileL:
                formatstr = "Processing file {0:s} ".format(file)
                print(formatstr, file=sys.stderr)
                rapfile = open(file, "r")
                rapfile.seek(61)
                lines = rapfile.readlines()
                if preexist:
                    lines = "".join(
                        [line for line in lines if line.split()[0] > lastline[0]]
                    )
                else:
                    lines = "".join([line for line in lines])

                outf.write(lines)
                rapfile.close()

            outf.close()


def TieTimes(sta1, sta2, dirConFilePath=None, freq=None, tie=[None, None, None]):
    """
    This function joins old and new mb_ time series files

    Examples:
        >>> TieTimes(sta1, sta2, dirConFilePath=None, freq=None, tie=[None, None, None])

    Args:
        sta1: first station name in capital letters
        sta2: second station name in capital letters
        dirConFilePath: optional alternative Directory of the GAMIT time series data.
        freq: optional frequency of the data. Default is None
        tie: optional tie file. Default is [None, None, None]

    Returns:
        None


    """
    import glob
    import sys
    import shutil

    from pandas import read_table
    import pandas as pd
    from cparser import ConfigParser
    config = ConfigParser()

    if dirConFilePath:  # for custom file
        Dirs = parsedir(dirConFilePath)
    else:
        Dirs = {
                "figDir": config.get_config("Configs", "figDir"),
                "prePath": config.get_config("Configs", "prePath"),
                "rapPath": config.get_config("Configs", "rapPath"),
                "totPath": config.get_config("Configs", "totPath")
            }


    # PrePath = Dirs['prePath'] - These paths are not used for now, but can be added later
    # RapPath = Dirs['rapPath'] - Same case as above
    TieFile = Dirs["tiefile"]
    TotPath = Dirs["totPath"]

    if freq == "TOT" or freq is None:
        freq = "TOT"
    else:
        PrePath = PrePath + "_%s" % (freq)
        RapPath = RapPath + "_%s" % (freq)

    print(TieFile)

    dtype = [
        ("North", "<f8"),
        ("East", "<f8"),
        ("Up", "<f8"),
        ("sta1", "|S5"),
        ("sta2", "|S5"),
    ]

    const = np.genfromtxt(TieFile, dtype=dtype)
    const = [i for i in const if i[3] == sta1 and i[4] == sta2]
    print(const)

    for axes in range(1, 4):
        TotFile1 = os.path.join(TotPath, "mb_%s_%s.dat%s" % (sta1, freq, axes))
        TotFile2 = os.path.join(TotPath, "mb_%s_%s.dat%s" % (sta2, freq, axes))
        print("Concating all the %s data to %s" % (sta1, TotFile2))
        # outf = open(TotFile, 'r')
        data1 = read_table(
            TotFile1, sep="\s+", header=None, index_col=0, names=["disp", "uncert"]
        )
        data2 = pd.read_csv(
            TotFile2, sep="\s+", header=None, index_col=0, names=["disp", "uncert"]
        )
        print(const[0][axes - 1])
        data2["disp"] -= const[0][axes - 1] / 1000
        data = pd.concat([data1, data2])
        

        outfile = os.path.join(TotPath, "mb_%s_%s.dat%s" % (sta2, "JON", axes))
        data.to_csv(outfile, sep="\t", index=True, header=False)


fitfuncl = lambda p, x: p[0] * x + p[1]
errfuncl = lambda p, x, y: fitfuncl(p, x) - y  # Distance to the target function

fitfunc = (
    lambda p, x: p[0] * x
    + p[1] * np.cos(2 * np.pi * x)
    + p[2] * np.sin(2 * np.pi * x)
    + p[3] * np.cos(4 * np.pi * x)
    + p[4] * np.sin(4 * np.pi * x)
    + p[5]
)
errfunc = lambda p, x, y: fitfunc(p, x) - y  # Distance to the target function


def fitline(yearf, data, STA):
    """
    This function fits a function through data points of a station STA

    Examples:
        >>> fitline(yearf, data, STA)

    Args:
        yearf: list of years
        data: list of data
        STA: station name

    Returns:
        parameters of the linear fitting


    """

    from scipy import optimize
    import numpy as np

    dtype = [
        ("Nrate", "<f8"),
        ("Erate", "<f8"),
        ("Urate", "<f8"),
        ("Nacos", "<f8"),
        ("Nasin", "<f8"),
        ("Eacos", "<f8"),
        ("Easin", "<f8"),
        ("Uacos", "<f8"),
        ("Uasin", "<f8"),
        ("Nscos", "<f8"),
        ("Nssin", "<f8"),
        ("Escos", "<f8"),
        ("Essin", "<f8"),
        ("Uscos", "<f8"),
        ("Ussin", "<f8"),
        ("shortname", "|S5"),
        ("name", "|S20"),
    ]

    const = np.genfromtxt("itrf08det", dtype=dtype)
    const = [i for i in const if i[15] == STA]

    pN = [const[0][0]]
    pE = [const[0][1]]
    pU = [const[0][2]]
    pN = [-1 * i for i in pN]
    pE = [-1 * i for i in pE]
    pU = [-1 * i for i in pU]
    # pN.append(0)
    # pE.append(0)
    # pU.append(0)

    # print "pN: %s" % p
    # print "pE: %s" % pE
    # print "pU: %s" % pU

    pb = [[0, 0], [0, 0], [0, 0]]

    # pb[0], success = optimize.leastsq(errfunc, pN[:], args=(yearf-yearf[0], data[0]))
    # pb[1], success = optimize.leastsq(errfunc, pE[:], args=(yearf-yearf[0], data[1]))
    # pb[2], success = optimize.leastsq(errfunc, pU[:], args=(yearf-yearf[0], data[2]))
    pb[0], success = optimize.leastsq(errfuncl, pb[0], args=(yearf, data[0]))
    pb[1], success = optimize.leastsq(errfuncl, pb[1], args=(yearf, data[1]))
    pb[2], success = optimize.leastsq(errfuncl, pb[2], args=(yearf, data[2]))

    return pN, pE, pU, pb


def pvel(pl, pcov):
    """ 
    This function prints the velocity for the three components and their uncertainty to numpy arrays

    Examples:
        >>> pvel(pl, pcov)

    Args:
        pl: list of the three components of the velocity and their uncertainties
        pcov: covariance matrix of the three components

    Returns:
        vel: list of the three components of the velocity
        vunc: list of the three components of the uncertainties
    """

    vunc = [None, None, None]
    vel = [None, None, None]

    for i in range(3):
        vel[i] = pl[i][1]
        vunc[i] = np.sqrt(np.diag(pcov[i]))[1]
        # print("{0:0.2f} {1:0.2f}".format( pl[i][1],vunc[i]) )

    return vel, vunc


def printvelocity(sta, ll, vel, vfile, pheader=False):
    """
    This function prints the velocity for a station to a file

    Examples:
        >>> printvelocity('GRIC', ll, vel, vfile)

    Args:
        sta: station name
        ll: list of the longitude and latitude
        vel: list of the three components of the velocity
        vfile: file to print the velocity
        pheader: print the header

    Returns:
        gpsvelo: string of the velocity

    """
    import os

    header = (
        "#lon       lat\t\t   N[mm]   DN[mm]  E[mm]  DE[mm]  U[mm]  DU[mm]\t\tStation"
    )

    if pheader is True:
        print(header, file=vfile)

    gpsvelo = "{0:5.6f} {1:5.6f}\t{2:7.2f} {5:7.2f}\t{3:7.2f} {6:7.2f}\t{4:7.2f} {7:7.2f}\t\t{8:s}".format(
        ll[1], ll[0], vel[0], vel[1], vel[2], vel[3], vel[4], vel[5], sta
    )

    print(gpsvelo, file=vfile)

    return gpsvelo


def detrend(
    x,
    y,
    Dy=None,
    fitfunc=lineperiodic,
    p=None,
    pcov=None,
    STA=None,
    onlyPeriodic=True,
    zref=False,
):
    """
    This function returns the detrending parameters for a specific fit function and station, for the GPS components

    Examples:
        >>> detrend(x, y, Dy, fitfunc=lineperiodic, p=None, pcov=None, STA='GRIC', onlyPeriodic=True, zref=False)

    Args:
        x: list of the years fractional for the timeseries
        y: list of the three components measurements for the timeseries
        Dy: list of the uncertainties of the three components
        fitfunc: fit function for the detrending. Default is lineperiodic
        p: list with initial guess for the fitting coefficients. Default is None.
        pcov: covariance matrix of the initial guess. Default is None.
        STA: station name, four letters in upper case. Default is None.
        onlyPeriodic: True or False. Default is True.
        zref: Reference z. Default is False. - Not implemented fully yet.

    Returns:
        


    """

    import numpy as np
    import geo_dataread.gps_read as gdrgps

    if Dy is None:
        Dy = np.ones(y.shape)

    # Handling parameters
    if p is not None:
        pass
    else:
        if STA:
            const = getDetrFit(STA, onlyPeriodic=onlyPeriodic)
            p0 = convconst(const)
        else:
            p0 = [None, None, None]

        p, pcov = fittimes(fitfunc, x, y, Dy, p0=p0)


    for i in range(3):
        y[i] = y[i] - fitfunc(x, *p[i])

    if zref:
        _, y, _ = gdrgps.vshift(x, y, Dy, uncert=20.0, refdate=None, Period=5)

    return y


def dPeriod(yearf, data, Ddata, startyear=None, endyear=None):
    """
    update( dict( [ [ line.split(',')[0], line.split(',')[1:] ] for line in args.eventf.read().splitlines() ] ) )

    This function returns the data for a specific period. Its default behavior is to do nothing.

    Examples:
        >>> dPeriod(yearf, data, Ddata, startyear=None, endyear=None)

    Args:
        yearf: time array with numeric time values
        data: data array 
        Ddata: same form as data but containing the uncertainties
        startyear: Initial time. Default=None
        endyear: Final time. Default=None

    Returns:
        yearf: Time array within the period defined by startyear and endyear
        data:  Data within the period defined by startyear and endyear
        Ddata: Data within the period defined by startyear and endyear

    """
    if startyear:
        index = np.where(yearf <= startyear - 0.001)
        yearf = np.delete(yearf, index)
        data = np.delete(data, index, 1)
        Ddata = np.delete(Ddata, index, 1)

    if endyear:
        index = np.where(yearf >= endyear + 0.001)
        yearf = np.delete(yearf, index)
        data = np.delete(data, index, 1)
        Ddata = np.delete(Ddata, index, 1)

    return yearf, data, Ddata


def vshift(yearf, data, Ddata, uncert=20.0, refdate=None, Period=5, offset=None):
    """
    This function shifts time series data by the average value of the interval defined by reday and the number of days specified ()

    Examples:
        >>> vshift(yearf, data, Ddata, uncert=20.0, refdate=None, Period=5, offset=None)

    Args:
        yearf: time array with numeric time values
        data: data array
        Ddata: same form as data but containing the uncertainties
        uncert: Maximum uncertainty of the data. Default=20.0
        refdate: reference date. Default=None
        Period: number of days. Default=5
        offset: initial offset. Default=None

    Returns:
        yearf: Time array
        data:  Data
        Ddata: Data uncertainty

    """

    from gtimes.timefunc import currYearfDate

    # Filtering a little, removing big outliers
    with np.errstate(invalid="ignore"):
        filt = Ddata < uncert
    filt = np.logical_and(np.logical_and(filt[0, :], filt[1, :]), filt[2, :])

    yearf = yearf[filt]
    data = np.reshape(data[np.array([filt, filt, filt])], (3, -1))
    Ddata = np.reshape(Ddata[np.array([filt, filt, filt])], (3, -1))

    if data.any():
        if not (offset is None):
            pass
        else:
            offset = estimate_offset(yearf, data, Ddata, refdate=refdate, Period=Period)

    data = np.array([data[i, :] - offset[i] for i in range(3)])

    return yearf, data, Ddata, offset


def estimate_offset(yearf, data, Ddata, refdate=None, Period=5):
    """
    Estimating offset of a time series at a reference (refdate) point for a given interval (Period)
    defaults at 5 days at the start of the time series

    """
    # averaging the first period days
    if refdate:
        startdate = currYearfDate(0, refdate)
        enddate = currYearfDate(Period, refdate)
        if Period < 0:
            tmpyearf, tmpdata, tmpDdata = dPeriod(
                yearf, data, Ddata, enddate, startdate
            )
        else:
            tmpyearf, tmpdata, tmpDdata = dPeriod(
                yearf, data, Ddata, startdate, enddate
            )

        if tmpdata.any():
            # if there are any data from this period
            offset = np.average(tmpdata[0:3, :], 1, weights=1 / tmpDdata[0:3, :])
        else:
            # We need to extrapolate
            # þarf að díla við þetta með því að módelera.
            offset = np.average(data[0:3, 0:j], 1, weights=1 / Ddata[0:3, 0:7])
    else:
        offset = np.average(data[0:3, 0:Period], 1, weights=1 / Ddata[0:3, 0:Period])

    return offset


def iprep(yearf, data, Ddata, uncert=20.0, offset=None):
    """
    This function is a wrapper for vshift intendet for initializing the time series. It converts to mm and initializes the start of the time series to zero.

    Examples:
        >>> iprep(yearf, data, Ddata, uncert=20.0, offset=None)

    Args:
        yearf: time array with numeric time values
        data: data array
        Ddata: same form as data but containing the uncertainties
        uncert: Maximum uncertainty of the data. Default=20.0
        offset: initial offset. Default=None

    Returns:
        yearf: Time array
        data:  Data
        Ddata: Data uncertainty
        
    """

    # converting to mm
    data *= 1000
    Ddata *= 1000
    return vshift(yearf, data, Ddata, uncert=uncert, offset=offset)


def filt_outl(yearf, data, Ddata, pb, errfunc, outlier):
    """
    This function removes outliers from a time series.

    Examples:
        >>> filt_outl(yearf, data, Ddata, pb, errfunc, outlier)

    Args:
        yearf: time array with numeric time values
        data: data array
        Ddata: same form as data but containing the uncertainties
        pb: parameters of the error function. Default=[None, None, None]
        errfunc: error function. Default=abs
        outlier: Maximum uncertainty of the data. 

    Returns:
        yearf: Time array
        data:  Data
        Ddata: Data uncertainty

    """
    # Removing big outliers
    for i in range(3):
        index = np.where(abs(errfunc(pb[i], yearf - yearf[0], data[i])) > outlier[i])
        yearf = np.delete(yearf, index)
        data = np.delete(data, index, 1)
        Ddata = np.delete(Ddata, index, 1)

    return yearf, data, Ddata


def gamittoNEU(sta, mm=False, ref="plate", dstring=None):
    """
    This function convert a gamit time series to a single np.array with readable time tag.

    Examples:
        >>> gamittoNEU(sta, mm=False, ref="plate", dstring=None)

    Args:
        sta: station name
        mm: convert to mm. Default=False
        ref: reference. Default="plate"
        dstring: time tag. Default=None

    Returns:
        yearf: Time array
        data:  Data
        Ddata: Data uncertainty
        
    """

    import geofunc.geofunc as gf

    yearf, data, Ddata = openGlobkTimes(sta)
    yearf, data, Ddata, _ = vshift(
        yearf, data, Ddata, uncert=1.1, refdate=None, Period=5, offset=None
    )

    # remove plata velocity
    if ref == "plate":
        plateVel = gf.plateVelo([sta])
        data[0, :] = data[0, :] - plateVel[0, 1] * (yearf - yearf[0])
        data[1, :] = data[1, :] - plateVel[0, 0] * (yearf - yearf[0])

    # convert to mm
    if mm:
        data = data * 1000
        Ddata = Ddata * 1000

    return gtoNEU(yearf, data, Ddata, dstring=dstring)


def gtoNEU(yearf, data, Ddata, dstring=None):
    """ 
    This function converts a gamit time series to a single np.array with readable time tag.

    Examples:
        >>> gtoNEU(yearf, data, Ddata)

    Args:
        yearf: time array with numeric time values
        data: data array
        Ddata: same form as data but containing the uncertainties
        dstring: time tag. Default=None

    Returns:
        yearf: Time array
        data:  Data
        Ddata: Data uncertainty

    """
    import numpy as np

    from gtimes.timefunc import convfromYearf

    if dstring == "yearf":  # use the decimal year format
        NEUdata = np.array(
            zip(yearf, data[0], data[1], data[2], Ddata[0], Ddata[1], Ddata[2]),
            dtype=[
                ("yearf", float),
                ("data[0]", float),
                ("data[1]", float),
                ("data[2]", float),
                ("Ddata[0]", float),
                ("Ddata[1]", float),
                ("Ddata[2]", float),
            ],
        )
    else:
        yearf = convfromYearf(yearf, dstring)

        NEUdata = np.array(
            zip(yearf, data[0], data[1], data[2], Ddata[0], Ddata[1], Ddata[2]),
            dtype=[
                ("yearf", "S23"),
                ("data[0]", float),
                ("data[1]", float),
                ("data[2]", float),
                ("Ddata[0]", float),
                ("Ddata[1]", float),
                ("Ddata[2]", float),
            ],
        )

    return NEUdata


def read_gps_data(
    sta,
    Dir=None,
    start=None,
    end=None,
    ref="plate",
    detrend_periodic=True,
    detrend_line=False,
    fit=False,
    detrend_period=[None, None],
    useSTA=None,
    useFIT=None,
    uncert=20.0,
    logging_level=logging.WARNING,
):
    """
    This function reads gps data from a station. It can be used to get the raw data, plate velocity and detrended data.

    Examples:


    Args:
        sta: station name
        Dir: directory. Default=None
        start: start date. Default=None
        end: end date. Default=None
        ref: reference. Default="plate"
        detrend_periodic: detrend periodic. Default=True
        detrend_line: detrend line. Default=False
        fit: fit. Default=False
        detrend_period: detrend period. Default=[None, None]
        useSTA: works in conjunction with useFit to get the fit. Default=None
        useFIT: useFIT from another station. Default=None
        uncert: Maximum uncertainty of the data. Default=20.0
        logging_level: logging level. Default=logging.WARNING
             

    Returns:
        const: detrending constants coefficient, for a lineperiodic function.
        data:  Data array for the three components including the uncertainties from the raw_data (measurement uncertainty)

    """

    import logging
    import numpy as np
    from gtimes.timefunc import TimetoYearf

    # Handling logging
    logging.basicConfig(
        format="%(asctime)-15s [%(levelname)s] %(funcName)s: %(message)s",
        level=logging_level,
    )
    logging.getLogger().setLevel(logging_level)
    module_logger = logging.getLogger()

    yearf, data, Ddata, _ = getData(sta, Dir=Dir, ref=ref)
    syearf, sdata, sDdata = yearf, data, Ddata

    # NOTE: detrending needs to be revised.
    const = getDetrFit(sta, useSTA=useSTA, useFIT=useFIT)
    p0 = convconst(const)
    pb = p0.copy()

    module_logger.info("Fitting constants:\n {}".format(p0))
    if not np.all([p0[i][1:].dtype if p0[i] is not None else False for i in range(3)]):
        module_logger.info("Setting fit to lineperiodic")
        fit = "lineperiodic"

    if useFIT == "periodic":
        module_logger.info(
            '"{}" parameters from {} used in {}'.format(
                const["Fit"].values[0], const["UseSTA"].values[0], sta
            )
        )
        module_logger.info('Setting the fit to a "line" for estimating the rate')
        fit = "line"

    syearf, sdata, sDdata = dPeriod(
        yearf,
        data,
        Ddata,
        startyear=detrend_period[0],
        endyear=detrend_period[1],
    )

    if fit:
        module_logger.info("Fitting =====================")
        if len(syearf) == 0:
            module_logger.warning(
                "No data for interval {}-{} try using the whole time series".format(
                    *detrend_period
                )
            )
            syearf, sdata, sDdata = yearf, data, Ddata

        module_logger.info("Fitting the data to a {}".format(fit))

        if fit == "line":
            pt = [p0[i][0:2] for i in range(3)]
            module_logger.info("initial parameters p0 {}".format(pt))
            pb, _ = fittimes(line, syearf, sdata, sDdata, p0=pt)
            module_logger.info("Estimated parameters for {} {}".format(sta, pb))
            pb = [np.concatenate((pb[i], p0[i][2:])) for i in range(3)]
            pt = [p0[i][0:2] for i in range(3)]

        elif fit == "periodic":
            pb, _ = fittimes(periodic, syearf, sdata, sDdata, p0=p0)

        elif fit == "lineperiodic":
            pb, _ = fittimes(lineperiodic, syearf, sdata, sDdata, p0=p0)

        const = convconst(const, pb)
        const.loc[sta, ["Starttime", "Endtime"]] = [syearf[0], syearf[-1]]

    else:
        module_logger.info("Not fitting")

    if np.all([pb[i][1:] if pb[i] is not None else False for i in range(3)]):
        if detrend_periodic:
            module_logger.info("Periodic detrending")
            module_logger.debug("Fitt parameters: {}".format(pb))
            data = detrend(yearf, data.copy(), Ddata, fitfunc=periodic, p=pb)

        if detrend_line:
            module_logger.info("linear detrending")
            pc = [pb[i][0:2] for i in range(3)]
            module_logger.debug("Fitt parameters: {}".format(pc))
            data = detrend(yearf, data.copy(), Ddata, fitfunc=line, p=pc)
    else:
        module_logger.warn("Fitt parameters are unknown pb={}".format(pb))
        if (detrend_periodic or detrend_line):
            module_logger.warning(
                "Will try to estimate the parameters based the whole dataset and detrend"
            )
            data = detrend(yearf, data.copy(), Ddata, fitfunc=lineperiodic)
    # ----------------------------------------------------

    if start:
        startf = TimetoYearf(start.year, start.month, start.day)
    else:
        startf = yearf[0]
    if end:
        endf = TimetoYearf(end.year, end.month, end.day)
    else:
        endf = yearf[-1]

    yearf, data, Ddata = dPeriod(yearf, data, Ddata, startyear=startf, endyear=endf)
    yearf, data, Ddata, _ = vshift(yearf, data, Ddata, uncert=uncert)

    data = convGlobktopandas(yearf, data, Ddata)

    data["hlength"] = np.sqrt(np.square(data[["east", "north"]]).sum(axis=1))
    data["hangle"] = np.rad2deg(np.arctan2(data["north"], data["east"]))
    data["Dhlength"] = np.sqrt(np.square(data[["Deast", "Dnorth"]]).sum(axis=1))

    module_logger.info("Dataframe columns:\n" + str(data.columns) + "\n")
    module_logger.info("Input time period: ({}, {})".format(start, end))
    module_logger.info("dataframe First and Last lines:\n" + str(data.iloc[[0, -1]]))
    module_logger.info("detrend parameter row:\n" + str(const))
    module_logger.debug("Dataframe shape: {}".format(str(data.shape)))
    module_logger.debug("dataframe types:\n" + str(data.dtypes) + "\n")

    return data, const


#
# Other functions
#


def toDateTime(yearf):
    """
    Function converting from floating point year to datetime.

    Examples:


    Args:
        yearf: floating point year array

    Returns:
        tmp: datetime equivalence of the yearf array



    """
    from gtimes.timefunc import TimefromYearf

    tmp = []

    for i in range(len(yearf)):
        tmp.append(TimefromYearf(yearf[i]))

    return tmp


def toord(yearf):
    """
    Function from floating point year to floating point ordinal.

    Examples:

    Args:
        yearf: floating point year array

    Returns:
        yearf: floating point ordinal array

    """
    from gtimes.timefunc import TimefromYearf

    for i in range(len(yearf)):
        yearf[i] = TimefromYearf(yearf[i], "ordinalf")

    return yearf


def fromord(yearf):
    """
    Function from floating point ordinal to floating point year.

    Examples:

    Args:
        yearf: floating point ordinal array

    Returns:
        yearf: floating point year array

    """


    # from floating point year to floating point ordinal

    from gtimes.timefunc import TimetoYearf

    for i in range(len(yearf)):
        yearf[i] = Timeto(yearf[i], "ordinalf")

    return yearf


def getData(
    sta,
    fstart=None,
    fend=None,
    ref="itrf2008",
    Dir=None,
    tType="TOT",
    uncert=15,
    offset=None,
):
    """
    Function extracting and filtering data to prepeare for plotting.

    Examples:
        >>>getData('GRIC', fstart='2017-01-01', fend='2017-12-31', ref='itrf2008', Dir=None, tType='TOT', uncert=15, offset=None)

    Args:
        sta: station name
        fstart: start date
        fend: end date
        ref: reference frame
        Dir: directory
        tType: type of data
        uncert: uncertainty
        offset: offset

    Returns:
        yearf: floating point year array
        data: data array
        Ddata: uncertainty array
        offset: offset

    


    """

    import geofunc.geofunc as gf

    if tType == "JOIN":
        tType = "TOT"

    yearf, data, Ddata = openGlobkTimes(sta, Dir=Dir, tType=tType)
    yearf, data, Ddata = dPeriod(yearf, data, Ddata, fstart, fend)
    if yearf is None or len(yearf) == 0:
        print("WARNING: no data for station {}".format(sta))
        return None, None, None, None
    yearf, data, Ddata, offset = iprep(yearf, data, Ddata, uncert=uncert, offset=offset)

    if offset is None:
        print("WARNING: offset determination failure for station {}".format(sta))

    if ref == "plate":
        plateVel = gf.plateVelo([sta])
        data[0, :] = data[0, :] - plateVel[0, 1] * 1000 * (yearf - yearf[0])
        data[1, :] = data[1, :] - plateVel[0, 0] * 1000 * (yearf - yearf[0])

    elif ref == "detrend":
        pN, pE, pU, pb = detrend(yearf, data, sta)
        pb_org = [pN, pE, pU]

        for i in range(3):
            data[i] = -errfunc(pb_org[i], yearf - yearf[0], data[i])

    elif ref == "itrf2008":
        pass

    else:
        plateVel = gf.plateVelo([sta], ref)
        data[0, :] = data[0, :] - plateVel[0, 1] * 1000 * (yearf - yearf[0])
        data[1, :] = data[1, :] - plateVel[0, 0] * 1000 * (yearf - yearf[0])

    return yearf, data, Ddata, offset


#
#   --- Private functions ---
#


def __converter(x):
    """
    The data extracted are converted to float and
    ocassional ******* in the data files needs to handled as NAN

    """
    import numpy as np

    try:
        return float(x)
    except:
        return np.nan

    # if x == '********':
    #    return np.nan
    # else:
    #    return float(x)
