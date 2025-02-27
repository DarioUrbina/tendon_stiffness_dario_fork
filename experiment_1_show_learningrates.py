
# next is to add accel and see the difference
# add stiffness too
import numpy as np
from scipy import signal, stats
from matplotlib import pyplot as plt
import colorsys
from all_functions import *
import pickle
from warnings import simplefilter
import matplotlib

simplefilter(action='ignore', category=FutureWarning)

matplotlib.rcParams['pdf.fonttype'] = 42
matplotlib.rcParams['ps.fonttype'] = 42

experiment_ID="experiment_1B"

stiffness_versions = 9#[0, 500, 1000, 2000, 4000, 7000, 10000. 15000, 20000]
mc_run_number = 50
babbling_times = [3]#np.arange(1,1+5)
epoch_numbers = 20
epoch_numbers_to_show = 10

histories = np.empty([mc_run_number, len(babbling_times), stiffness_versions]).tolist()
learning_errors = np.zeros([mc_run_number, len(babbling_times), stiffness_versions, epoch_numbers])
fig, axes = plt.subplots(nrows=1, ncols=1, figsize=(6, 4.5))
for stiffness_ver in range(stiffness_versions):
	MuJoCo_model_name="nmi_leg_w_chassis_air_v{}.xml".format(stiffness_ver)
	for babbling_time_cntr in range(len(babbling_times)):
		for mc_counter in range(mc_run_number):
			logdir="./logs/{}/scalars/stiffness_v{}/babbling_time_{}_mins/mc_run{}".format(experiment_ID, stiffness_ver,babbling_times[babbling_time_cntr], mc_counter)
			with open(logdir+'/trainHistoryDict.pickle', 'rb') as file_pi:
				history=pickle.load(file_pi)
			histories[mc_counter][babbling_time_cntr][stiffness_ver] = history
			learning_errors[mc_counter, babbling_time_cntr, stiffness_ver, :] = np.array(history['loss'])
learning_errors_per_stiffness = np.zeros([stiffness_versions, epoch_numbers])
for stiffness_ver in range(stiffness_versions):
	learning_errors_per_stiffness[stiffness_ver,:] = learning_errors[:, :, stiffness_ver, :].mean(0).squeeze()
	axes.plot(np.arange(1,epoch_numbers_to_show+1), learning_errors_per_stiffness[stiffness_ver,:epoch_numbers_to_show],
		color=colorsys.hsv_to_rgb((8.75-stiffness_ver)/14,1,.75), alpha=.65, linewidth=3.0)
#(50, 1, 9, 20) 
plt.sca(axes)
#plt.ylim([0.035,0.1])
plt.legend(['K: 0', 'K: 500', 'K: 1k', 'K: 2k', 'K: 4k', 'K: 7k', 'K: 10k', 'K: 15k', 'K: 20k'],fontsize='small')
plt.xticks(np.arange(1,epoch_numbers_to_show+1,1), np.arange(1,epoch_numbers_to_show+1,1),
	rotation=45, fontsize=8)

plt.xlabel("Epoch #", fontsize=9)
#axes.set_xlabel("epoch #")
plt.ylabel("Epoch MSE", fontsize=9)
plt.yticks(np.arange(0.035,0.096,0.005),rotation=45, fontsize=8)
plt.title("Learning curves for different stiffness values (S)", fontsize=10)
#plt.grid()
fig.savefig('./results/{}/exp1_learningcurves.pdf'.format(experiment_ID))
fig.savefig('./results/figures/exp1_learningcurves.pdf'.format(experiment_ID))
plt.show()



#import pdb; pdb.set_trace()
