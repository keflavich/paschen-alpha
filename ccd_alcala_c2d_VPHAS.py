# Produce a color-color diagram with photometric data for YSOs (Alcala and c2d) and background sources (VPHAS and c2d)

import pandas as pd
import numpy as np
from astropy import units as u
import matplotlib.pyplot as plt
from matplotlib import rc
from adaptive_param_plot import *

plt.rcParams['text.latex.preamble'] = [r'\usepackage{gensymb}']

def import_csv(filename, columns, sourceName, drop_NaN=True):
    '''Import contents of a .csv file into a pandas dataframe, dropping NaNs
    when specified and grouping by specified unique identifier.'''
    df = pd.read_csv(filename)
    if drop_NaN==True:
        df = df.dropna(subset=columns)
    df = df.groupby(sourceName).mean()
    return df

def convert_flux_to_mag(flux, filter):
    '''Convert H-alpha fluxes to average flux densities in mJy.'''
    if filter=='FHa':
        FHa_flux = u.Quantity(flux, (10**(-3))*u.W/u.meter**2) # Give flux units that match catalog units
        frequency_Ha = (6568.0 * u.AA).to(u.Hz, equivalencies=u.spectral()) # Used INT WFC H-alpha filter center wavelength from http://svo2.cab.inta-csic.es/theory/fps/index.php?id=INT/IPHAS.Ha&&mode=browse&gname=INT&gname2=IPHAS#filter
        FHa_Jy = (FHa_flux/frequency_Ha).to(u.Jy) # Divide H-alpha flux by frequency of H-alpha in Hz
        Ha_ZP_Jy = 2659.39*u.Jy # VST H-alpha filter from http://svo2.cab.inta-csic.es/theory/fps/index.php?id=Paranal/OmegaCAM.Halpha&&mode=search&search_instrument=OmegaCAM#filter
        mag = -2.5*np.log10(FHa_Jy/Ha_ZP_Jy)
    return mag

def convert_flux_density_to_mag(flux_density, filter):
    '''Convert flux densities to magnitudes using correct zero points. 
    From http://svo2.cab.inta-csic.es/theory/fps/index.php?mode=browse&gname=Spitzer'''
    if filter=='FIR1':
        FIR_ZP_Jy = 277.2
    if filter=='FIR2':
        FIR_ZP_Jy = 179.0
    if filter=='FIR3':
        FIR_ZP_Jy = 113.8
    if filter=='FIR4':
        FIR_ZP_Jy = 62.0
    mag = -2.5*np.log10(flux_density*(10**(-3))/FIR_ZP_Jy)
    return mag

def get_data(df, df_type):
    '''Get data from a given dataframe.'''
    if df_type=='yso':
        df_3p6, df_4p5, df_5p8, df_8p0, df_Halpha = df['FIR1_mag'].values, df['FIR2_mag'].values, df['FIR3_mag'].values, df['FIR4_mag'].values, df['Hamag'].values
    if df_type=='background':
        df_3p6, df_4p5, df_5p8, df_8p0, df_Halpha = df['FIR1_mag'].values, df['FIR2_mag'].values, df['FIR3_mag'].values, df['FIR4_mag'].values, df['Hamag'].values
    return df_3p6, df_4p5, df_5p8, df_8p0, df_Halpha


def plot_ccd(yso_IR_sw, yso_IR_lw, yso_Halpha, bg_IR_sw, bg_IR_lw, bg_Halpha, sw_str, lw_str):
    '''Plot a color-color diagram, given a dataframe.'''
    plt.figure(dpi = 100)
    plt.grid()
    plt.plot(yso_Halpha-yso_IR_lw,yso_IR_sw-yso_IR_lw,marker='.',linestyle='',color='xkcd:azure',label="Young stellar objects",alpha=1.0)
    plt.plot(bg_Halpha-bg_IR_lw,bg_IR_sw-bg_IR_lw,marker='.',linestyle='',color='xkcd:orange',label="Background sources",alpha=1.0)
    plt.xlabel(r"H$\mathrm{\alpha}$ - "+lw_str)
    plt.ylabel(sw_str+" - "+lw_str)
    plt.title("Color-color diagram for YSOs/background sources")
    plt.legend()
    plt.show()

def plot_contoured_ccd(yso_IR_sw, yso_IR_lw, yso_Halpha, bg_IR_sw, bg_IR_lw, bg_Halpha, sw_str, lw_str, bins):
    '''Plot a color-color diagram with contours in dense areas.'''
    plt.figure(dpi = 100)
    plt.grid()
    adaptive_param_plot(yso_Halpha-yso_IR_lw,yso_IR_sw-yso_IR_lw,marker_color='xkcd:azure',bins=bins,fill=False,alpha=1,threshold=10,cmap=None,colors='xkcd:azure',label="Young stellar objects")
    adaptive_param_plot(bg_Halpha-bg_IR_lw,bg_IR_sw-bg_IR_lw,marker_color='xkcd:orange',bins=bins,fill=False,alpha=1,threshold=10,cmap=None,colors='xkcd:orange',label="Background sources")
    plt.xlabel(r"H$\mathrm{\alpha}$ - "+lw_str)
    plt.ylabel(sw_str+" - "+lw_str)
    plt.title("Color-color diagram for YSOs/background sources")
    plt.legend()
    plt.show()

df_yso = import_csv('alcala_c2d_xmatch.csv',columns=['FIR1','FIR2','FIR3','FIR4','FHa'],sourceName='Object')
df_background = import_csv('c2d_VPHAS_xmatch.csv',columns=['FIR1','FIR2','FIR3','FIR4','Hamag'],sourceName='sourceID')

df_yso['Hamag'] = convert_flux_to_mag(df_yso['FHa'], 'FHa')
df_yso['FIR1_mag'] = convert_flux_density_to_mag(df_yso['FIR1'], 'FIR1')
df_yso['FIR2_mag'] = convert_flux_density_to_mag(df_yso['FIR2'], 'FIR2')
df_yso['FIR3_mag'] = convert_flux_density_to_mag(df_yso['FIR3'], 'FIR3')
df_yso['FIR4_mag'] = convert_flux_density_to_mag(df_yso['FIR4'], 'FIR4')
df_background['FIR1_mag'] = convert_flux_density_to_mag(df_background['FIR1'], 'FIR1')
df_background['FIR2_mag'] = convert_flux_density_to_mag(df_background['FIR2'], 'FIR2')
df_background['FIR3_mag'] = convert_flux_density_to_mag(df_background['FIR3'], 'FIR3')
df_background['FIR4_mag'] = convert_flux_density_to_mag(df_background['FIR4'], 'FIR4')

yso_3p6, yso_4p5, yso_5p8, yso_8p0, yso_Halpha = get_data(df_yso, 'yso')
bg_3p6, bg_4p5, bg_5p8, bg_8p0, bg_Halpha = get_data(df_background, 'background')

# plot_ccd(yso_3p6, yso_4p5, yso_Halpha, bg_3p6, bg_4p5, bg_Halpha, '[3.6]', '[4.5]')

plot_contoured_ccd(yso_5p8, yso_8p0, yso_Halpha, bg_5p8, bg_8p0, bg_Halpha, '[5.8]', '[8.0]', 20)