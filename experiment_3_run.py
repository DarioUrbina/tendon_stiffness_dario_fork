
# next is to add accel and see the difference
# add stiffness too
import tensorflow as tf
import numpy as np
from matplotlib import pyplot as plt
from all_functions import *
import pickle
from warnings import simplefilter

simplefilter(action='ignore', category=FutureWarning)

experiment_ID = "experiment_3_tmp"

mc_run_number = 50
babbling_time = 3
number_of_refinements = 0
stiffness_versions = 9
# errors_all_A_A = np.zeros([2, number_of_refinements+1, mc_run_number])
# errors_all_A_B = np.zeros([2, number_of_refinements+1, mc_run_number])
# errors_all_B_B = np.zeros([2, number_of_refinements+1, mc_run_number])



rewards_all = np.zeros([mc_run_number, stiffness_versions])
energies_all = np.zeros([mc_run_number, stiffness_versions])
exploration_run_no_all = np.zeros([mc_run_number, stiffness_versions])

for stiffness_version_A in range(stiffness_versions):

	MuJoCo_model_name_A="nmi_leg_w_chassis_air_v{}.xml".format(stiffness_version_A)
	MuJoCo_model_name_A_walk="nmi_leg_w_chassis_air_v{}_walk.xml".format(stiffness_version_A)

	random_seed = -1

	for mc_counter in range(mc_run_number):
		random_seed+=1
		# train model_A
		np.random.seed(random_seed) # change the seed for different initial conditions
		tf.random.set_random_seed(random_seed)
		[babbling_kinematics, babbling_activations] =\
			babbling_fcn(
				MuJoCo_model_name=MuJoCo_model_name_A,
				simulation_minutes=babbling_time,
				kinematics_activations_show=False)
		model_A_babble = inverse_mapping_fcn(
			kinematics=babbling_kinematics,
			activations=babbling_activations,
			log_address="./logs/{}/scalars/stiffness_version{}/babble_A_mc_run{}/".format(experiment_ID, stiffness_version_A, mc_counter),
			early_stopping=False)
		cum_kinematics_A_babble = babbling_kinematics
		cum_activations_A_babble = babbling_activations
		#A_A test
		np.random.seed(random_seed) # change the seed for different initial conditions
		tf.random.set_random_seed(random_seed)
		[ best_reward_so_far, all_rewards, best_features_so_far, real_attempt_activations, exploration_run_no ]=\
		learn_to_move_2_fcn(
			MuJoCo_model_name=MuJoCo_model_name_A_walk,
			model=model_A_babble,
			cum_kinematics=cum_kinematics_A_babble,
			cum_activations=cum_activations_A_babble,
			reward_thresh=7,
			refinement=False,
			Mj_render=False)
		[rewardA_A, _, _, _, real_attempt_activations]=\
		feat_to_run_attempt_fcn(
			MuJoCo_model_name=MuJoCo_model_name_A_walk,
			features=best_features_so_far,
			model=model_A_babble,
			feat_show=False,
			Mj_render=False)
		total_energyA_A = np.square(real_attempt_activations).sum(0).sum(0)

		print("traveled distance: ", rewardA_A)
		print("consumed energy: ", total_energyA_A)
		exploration_run_no_all[mc_counter, stiffness_version_A] = exploration_run_no
		rewards_all[mc_counter, stiffness_version_A] = rewardA_A
		energies_all[mc_counter, stiffness_version_A] = total_energyA_A

os.makedirs("./results/{}".format(experiment_ID), exist_ok=True)
np.save("./results/{}/exploration_run_no_all".format(experiment_ID),exploration_run_no_all)
np.save("./results/{}/rewards_all".format(experiment_ID),rewards_all)
np.save("./results/{}/energies_all".format(experiment_ID),energies_all)
#print("best_reward_so_far: ", best_reward_so_far)
## printing the results
# print("errors_mean: ",errors_all_A_A.mean(1))
# print("errors_std: ",errors_all_A_A.std(1))
# print("errors_mean: ",errors_all_A_B.mean(1))
# print("errors_std: ",errors_all_A_B.std(1))

# import pdb; pdb.set_trace()
