import numpy as np
from dynamics.bodies.body import Body

def sort_and_sweep(bodies: list[Body] , axis: int):
    """
    Sorts bodies along the given axis and returns a list of pairs of bodies that overlap along that axis.
    
    :param bodies: The bodies to sort and sweep.
    :param axis: The axis to sort and sweep along.
    :return: A list of pairs of bodies that overlap along the given axis.
    """
    bodies.sort(key=lambda body: body.get_bounding_volume().get_extend_along_axis(axis)[0])
    overlapping_bodies = list()
    for i in range(len(bodies)):
        for j in range(i + 1, len(bodies)):
            min = bodies[i].get_bounding_volume().get_extend_along_axis(axis)[0]
            max = bodies[j].get_bounding_volume().get_extend_along_axis(axis)[1]
            if min > max:
                break
            overlapping_bodies.append((bodies[i], bodies[j]))
    return overlapping_bodies