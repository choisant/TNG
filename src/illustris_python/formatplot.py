import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import pandas as pd
import numpy as np
from matplotlib.ticker import ScalarFormatter, MultipleLocator, FormatStrFormatter, AutoMinorLocator
TEXTSIZE = 20

def log_formater(df):
    df_log = df.copy(deep=True)
    for key in df.keys():
        if key == "id" or key == "cataid":
            df_log[key] = df[key]
        elif "SubhaloStellarPhotometrics" in key:
            df_log[key] = df[key]
        elif "SubhaloColor" in key:
            df_log[key] = df[key]
        else:
            df_log[key] = np.log10(list(df[key]))
    return df_log

def VD_SM(ax, x0=1.5, x1=3, y0=9, y1=12):
    ax.set(xlim=(x0, x1), ylim=(y0, y1))
    ax.set_xlabel(r"$\log(\sigma)$ [km/s])", fontsize=TEXTSIZE)
    ax.set_ylabel(r"$\log(M_{*})$ [$ \mathrm{M}_\odot $]", fontsize=TEXTSIZE)
    ax.tick_params(which="both", direction="in", top=True, right=True, labelsize=TEXTSIZE, pad=15, length=4, width=2)
    ax.minorticks_on()
    ax.legend(loc=2, fontsize=TEXTSIZE, frameon=False)

def VD_fVD(ax, x0=1.5, x1=3, y0=0.5, y1=2):
    ax.set(xlim=(x0, x1), ylim=(y0, y1))
    ax.set_xlabel(r"$\log(\sigma_{SF})$ [km/s])", fontsize=TEXTSIZE)
    ax.set_ylabel(r"$\sigma/\sigma_{SF}$", fontsize=TEXTSIZE)
    ax.tick_params(which="both", direction="in", top=True, right=True, labelsize=TEXTSIZE, pad=15, length=4, width=2)
    ax.minorticks_on()
    ax.legend(loc=2, fontsize=TEXTSIZE, frameon=False)

def VSigma_SM(ax, x0=0, x1=2.5, y0=10**9, y1=10**12):
    ax.set(xlim=(x0, x1), ylim=(y0, y1))
    ax.set_xlabel(r"$V_{max}/\sigma$", fontsize=TEXTSIZE)
    ax.set_ylabel(r"$M_*$ [$ \mathrm{M}_\odot $]", fontsize=TEXTSIZE)
    ax.tick_params(which="both", direction="in", top=True, right=True, labelsize=TEXTSIZE, pad=15, length=4, width=2)
    ax.minorticks_on()
    ax.legend(fontsize=TEXTSIZE, frameon=False)

def Vmax_SM(ax, x0=1.5, x1=2.5, y0=9, y1=11.5):
    ax.set(xlim=(x0, x1), ylim=(y0, y1))
    ax.set_xlabel(r"$\log(V_{max})$ [km/s]", fontsize=TEXTSIZE)
    ax.set_ylabel(r"$\log(M_*)$ [$ \mathrm{M}_\odot $]", fontsize=TEXTSIZE)
    ax.tick_params(which="both", direction="in", top=True, right=True, labelsize=TEXTSIZE, pad=15, length=4, width=2)
    ax.minorticks_on()
    ax.legend(loc=4, fontsize=TEXTSIZE, frameon=False)

def V_fV(ax, x0=2, x1=2.6, y0=0.9, y1=1.4):
    ax.set(xlim=(x0, x1), ylim=(y0, y1))
    ax.set_xlabel(r"$\log(V_{max, SF})$ [km/s])", fontsize=TEXTSIZE)
    ax.set_ylabel(r"$V_{rot, 2.2}/V_{max, SF}$", fontsize=TEXTSIZE)
    ax.tick_params(which="both", direction="in", top=True, right=True, labelsize=TEXTSIZE, pad=15, length=4, width=2)
    ax.minorticks_on()
    ax.legend(loc=2, fontsize=TEXTSIZE, frameon=False)

def GF_sSFR(ax, x0=-5, x1=0.1, y0=-5, y1=1):
    ax.set(xlim=(x0, x1), ylim=(y0, y1))
    ax.set_xlabel(r"$\log(sSFR) [Gyr^{-1}]$", fontsize=TEXTSIZE)
    ax.set_ylabel(r"$\log(f_{gas})$", fontsize=TEXTSIZE)
    ax.tick_params(which="both", direction="in", top=True, right=True, labelsize=TEXTSIZE, pad=15, length=4, width=2)
    ax.minorticks_on()
    ax.legend(loc=4, fontsize=TEXTSIZE, frameon=True)

def C_SM(color, ax, x0=9, x1=12, y0=-1, y1=1):
    ax.set(xlim=(x0, x1), ylim=(y0, y1))
    ax.set_ylabel(color + " [mag]", fontsize=TEXTSIZE+5)
    ax.set_xlabel(r"$\log(M_*)$ [$ \mathrm{M}_\odot $]", fontsize=TEXTSIZE+5)
    ax.tick_params(which="major", direction="in", top=True, right=True, labelsize=TEXTSIZE+5, pad=20, length=8, width=3)
    ax.tick_params(which="minor", direction="in", top=True, right=True, labelsize=TEXTSIZE+5, pad=20, length=5, width=3)
    ax.minorticks_on()
    ax.legend(loc=0, fontsize=TEXTSIZE+5, frameon=False)
    
def PDF_C(color, ax, legend_on, x0=-1, x1=2, y0=0, y1=4):
    ax.set(xlim=(x0, x1), ylim=(y0, y1))
    ax.set_ylabel("PDF", fontsize=TEXTSIZE)
    ax.set_xlabel(color + " color [mag]", fontsize=TEXTSIZE)
    ax.tick_params(which="both", direction="in", top=True, right=True, labelsize=TEXTSIZE, pad=15, length=4, width=2)
    ax.minorticks_on()
    if legend_on:
        ax.legend(fontsize=TEXTSIZE, frameon=False)

def HM_SM(ax, text="", x0=11, x1=14, y0=(9.0), y1=(12)):
    ax.set(xlim=(x0, x1), ylim=(y0, y1))
    ax.set_xlabel(r"$\log(M_{halo})$ [$ \mathrm{M}_\odot $]", fontsize=TEXTSIZE)
    ax.set_ylabel(r"$\log(M_{*})$ [$ \mathrm{M}_\odot $]", fontsize=TEXTSIZE)
    ax.tick_params(which="both", direction="in", top=True, right=True, labelsize=TEXTSIZE, pad=15, length=4, width=2)
    ax.minorticks_on()
    ax.text(0.05, 0.92, text, fontsize=TEXTSIZE, fontweight="bold", transform=ax.transAxes)
    ax.legend(loc=2, fontsize=TEXTSIZE, edgecolor=None)

def SM_SM(ax, text="", x0=9.5, x1=12, y0=(9.5), y1=(12)):
    ax.set(xlim=(x0, x1), ylim=(y0, y1))
    ax.set_xlabel(r"$\log(M_{*, SF})$ [$ \mathrm{M}_\odot $]", fontsize=TEXTSIZE)
    ax.set_ylabel(r"$\log(M_{*})$ [$ \mathrm{M}_\odot $]", fontsize=TEXTSIZE)
    ax.tick_params(which="both", direction="in", top=True, right=True, labelsize=TEXTSIZE, pad=15, length=4, width=2)
    ax.minorticks_on()
    ax.text(0.05, 0.92, text, fontsize=TEXTSIZE, fontweight="bold", transform=ax.transAxes)
    ax.legend(loc=2, fontsize=TEXTSIZE, edgecolor=None)

def SM_fSM(ax, text="", x0=9.5, x1=12, y0=(1), y1=(1.5)):
    ax.set(xlim=(x0, x1), ylim=(y0, y1))
    ax.set_xlabel(r"$\log(M_{*, SF})$ [$ \mathrm{M}_\odot $]", fontsize=TEXTSIZE)
    ax.set_ylabel(r"$M_{*}/M_{*, SF}$", fontsize=TEXTSIZE)
    ax.tick_params(which="both", direction="in", top=True, right=True, labelsize=TEXTSIZE, pad=15, length=4, width=2)
    ax.minorticks_on()
    ax.text(0.05, 0.92, text, fontsize=TEXTSIZE, fontweight="bold", transform=ax.transAxes)
    ax.legend(loc=2, fontsize=TEXTSIZE, edgecolor=None)

def HM_fHM(ax, text="", x0=11, x1=14, y0=(0), y1=(1)):
    ax.set(xlim=(x0, x1), ylim=(y0, y1))
    ax.set_xlabel(r"$\log(M_{halo, SF})$ [$ \mathrm{M}_\odot $]", fontsize=TEXTSIZE)
    ax.set_ylabel(r"$M_{200}/M_{halo, SF}$", fontsize=TEXTSIZE)
    ax.tick_params(which="both", direction="in", top=True, right=True, labelsize=TEXTSIZE, pad=15, length=4, width=2)
    ax.minorticks_on()
    ax.text(0.05, 0.92, text, fontsize=TEXTSIZE, fontweight="bold", transform=ax.transAxes)
    ax.legend(loc=2, fontsize=TEXTSIZE, edgecolor=None)

def GM_SM(ax, text="", x0=5.5, x1=10, y0=9.5, y1=12):
    ax.set(xlim=(x0, x1), ylim=(y0, y1))
    ax.set_xlabel(r"$\log(M_{gas})$ [$ \mathrm{M}_\odot $]", fontsize=TEXTSIZE)
    ax.set_ylabel(r"$\log(M_{*})$ [$ \mathrm{M}_\odot $]", fontsize=TEXTSIZE)
    ax.tick_params(which="both", direction="in", top=True, right=True, labelsize=TEXTSIZE, pad=15, length=4, width=2)
    ax.minorticks_on()
    ax.text(0.05, 0.92, text, fontsize=TEXTSIZE, fontweight="bold", transform=ax.transAxes)
    ax.legend(loc=2, fontsize=TEXTSIZE, edgecolor=None)


def R_SM(ax, x0=(-1), x1=2, y0=9, y1=12):
    ax.set(xlim=(x0, x1), ylim=(y0, y1))
    ax.set_xlabel(r"$\log(r_e)$ [kpc]", fontsize=TEXTSIZE)
    ax.set_ylabel(r"$\log(M_{*})$ [$ \mathrm{M}_\odot $]", fontsize=TEXTSIZE)
    ax.tick_params(which="both", direction="in", top=True, right=True, labelsize=TEXTSIZE, pad=15, length=4, width=2)
    ax.minorticks_on()
    ax.legend(loc=0, fontsize=TEXTSIZE, frameon=False)

def R_fR(ax, x0=(0), x1=1.5, y0=(0.8), y1=2):
    ax.set(xlim=(x0, x1), ylim=(y0, y1))
    ax.set_xlabel(r"$\log(R_{e, SF})$ [kpc]", fontsize=TEXTSIZE)
    ax.set_ylabel(r"$R_e/R_{e, SF}$ ", fontsize=TEXTSIZE)
    ax.tick_params(which="both", direction="in", top=True, right=True, labelsize=TEXTSIZE, pad=15, length=4, width=2)
    ax.minorticks_on()
    ax.legend(loc=0, fontsize=TEXTSIZE, frameon=False)

def SM_R(ax, x0=(9), x1=13, y0=(-1), y1=2):
    ax.set(xlim=(x0, x1), ylim=(y0, y1))
    ax.set_ylabel(r"$\log(r_e)$ [kpc]", fontsize=TEXTSIZE)
    ax.set_xlabel(r"$\log(M_{*})$ [$ \mathrm{M}_\odot $]", fontsize=TEXTSIZE)
    ax.tick_params(which="both", direction="in", top=True, right=True, labelsize=TEXTSIZE, pad=15, length=4, width=2)
    ax.minorticks_on()
    ax.legend(fontsize=TEXTSIZE, frameon=False)

def R_VD(ax, x0=(-1), x1=2, y0=1.5, y1=3):
    ax.set(xlim=(x0, x1), ylim=(y0, y1))
    ax.set_xlabel(r"$\log(r_e)$ [kpc/h]", fontsize=TEXTSIZE)
    ax.set_ylabel(r"$\log(\sigma)$ [km/s]", fontsize=TEXTSIZE)
    ax.tick_params(which="both", direction="in", top=True, right=True, labelsize=TEXTSIZE, pad=15, length=4, width=2)
    ax.minorticks_on()
    ax.legend(loc=0, fontsize=TEXTSIZE, frameon=False)

def VD_BH(ax, x0=1, x1=3, y0=(6), y1=(10)):
    ax.set(xlim=(x0, x1), ylim=(y0, y1))
    ax.set_ylabel(r"$\log(M_{BH})$ [$ \mathrm{M}_\odot $]", fontsize=TEXTSIZE)
    ax.set_xlabel(r"$\log(\sigma)$ [km/s]", fontsize=TEXTSIZE)
    ax.tick_params(which="both", direction="in", top=True, right=True, labelsize=TEXTSIZE, pad=15, length=4, width=2)
    ax.minorticks_on()
    ax.legend(fontsize=TEXTSIZE, frameon=False)

def SM_BH(ax, x0=9, x1=(13), y0=(6), y1=(10)):
    ax.set(xlim=(x0, x1), ylim=(y0, y1))
    ax.set_ylabel(r"$\log(M_{BH})$ [$ \mathrm{M}_\odot $]", fontsize=TEXTSIZE)
    ax.set_xlabel(r"$\log(M_{*})$ [$ \mathrm{M}_\odot $]", fontsize=TEXTSIZE)
    ax.tick_params(which="both", direction="in", top=True, right=True, labelsize=TEXTSIZE, pad=15, length=4, width=2)
    ax.minorticks_on()
    ax.legend(fontsize=TEXTSIZE, frameon=False)

def DM_BH(ax, x0=10, x1=(14), y0=(6), y1=(10)):
    ax.set(xlim=(x0, x1), ylim=(y0, y1))
    ax.set_ylabel(r"$\log(M_{BH})$ [$ \mathrm{M}_\odot $]", fontsize=TEXTSIZE)
    ax.set_xlabel(r"$\log(M_{DM})$ [$ \mathrm{M}_\odot $]", fontsize=TEXTSIZE)
    ax.tick_params(which="both", direction="in", top=True, right=True, labelsize=TEXTSIZE, pad=15, length=4, width=2)
    ax.minorticks_on()
    ax.legend(fontsize=TEXTSIZE, frameon=False)

def R_BH(ax, x0=0, x1=2, y0=(6), y1=(10)):
    ax.set(xlim=(x0, x1), ylim=(y0, y1))
    ax.set_ylabel(r"$\log(M_{BH})$ [$ \mathrm{M}_\odot $]", fontsize=TEXTSIZE)
    ax.set_xlabel(r"$\log(r_e)$ [ckpc/h]", fontsize=TEXTSIZE)
    ax.tick_params(which="both", direction="in", top=True, right=True, labelsize=TEXTSIZE, pad=15, length=4, width=2)
    ax.minorticks_on()
    ax.legend(fontsize=TEXTSIZE, frameon=False)

def rot_galaxy_map(ax, r_e, label_x, label_y):
    ax.set(xlim=(-r_e*4, r_e*4), ylim=(-r_e*4, r_e*4))
    ax.set_ylabel(label_x + " [kpc]", fontsize=TEXTSIZE)
    ax.set_xlabel(label_y + " [kpc]", fontsize=TEXTSIZE)
    ax.tick_params(which="both", direction="in", top=True, right=True, labelsize=TEXTSIZE, pad=15, length=4, width=2)
    ax.minorticks_on()
    ax.legend(fontsize=TEXTSIZE, frameon=False)

def FP_3D(df):
    #make the figure
    fig = plt.figure(figsize = (9,6))
    ax = fig.gca(projection="3d")

    #plot the data
    x, y, z = [], [], []
    z = np.log10(list(df["SubhaloMassInHalfRadStellar"]))
    y = np.log10(list(df["SubhaloHalfmassRadStellar"]))
    x = np.log10(list(df["SubhaloVelDisp"]))
    s = list(df["SubhaloMass"])
    s = [(i/(10**(10)))**(1/2) for i in s]

    ax.scatter(xs = x, ys = y, zs = z, alpha=0.8, c=y, cmap=plt.get_cmap("magma"), s=s)

    #plane
    """
    FPz = np.arange(0,12, 0.25)
    FPy = np.arange(0,12, 0.25)
    FPz, FPy = np.meshgrid(FPz, FPy)
    FPx = 0.8*FPz-0.8*FPy -2
    # Plot the surface.
    ax.plot_surface(FPx, FPy, FPz, linewidth=0, antialiased=False, alpha = 0.2)
    """
    #Format
    ax.set_title("Fundamental Plane", fontsize=14)
    ax.set_zlabel("Mass")
    ax.set_ylabel("Radius")
    ax.set_xlabel("Velocity")
    ax.set_zlim(8, 13)
    ax.set_ylim(1, 4)
    ax.set_xlim(1, 3)
    return ax