import numpy as np 
import scipy as sp 
import matplotlib.pyplot as plt 
import pandas as pd 
import matplotlib.gridspec as gridspec
import seaborn as sns 
from scipy import stats

####figure settings####
plt.rcParams["axes.titlesize"]=10
plt.rcParams["axes.labelsize"]=8
plt.rcParams["axes.linewidth"]=.5
plt.rcParams["lines.linewidth"]=2
plt.rcParams["lines.markersize"]=2
plt.rcParams["xtick.labelsize"]=6
plt.rcParams["ytick.labelsize"]=6
plt.rcParams["font.family"] = "arial"
plt.rcParams['mathtext.fontset'] = 'dejavusans'
plt.rcParams["legend.fontsize"] = 6
plt.rcParams['xtick.minor.width'] = 0.5
plt.rcParams['xtick.major.width'] = 0.5
plt.rcParams['ytick.minor.width'] = 0.5
plt.rcParams['ytick.major.width'] = 0.5

def cm2inch(value):
    return value/2.54
#######################
data = pd.read_csv("calcium_data_wo-metal-disc.csv")
data =data.dropna()

    # generate frame
fig = plt.figure(figsize=(cm2inch(17.6), cm2inch(25)))
gs1 = gridspec.GridSpec(5, 3)
gs1.update(top=0.95,bottom=0.05,left=0.08,right=0.98,hspace=0.3,wspace=0.3)
ax1 = plt.subplot(gs1[0,0])
ax2 = plt.subplot(gs1[0,1])
ax3 = plt.subplot(gs1[0,2])
ax4 = plt.subplot(gs1[1,0])
ax5 = plt.subplot(gs1[1,1])
ax6 = plt.subplot(gs1[1,2])
ax7 = plt.subplot(gs1[2,0])
ax8 = plt.subplot(gs1[2,1])
ax9 = plt.subplot(gs1[2,2])
ax10 = plt.subplot(gs1[3,0])
ax11 = plt.subplot(gs1[3,1])
ax12 = plt.subplot(gs1[3,2])
ax13 = plt.subplot(gs1[4,0])
ax14 = plt.subplot(gs1[4,1])
ax15 = plt.subplot(gs1[4,2])

axs = [ax1,ax2,ax3,ax4,ax5,ax6,ax7,ax8,ax9,ax10,ax11,ax12,ax13,ax14,ax15]

step = 0
for group in np.unique(data["group"]):
    data_1 = data[data["group"]==group]

    inx = 0
    for culture in np.unique(data_1["culture_ID"]):
        indx = step+inx
        culture_data = data_1[data_1["culture_ID"]==culture]

        if group=="sham":
            sns.kdeplot(data=culture_data,x="firing_rate",hue="timing", hue_order=["pre","1st"],palette=["#293241ff","#98c1d9ff"],fill=False,common_norm=False,alpha=.5,cumulative=True,ax=axs[indx],legend=False)
            axs[indx].set_title("batch "+str(np.unique(culture_data["prep_date"])[0])+", culture "+str(culture))
            axs[indx].text(-0.01,0.5,"N="+str(len(culture_data[culture_data["timing"]=="pre"])),color="#293241ff",fontsize=6.,ha='left')
            axs[indx].text(-0.01,0.6,"N="+str(len(culture_data[culture_data["timing"]=="1st"])),color="#98c1d9ff",fontsize=6.,ha='left')

        if np.unique(culture_data["group"])[0]=="stim":
            sns.kdeplot(data=culture_data,x="firing_rate",hue="timing", hue_order=["pre","1st"],palette=["#293241ff","#98c1d9ff"],fill=False,common_norm=False,alpha=.5,cumulative=True,ax=axs[indx],legend=False)
            axs[indx].set_title("batch "+str(np.unique(culture_data["prep_date"])[0])+", culture "+str(culture))
            axs[indx].text(-0.01,0.5,"N="+str(len(culture_data[culture_data["timing"]=="pre"])),color="#293241ff",fontsize=6.,ha='left')
            axs[indx].text(-0.01,0.6,"N="+str(len(culture_data[culture_data["timing"]=="1st"])),color="#98c1d9ff",fontsize=6.,ha='left')

        inx = inx + 1
    step = step+7


    for ax in axs:
        if ax!=ax13:
            ax.set_xlabel("")
            ax.set_ylabel("")
        ax13.set_xlabel(r"$\mathrm{\bf{[Ca^{2+}]_i\ spike\ rate}}$ | Hz")
        ax13.set_ylabel(r"$\mathrm{\bf{cdf}}$")

plt.savefig("S-calcium.svg")
plt.show()