from gymnasium import spaces
import numpy as np
from py4j.java_gateway import is_instance_of, get_java_class
import pickle
import os
from filelock import FileLock
    

def convert_gym_action_to_anylogic(anylogic_model, action_space, action):
    """[INTERNAL] Convert gym action to a type that can be consumed by AnyLogic model"""
    if isinstance(action_space, spaces.Discrete):
        return int(action)
    elif isinstance(action_space, spaces.Box) and action.size == 1:
        return float(action[0])
    elif isinstance(action_space, spaces.Tuple) and len(action_space.spaces) == 1:
        return int(action[0]) if np.issubdtype(type(action[0]), np.integer) else float(action[0])
    # TODO: spaces.Dict, spaces.Sequence

    # Assume it is a 'spaces.Tuple' and create a Number[] type that can be consumed
    # by java model
    return get_java_number_array(anylogic_model, action)

def get_java_number_array(anylogic_model, action):
    """[INTERNAL] Convert python array to a java Number[] type"""
    # Format to Number[] type if anylogic model is provided
    if anylogic_model is not None:
        # First get 'Number' class from JVM
        number_class = anylogic_model.jvm.java.lang.Number
        # Create 'Number' array using 'py4j'
        number_array = anylogic_model.new_array(number_class, len(action))
        # Populate array with values from action and cast them accordingly
        for i, v in enumerate(action):
            number_array[i] = int(v) if np.issubdtype(type(v), np.integer) else float(v)
        return number_array
    # Otherwise, just return the action as a list
    else:
        # Initialize action list
        action_list = []
        # Populate list with values from action and cast them accordingly
        for v in action:
            action_list.append(int(v) if np.issubdtype(type(v), np.integer) else float(v))
        return action_list

def convert_anylogic_space_to_gym(anylogic_model, java_space):
    """[INTERNAL] Convert AnyLogic space into a gymnasium.spaces compatible type"""
    # NOTE: For scalability and flexibility, it is assumed that all spaces
    # will be individually added into a 'spaces.Tupble'
    # Initialize spaces list which can hold Discrete or Box spaces
    space_list = []
    # Create gym spaces and add to list individually
    for i in range(java_space.size()):
        space_list.append(__convert_anylogic_range_to_gym_space(anylogic_model, java_space.get(i)))
    return spaces.Tuple(space_list)

def __convert_anylogic_range_to_gym_space(anylogic_model, java_range):
    """[INTERNAL] Parse AnyLogic range into a gymnasium.spaces compatible type"""
    # Create a discrete space
    if is_instance_of(anylogic_model, java_range, 'com.alpype.DiscreteRLRange'):
        return spaces.Discrete(java_range.size())

    # Create a continuous space using 'spaces.Box'
    elif is_instance_of(anylogic_model, java_range, 'com.alpype.ContinuousRLRange'):
        # First get upper and lower bounds
        # They will be automatically parsed to python 'None' if they are
        # 'null' in java
        lb = java_range.lb()
        ub = java_range.ub()
        # Create a box space
        return spaces.Box(
            low=lb if lb is not None else -np.finfo(np.float32).max,
            high=ub if ub is not None else np.finfo(np.float32).max,
            dtype=np.float32
        )
    raise Exception(f"Unknown space entry type '{get_java_class(java_range)}'")

def load_space(location_path):
    """[INTERNAL] Load space from given location"""
    # Load space from given location
    with open(location_path, 'rb') as f:
        space = pickle.load(f)
    return space

def save_space(space, location_path):
    """[INTERNAL] Save space to given location"""
    # First, create location directory if it does not exist
    os.makedirs(os.path.dirname(location_path), exist_ok=True)
    # Define the lock file path
    lock_file_path = location_path + '.lock'
    # Use a file lock for synchronization across processes
    with FileLock(lock_file_path):
        # Save space to given location
        with open(location_path, 'wb') as f:
            pickle.dump(space, f)
