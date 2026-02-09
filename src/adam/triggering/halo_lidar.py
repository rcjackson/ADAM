import numpy as np
import paramiko
import datetime
import os
import xarray as xr

from ..util import azimuth_point

def make_scan_file(elevations, azimuths,
                   out_file_name, azi_speed=1.,
                   el_speed=0.1,
                   wait=0, acceleration=30, repeat=7,
                   rays_per_point=2, dyn_csm=False):
    """
    Makes a CSM scanning strategy file for a Halo Photonics Doppler Lidar.
    
    Parameters
    ----------
    no_points: int
        The number of points to collect in the ray
    elevations: float 1d array or tuple
        The elevation of each sweep in the scan. If this is a 2-tuple, then
        the script will generate an RHI spanning the smallest to largest elevation
    azimuths: float or 2-tuple
        If this is a 2-tuple, then this script will generate a PPI from min_azi to max_azi.
    out_file_name: str
        The output name of the file.
    beam_width: float
        The spacing between beams.
    dyn_csm: bool
        Set to True to send CSM assuming Dynamic CSM mode
    
    Returns
    -------
    None
        This function does not return anything. It generates a CSM scan strategy file for the Halo Lidar 
        and saves it to the specified output file name.
    """    
    speed_azi_encoded = int(azi_speed * (AZ_COUNTS_PER_ROT / 360.))
    speed_el_encoded = int(el_speed * (EL_COUNTS_PER_ROT / 360.))
    clockwise = True
    no_points = len(azimuths) * len(elevations)
    with open(out_file_name, 'w') as output:
        if dyn_csm is False:
            output.write('%d\r\n' % repeat)
            output.write('%d\r\n' % no_points)
            output.write('%d\r\n' % rays_per_point)
  
        for el in elevations:
            if clockwise:
                az_array = azimuths
            else:
                az_array = azimuths.reverse()
            for az in az_array:
                azi_encoded = -int(az * (AZ_COUNTS_PER_ROT / 360.))
                el_encoded = -int(el * (EL_COUNTS_PER_ROT / 360.))
                output.write("A.1=%d,S.1=%d,P.1=%d*A.2=%d,S.2=%d,P.2=%d\r\n" %
                             (acceleration, speed_azi_encoded, azi_encoded,
                              acceleration, speed_el_encoded, el_encoded))
                output.write('W%d\r\n' % (wait))
            clockwise = ~clockwise
    return


def send_scan(file_name, lidar_ip_addr, lidar_uname, lidar_pwd, out_file_name='user.txt', dyn_csm=False,
              client=None):
    """
    Sends a scan to the lidar

    Parameters
    ---------
    file_name: str
        Path to the CSM-format scan strategy
    lidar_ip_addr:
        IP address of the lidar
    lidar_uname:
        The username of the lidar
    lidar_password:
        The lidar's password
    out_file_name:
        The output file name on the lidar
    dyn_csm: bool
        Set to True to assume Dynamic CSM mode
    client: paramiko.SSHClient, optional
        An optional SSH client to use for the connection. If not provided, a new client will be created
        and closed within this function.

    """
    if client is not None:
        ssh = client
        close_client = False
    else:
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh.connect(lidar_ip_addr, username=lidar_uname, password=lidar_pwd)
        print("Connected to the Lidar!")
        close_client = True

    with ssh.open_sftp() as sftp:
        if dyn_csm is False:
            print(f"Writing {out_file_name} on lidar.")
            sftp.put(file_name, "/C:/Lidar/System/Scan parameters/%s" % out_file_name)
        else:
            sftp.put(file_name, f"/C:/Users/End User/DynScan/{out_file_name}")
    if close_client:
        ssh.close()


def get_file(time, lidar_ip_addr, lidar_uname, lidar_pwd, client=None):
    """
    Gets all files from the lidar within the previous and current hour. If no files are found, prints a message and returns.

    Parameters
    ----------
    time: datetime
        The time for which to retrieve the file. This function will look for files from the previous hour and the current hour.
    lidar_ip_addr:
        IP address of the lidar.
    lidar_uname:
        The username of the lidar.
    lidar_password:
        The lidar's password.
    client: paramiko.SSHClient, optional
        An optional SSH client to use for the connection. If not provided, a new client will be created and closed within this function.
    
    Returns
    -------
    None
        This function does not return anything. It retrieves files from the lidar and saves them to the current directory.
    
    """
    if client is not None:
        ssh = client
        close_client = False
    else:
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh.connect(lidar_ip_addr, username=lidar_uname, password=lidar_pwd)
        print("Connected to the Lidar!")
        close_client = True
    
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    print("Connecting to %s" % lidar_ip_addr)
    ssh.connect(lidar_ip_addr, username=lidar_uname, password=lidar_pwd)
    print("Connected to the Lidar!")
    year = time.year
    day = time.day
    month = time.month
    hour = time.hour
    prev_hour = time - datetime.timedelta(hours=1)
    file_path = "/C:/Lidar/Data/Proc/%d/%d%02d/%d%02d%02d/" % (year, year, month, year, month, day)
    print(file_path)
    with ssh.open_sftp() as sftp:
        file_list = sftp.listdir(file_path)
        time_string = '%d%02d%02d_%02d' % (year, month, day, hour)
        time_string_prev = '%d%02d%02d_%02d' % (prev_hour.year, prev_hour.month, prev_hour.day, prev_hour.hour)
        file_name = None
        
        for f in file_list:
            if time_string in f or time_string_prev in f: 
                file_name = f
                base, name = os.path.split(file_name)
                print(print(file_name))
                sftp.get(os.path.join(file_path, file_name), name)
        if file_name is None:
            print("%s not found!" % str(time))
            if close_client:                 
                ssh.close()

            return
    if close_client:
        ssh.close()

def trigger_lidar_ppis_from_mask(rad_scan, lidar_lat, lidar_lon, lidar_ip_addr, lidar_uname, lidar_pwd, elevations, 
                                 az_width=30., az_res=2., out_file_name='user.txt', dyn_csm=False):
    """
    Triggers a PPI scan on the lidar using a scan strategy generated from a lake breeze mask.

    Parameters
    ----------
    rad_scan: RadarImage
        The radar scan containing the lake breeze mask. The azimuth of the largest lake breeze region will be
        used to determine the center of the RHI scan.
    lidar_lat: float
        The latitude of the lidar
    lidar_lon: float
        The longitude of the lidar
    lidar_ip_addr:
        IP address of the lidar
    lidar_uname:
        The username of the lidar
    lidar_password:
        The lidar's password
    out_file_name:
        The output file name on the lidar
    dyn_csm: bool
        Set to True to assume Dynamic CSM mode
    az_width: float
        The width of the azimuth scan in degrees. The scan will be centered around the azimuth of the
        largest lake breeze region as determined by the model's radar image and the location of the lidar.
    az_res: float
        The resolution of the azimuth scan in degrees. This determines how many points will be in the scan.
        For example, if az_width is 30 and az_res is 2, then
        there will be 15 points in the azimuth scan (from -15 to +15 degrees around the center azimuth).
    """
    middle_azimuth = azimuth_point(lidar_lat, lidar_lon, rad_scan)
    azimuths = np.arange(middle_azimuth - az_width/2, middle_azimuth + az_width/2, az_res)

    make_scan_file(elevations, azimuths, out_file_name, dyn_csm=dyn_csm)
    send_scan(out_file_name, lidar_ip_addr, lidar_uname, lidar_pwd, out_file_name=out_file_name, dyn_csm=dyn_csm)


def trigger_lidar_RHI_from_mask(rad_scan, lidar_lat, lidar_lon, lidar_ip_addr, lidar_uname, lidar_pwd, elevations, 
                                out_file_name='user.txt', dyn_csm=False):
    """
    Triggers a PPI scan on the lidar using a scan strategy generated from a lake breeze mask.

    Parameters
    ----------
    rad_scan: RadarImage
        The radar scan containing the lake breeze mask. The azimuth of the largest lake breeze region will be
        used to determine the center of the RHI scan.
    lidar_lat: float
        The latitude of the lidar
    lidar_lon: float
        The longitude of the lidar
    lidar_ip_addr:
        IP address of the lidar
    lidar_uname:
        The username of the lidar
    lidar_password:
        The lidar's password
    out_file_name:
        The output file name on the lidar
    dyn_csm: bool
        Set to True to assume Dynamic CSM mode
    az_width: float
        The width of the azimuth scan in degrees. The scan will be centered around the azimuth of the
        largest lake breeze region as determined by the model's radar image and the location of the lidar.
    az_res: float
        The resolution of the azimuth scan in degrees. This determines how many points will be in the scan.
        For example, if az_width is 30 and az_res is 2, then
        there will be 15 points in the azimuth scan (from -15 to +15 degrees around the center azimuth).
    """
    middle_azimuth = azimuth_point(lidar_lat, lidar_lon, rad_scan)
    azimuths = middle_azimuth

    make_scan_file(elevations, azimuths, out_file_name, dyn_csm=dyn_csm)
    send_scan(out_file_name, lidar_ip_addr, lidar_uname, lidar_pwd, out_file_name=out_file_name, dyn_csm=dyn_csm)