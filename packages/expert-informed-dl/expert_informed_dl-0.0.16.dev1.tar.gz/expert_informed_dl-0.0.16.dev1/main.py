用了
from signal import signal, SIGINT
import ray
from utils import (
    load_config,
    parse_args,
    setup,
    exit_handler,
    mkdir_and_save_config)
from os.path import exists, basename, abspath, dirname
from time import time
from copy import copy
from json import dump
from tqdm import tqdm
import numpy as np
from pathlib import Path
from random import shuffle as shuffle_f
import pickle
from itertools import chain
import os


def step_env(all_envs, ready_envs, ready_actions, remaining_observations):
    remaining_observations.extend([e.step.remote(a)
                                   for e, a in zip(ready_envs, ready_actions)])
    step_retval = []
    start = time()
    total = 0
    while True:
        ready, remaining_observations = ray.wait(
            remaining_observations, num_returns=1, timeout=0.01)
        if len(ready) == 0:
            continue
        step_retval.extend(ready)
        total = time() - start
        if (total > 0.01 and len(step_retval) > 0)\
                or len(step_retval) == len(all_envs):
            break

    observations = []
    ready_envs = []

    for obs, env_id in ray.get(step_retval):
        observations.append(obs)
        ready_envs.append(env_id['val'])

    return ready_envs, observations, remaining_observations


def step_rrt_ep(all_envs, ready_envs, remaining_episodes):
    remaining_episodes.extend([e.save_expert_episode.remote()
                                   for e in ready_envs])
    save_expert_episode_retval = []
    start = time()
    total = 0
    while True:
        ready, remaining_episodes = ray.wait(
            remaining_episodes, num_returns=1, timeout=0.01)
        if len(ready) == 0:
            continue
        save_expert_episode_retval.extend(ready)
        total = time() - start
        if (total > 0.01 and len(save_expert_episode_retval) > 0)\
                or len(save_expert_episode_retval) == len(all_envs):
            break

    episodes = []
    ready_envs = []

    for ep, env_id in ray.get(save_expert_episode_retval):
        episodes.append(ep)
        ready_envs.append(env_id['val'])

    return ready_envs, episodes, remaining_episodes


def simulate(args, config):
    # Set up pybullet env and policies
    envs, policy_manager, keep_alive = setup(args, config)
    signal(SIGINT, lambda sig, frame: exit_handler(
        [value['exit_handler'] for key, value in keep_alive.items()
         if value['exit_handler'] is not None]))

    observations = ray.get([e.reset.remote() for e in envs])
    observations = [obs for obs, _ in observations]

    inference_policies = policy_manager.get_inference_nodes()
    multiarm_motion_planner = inference_policies['multiarm_motion_planner']
    if args.mode == 'benchmark':
        multiarm_motion_planner.deterministic = True

    remaining_observations = []
    ready_envs = copy(envs)
    while(True):
        env_actions = [multiarm_motion_planner.act(
            observation['multiarm_motion_planner'])
            for observation in observations]
        ready_envs, observations, remaining_observations = step_env(
            all_envs=envs,
            ready_envs=ready_envs,
            ready_actions=env_actions,
            remaining_observations=remaining_observations)
        print('\r{:02d}'.format(len(observations)), end='')


def generate_expert_dataset(args, config):
    if not os.path.exists("expert_episodes"):
        os.mkdir("expert_episodes")

    envs, policy_manager, keep_alive = setup(args, config)
    signal(SIGINT, lambda sig, frame: exit_handler(
        [value['exit_handler'] for key, value in keep_alive.items()
         if value['exit_handler'] is not None]))

    remaining_episodes = []
    ready_envs = copy(envs)

    start = time()
    ct = 1
    total_episodes = 250000
    while(True):
        # episodes = ray.get([e.save_expert_episode.remote() for e in envs])

        ready_envs, episodes, remaining_episodes = step_rrt_ep(envs, ready_envs, remaining_episodes)
        ct += len(episodes)

        sec_per_ep = (time() - start) / ct
        elapsed = ct * sec_per_ep
        remaining = (total_episodes - ct) * sec_per_ep
        print(f"Completed {ct - 1} | Elapsed {elapsed:0.1f}s | Remaining {remaining:0.1f}s | Rate {sec_per_ep:0.3f}s/ep")



    # observations = ray.get([e.reset.remote() for e in envs])
    # observations = [obs for obs, _ in observations]
    #
    # inference_policies = policy_manager.get_inference_nodes()
    # multiarm_motion_planner = inference_policies['multiarm_motion_planner']
    #
    # remaining_observations = []
    # ready_envs = copy(envs)
    #
    # while(True):
    #     env_actions = [multiarm_motion_planner.act(
    #         observation['multiarm_motion_planner'])
    #         for observation in observations]
    #     ready_envs, observations, remaining_observations = step_env(
    #         all_envs=envs,
    #         ready_envs=ready_envs,
    #         ready_actions=env_actions,
    #         remaining_observations=remaining_observations)
    #     print('\r{:02d}'.format(len(observations)), end='')


    # iterate through the expert waypoints
    # for args["expert_waypoints"]

    # perform the actions according to the waypoints while recording data

    # save data for this expert demonstration episode

if __name__ == "__main__":
    args = parse_args()
    config = load_config(args.config)
    if args.mode == 'train' or\
            args.mode == 'benchmark' or\
            args.mode == 'enjoy':
        simulate(args, config)
    elif args.mode == 'behaviour-clone':
        signal(SIGINT, lambda sig, frame: exit_handler(None))
        setup(args, config)()

    # generate the expert dataset from waypoints
    elif args.mode == 'expert':
        generate_expert_dataset(args, config)
