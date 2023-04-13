import numpy as np 
import scipy as sp 
import matplotlib.pyplot as plt 
import pandas as pd 
import matplotlib.gridspec as gridspec
from scipy import stats
from matplotlib import rc 

####figure settings####
plt.rcParams["axes.titlesize"]=10
plt.rcParams["axes.labelsize"]=8
plt.rcParams["axes.linewidth"]=.5
plt.rcParams["lines.linewidth"]=1.
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

def get_value(subdata):
    pre_data = subdata[subdata["sequence"]=="pre"]
    post_data = subdata[subdata["sequence"]=="post"]

    pre_intensity = pre_data["normed"]
    post_intensity = post_data["normed"]

    pre_intensity  = [i for i in pre_intensity]
    post_intensity = [i for i in post_intensity]

    return pre_intensity,post_intensity

def get_value_raw(subdata):
    pre_data = subdata[subdata["sequence"]=="pre"]
    post_data = subdata[subdata["sequence"]=="post"]

    pre_intensity = pre_data["RawIntDen"]
    post_intensity = post_data["RawIntDen"]

    pre_intensity  = [i for i in pre_intensity]
    post_intensity = [i for i in post_intensity]

    return pre_intensity,post_intensity


def get_list_group(data,label_group):
    data_group    = data[data["Label_group"]==label_group]

    pre = []
    post = []
    for chamber in np.unique(data_group["groupID"]):
        subdata = data_group[data_group["groupID"]==chamber]
        pre  +=get_value(subdata)[0]
        post +=get_value(subdata)[1]

    return pre,post

def get_list_group_raw(data,label_group):
    data_group    = data[data["Label_group"]==label_group]

    pre = []
    post = []
    for chamber in np.unique(data_group["groupID"]):
        subdata = data_group[data_group["groupID"]==chamber]
        pre  += get_value_raw(subdata)[0]
        post += get_value_raw(subdata)[1]

    return pre,post



def plot_lines(data,ax,label_group,colors):
    pre,post  = get_list_group_raw(data,label_group)

    if label_group == 'chamber':
        print("chamber")
        print(len(pre))

        for i in np.arange(0,len(post),1):
            ax.plot([1,2],[pre[i],post[i]],'-',color='#1f77b4ff',alpha=0.2)
        x = np.array([1,2])
        y = np.array([np.mean(pre),np.mean(post)])
        yerr = np.array([abs(sp.stats.sem(pre)),abs(sp.stats.sem(post))])
        ax.errorbar(x,y,yerr,marker='o',color=colors[2],ecolor=colors[2],markerfacecolor=colors[2],markeredgecolor=colors[2],capsize=3.,linewidth=2,label='chamber')
        print("chamber")
        print(sp.stats.wilcoxon(pre,post)[1])
        if sp.stats.wilcoxon(pre,post)[1]>0.05:
            ax.text(2.1,np.mean(post),"ns",fontsize=8,ha='left',va='center')

    if label_group == 'dcEF':
        print("dcEF")
        print(len(pre))
        for i in np.arange(0,len(post),1):
            ax.plot([1,2],[pre[i],post[i]],'-',color=colors[3],alpha=0.2)
        x = np.array([1,2])
        y = np.array([np.mean(pre),np.mean(post)])
        yerr = np.array([abs(sp.stats.sem(pre)),abs(sp.stats.sem(post))])
        ax.errorbar(x,y,yerr,marker='o',color=colors[3],ecolor=colors[3],markerfacecolor=colors[3],markeredgecolor=colors[3],capsize=3.,linewidth=2,label='dcEF')
        print("dcEF")
        print(sp.stats.wilcoxon(pre,post)[1])
        if sp.stats.wilcoxon(pre,post)[1]>0.05:
            ax.text(2.1,np.mean(post),"ns",fontsize=8,ha='left',va='center')

    if label_group == 'LPS':
        print("LPS")
        print(len(pre))

        for i in np.arange(0,len(post),1):
            ax.plot([1,2],[pre[i],post[i]],'-',color=colors[1],alpha=0.2)
        x = np.array([1,2])
        y = np.array([np.mean(pre),np.mean(post)])
        yerr = np.array([abs(sp.stats.sem(pre)),abs(sp.stats.sem(post))])
        ax.errorbar(x,y,yerr,marker='o',color=colors[1],ecolor=colors[1],markerfacecolor=colors[1],markeredgecolor=colors[1],capsize=3.,linewidth=2,label='LPS')
        print("LPS")
        print(sp.stats.wilcoxon(pre,post)[1])
        if sp.stats.wilcoxon(pre,post)[1]<0.001:
            ax.text(2.1,np.mean(post),"***",fontsize=12,ha='left',va='center')

    ax.legend(bbox_to_anchor=(0.0, 0.7, 1, 0.2), loc=3,ncol=1, mode="expand", borderaxespad=0.,frameon=False,fontsize=6)

def plot_lines_normed(data,ax,label_group,colors):
    pre,post  = get_list_group(data,label_group)

    if label_group == 'chamber':
        x = np.array([1,2])
        y = np.array([1,np.mean(post)])
        yerr = np.array([0,abs(sp.stats.sem(post))])
        ax.errorbar(x,y,yerr,marker='o',color=colors[2],ecolor=colors[2],markerfacecolor=colors[2],markeredgecolor=colors[2],capsize=3.,label='chamber')



    if label_group == 'dcEF':
        x = np.array([1,2])
        y = np.array([1,np.mean(post)])
        yerr = np.array([0,abs(sp.stats.sem(post))])
        ax.errorbar(x,y,yerr,marker='o',color=colors[3],ecolor=colors[3],markerfacecolor=colors[3],markeredgecolor=colors[3],capsize=3.,label='dcEF')


    if label_group == 'LPS':
        x = np.array([1,2])
        y = np.array([1,np.mean(post)])
        yerr = np.array([0,abs(sp.stats.sem(post))])
        ax.errorbar(x,y,yerr,marker='o',color=colors[1],ecolor=colors[1],markerfacecolor=colors[1],markeredgecolor=colors[1],capsize=3.,label='LPS')



fig = plt.figure(figsize=(cm2inch(5), cm2inch(4.4)))
gs1 = gridspec.GridSpec(1, 1)
gs1.update(top=0.97,bottom=0.12,left=0.22,right=0.99,hspace=0.1,wspace=0.1)
ax1 = plt.subplot(gs1[0,0])
colors = ['#293241','#ee6c4d','#98c1d9','#3d5a80']
data = pd.read_csv("data_merged.csv")
plot_lines(data,ax1,"chamber",colors)
plot_lines(data,ax1,"dcEF",colors)
plot_lines(data,ax1,"LPS",colors)

ax1.spines['right'].set_visible(False)
ax1.spines['top'].set_visible(False)
ax1.yaxis.set_ticks_position('left')
ax1.xaxis.set_ticks_position('bottom')
ax1.set_xlim(0.5,2.5)
ax1.set_xticks([1,2])
ax1.set_xticklabels(["baseline","after treatment"])
ax1.set_ylabel(r"$\mathrm{\bf{eGFP\ intensity}}$ | a.u.")
plt.savefig("TNF-stats-raw.svg")




fig = plt.figure(figsize=(cm2inch(3), cm2inch(2.5)))
gs1 = gridspec.GridSpec(1, 1)
gs1.update(top=0.97,bottom=0.12,left=0.22,right=0.99,hspace=0.1,wspace=0.1)
ax1 = plt.subplot(gs1[0,0])

data = pd.read_csv("data_merged.csv")
plot_lines_normed(data,ax1,"chamber",colors)
plot_lines_normed(data,ax1,"dcEF",colors)
plot_lines_normed(data,ax1,"LPS",colors)

ax1.axhline(y=1,linestyle='--',color='k',linewidth=0.5)
ax1.spines['right'].set_visible(False)
ax1.spines['top'].set_visible(False)
ax1.yaxis.set_ticks_position('left')
ax1.xaxis.set_ticks_position('bottom')
ax1.text(1.25,1.01,"baseline",va='bottom',ha='left',fontsize=6)
ax1.set_xlim(0.5,2.5)
ax1.set_xticks([1,2])
ax1.set_xticklabels(["baseline","after-"])
ax1.set_ylabel(r"$\mathrm{\bf{normalized}}$")
plt.savefig("TNF-stats-normed.svg")
plt.show()