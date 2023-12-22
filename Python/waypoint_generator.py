#!/usr/bin/env python3

import carla
import time

from agents.navigation.global_route_planner import GlobalRoutePlanner

def main():

    client = carla.Client("localhost", 2000)
    client.set_timeout(10)

    world = client.get_world()

    amap = world.get_map()
    sampling_resolution = 3
    grp = GlobalRoutePlanner(amap, sampling_resolution)
    spawn_points = amap.get_spawn_points()
    print(len(spawn_points))
    print('\n')
    a = carla.Location(spawn_points[0].location)
    b = carla.Location(spawn_points[1].location)

    w1 = grp.trace_route(a, b)

    for w in w1:
        world.debug.draw_string(w[0].transform.location, 'O', draw_shadow=False,
        color=carla.Color(r=0, g=0, b=255), life_time=20.0,
        persistent_lines=True)
        print(w[0].transform.location)
        time.sleep(0.1)

    print('\nBye!')

if __name__ == '__main__':

    main()
