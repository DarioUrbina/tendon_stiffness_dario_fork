# next is to add accel and see the difference
# add stiffness too
import numpy as np
from scipy import signal, stats
from matplotlib import pyplot as plt
from all_functions import *
import pickle
from warnings import simplefilter

def exp2_learning_curves_cal_fcn(errors_all):
	average_curve_mean = errors_all.mean(0).mean(1)
	q0_curve_mean = errors_all[0].mean(1)
	q1_curve_mean = errors_all[1].mean(1)
	average_curve_std = errors_all.mean(0).std(1)
	q0_curve_std = errors_all[0].std(1)
	q1_curve_std = errors_all[1].std(1)
	return average_curve_mean, q0_curve_mean, q1_curve_mean, average_curve_std, q0_curve_std, q1_curve_std 

simplefilter(action='ignore', category=FutureWarning)

import matplotlib
matplotlib.rcParams['pdf.fonttype'] = 42
matplotlib.rcParams['ps.fonttype'] = 42

experiment_ID = "experiment_2_2way"
number_of_refinements = 5
errors_all_cyc_A_A = np.load("./results/{}/errors_all_cyc_A_A.npy".format(experiment_ID))
errors_all_cyc_A_B = np.load("./results/{}/errors_all_cyc_A_B.npy".format(experiment_ID))
errors_all_cyc_B_B = np.load("./results/{}/errors_all_cyc_B_B.npy".format(experiment_ID))
errors_all_cyc_B_A = np.load("./results/{}/errors_all_cyc_B_A.npy".format(experiment_ID))

errors_all_p2p_A_A = np.load("./results/{}/errors_all_p2p_A_A.npy".format(experiment_ID))
errors_all_p2p_A_B = np.load("./results/{}/errors_all_p2p_A_B.npy".format(experiment_ID))
errors_all_p2p_B_B = np.load("./results/{}/errors_all_p2p_B_B.npy".format(experiment_ID))
errors_all_p2p_B_A = np.load("./results/{}/errors_all_p2p_B_A.npy".format(experiment_ID))

number_of_mods = 8
errors_all = np.zeros((number_of_mods,)+errors_all_cyc_A_A.shape)
average_curve_mean_all = np.zeros([number_of_mods,number_of_refinements+1])
q0_curve_mean_all = np.zeros([number_of_mods,number_of_refinements+1])
q1_curve_mean_all= np.zeros([number_of_mods,number_of_refinements+1])
average_curve_std_all = np.zeros([number_of_mods,number_of_refinements+1])
q0_curve_std_all = np.zeros([number_of_mods,number_of_refinements+1])
q1_curve_std_all= np.zeros([number_of_mods,number_of_refinements+1])
errors_all = \
np.array([errors_all_cyc_A_A,
errors_all_cyc_B_A,
errors_all_cyc_B_B,
errors_all_cyc_A_B,
errors_all_p2p_A_A,
errors_all_p2p_B_A,
errors_all_p2p_B_B,
errors_all_p2p_A_B])
for mod_iter in range(number_of_mods):
	[average_curve_mean_all[mod_iter,:], q0_curve_mean_all[mod_iter,:], q1_curve_mean_all[mod_iter,:],
	average_curve_std_all[mod_iter,:], q0_curve_std_all[mod_iter,:], q1_curve_std_all[mod_iter,:]] = \
	exp2_learning_curves_cal_fcn(errors_all=errors_all[mod_iter,:])
## plots
show_p2p = False
y_lim=[0.1, .78]

A_A_color = 'forestgreen'
B_A_color = 'lightgreen'

B_B_color = 'firebrick'
A_B_color = 'orange'

mod_colors = [A_A_color, B_A_color, B_B_color, A_B_color]

if show_p2p:
	nrows = 2
else:
	nrows = 1
ncols = 3
fig, axes = plt.subplots(nrows=nrows, ncols=ncols, figsize=(9, 3))
title_texts = ['average across both joints', 'proximal joint ($q_0$)', 'distal joint ($q_1$)']
for mod_iter in range(number_of_mods):
	#axes[np.divmod(mod_iter,3)[0]][np.divmod(mod_iter,3)[1]].plot(mean_curve_all[mod_iter,:])
	if show_p2p:
		if mod_iter < number_of_mods/2:
			axes[0][0].errorbar(x=np.arange(number_of_refinements+1)+mod_iter/10, y=average_curve_mean_all[mod_iter,:], yerr=average_curve_std_all[mod_iter,:]/2, capsize=2)
			axes[0][1].errorbar(x=np.arange(number_of_refinements+1)+mod_iter/10, y=q0_curve_mean_all[mod_iter,:], yerr=q0_curve_std_all[mod_iter,:]/2, capsize=2)
			axes[0][2].errorbar(x=np.arange(number_of_refinements+1)+mod_iter/10, y=q1_curve_mean_all[mod_iter,:], yerr=q1_curve_std_all[mod_iter,:]/2, capsize=2)
			for ii in range(ncols):
				plt.sca(axes[0][ii])
				plt.xticks(range(number_of_refinements+1), [])
		else:
			axes[1][0].errorbar(x=np.arange(number_of_refinements+1)+mod_iter/10, y=average_curve_mean_all[mod_iter,:], yerr=average_curve_std_all[mod_iter,:]/2, capsize=2)
			axes[1][1].errorbar(x=np.arange(number_of_refinements+1)+mod_iter/10, y=q0_curve_mean_all[mod_iter,:], yerr=q0_curve_std_all[mod_iter,:]/2, capsize=2)
			axes[1][2].errorbar(x=np.arange(number_of_refinements+1)+mod_iter/10, y=q1_curve_mean_all[mod_iter,:], yerr=q1_curve_std_all[mod_iter,:]/2, capsize=2)
			for ii in range(ncols):
				plt.sca(axes[1][ii])
				plt.xticks(range(number_of_refinements+1), ['babbling', 'refinement #1','refinement #2','refinement #3','refinement #4','refinement #5'], rotation=30, ha='right')
	else:
		if mod_iter < number_of_mods/2:
			axes[0].errorbar(x=np.arange(number_of_refinements+1)+mod_iter/10, 
				y=average_curve_mean_all[mod_iter,:], yerr=average_curve_std_all[mod_iter,:]/2, capsize=2,
				color=mod_colors[mod_iter],animated=True)
			axes[0].plot(np.arange(number_of_refinements+1)+mod_iter/10, 
				average_curve_mean_all[mod_iter,:],'--',color=mod_colors[mod_iter],alpha=.7)
			axes[1].errorbar(x=np.arange(number_of_refinements+1)+mod_iter/10, 
				y=q0_curve_mean_all[mod_iter,:], yerr=q0_curve_std_all[mod_iter,:]/2, capsize=2,
				color=mod_colors[mod_iter],animated=True)
			axes[1].plot(np.arange(number_of_refinements+1)+mod_iter/10, 
				q0_curve_mean_all[mod_iter,:],'--',color=mod_colors[mod_iter],alpha=.7)
			axes[2].errorbar(x=np.arange(number_of_refinements+1)+mod_iter/10, 
				y=q1_curve_mean_all[mod_iter,:], yerr=q1_curve_std_all[mod_iter,:]/2, capsize=2,
				color=mod_colors[mod_iter],animated=True)
			axes[2].plot(np.arange(number_of_refinements+1)+mod_iter/10, 
				q1_curve_mean_all[mod_iter,:],'--',color=mod_colors[mod_iter],alpha=.7)
			for ii in range(ncols):
				plt.sca(axes[ii])
				plt.xticks(range(number_of_refinements+1), ['babbling', 'refinement #1','refinement #2','refinement #3','refinement #4','refinement #5'], rotation=30, ha='right',fontsize=8)	
				plt.title(title_texts[ii], fontsize=10)
				plt.yticks(rotation=45, fontsize=8)
				if ii==0:
					plt.ylabel("RMSE (rads)", fontsize=8)
				# else:
				# 	plt.yticks()

for subplot_iter in range(nrows*ncols):
	if show_p2p:
		axes[np.divmod(subplot_iter,3)[0]][np.divmod(subplot_iter,3)[1]].set_ylim(y_lim)
		axes[np.divmod(subplot_iter,3)[0]][np.divmod(subplot_iter,3)[1]].legend(['A_A','B_A','B_B','A_B'], fontsize=6)
	else:
		axes[subplot_iter].set_ylim(y_lim)
		#axes[subplot_iter].grid()
axes[-1].legend(['A_A','B_A','B_B','A_B'], fontsize=6)

fig.subplots_adjust(top=.9, bottom=.2, left=.06, right=.95)
fig.savefig('./results/{}/exp2_learningcurves.pdf'.format(experiment_ID))
fig.savefig('./results/figures/exp2_learningcurves.pdf'.format(experiment_ID))
plt.show()
#import pdb; pdb.set_trace()
