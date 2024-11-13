import math

import numpy as np
from matplotlib import pyplot as plt


class Particle:
    def __init__(self, x, y, velocity):
        self.pos = [x, y]
        self.velocity = velocity
        self.best_pos = self.pos.copy()
        self.best_solution = evaluate(self.pos)


class Swarm:
    def __init__(self, pop, v_max, lower_bound, upper_bound):
        self.particles = []
        self.best_pos = None
        self.best_solution = math.inf

        for _ in range(pop):
            x = np.random.uniform(lower_bound, upper_bound)
            y = np.random.uniform(lower_bound, upper_bound)
            velocity = np.random.rand(2) * v_max
            particle = Particle(x, y, velocity)
            self.particles.append(particle)

            self.best_pos = particle.pos.copy()
            self.best_solution = particle.best_solution


def evaluate(xy):
    result = (-12) * xy[1] + 4 * pow(xy[0], 2) + 4 * pow(xy[1], 2) - 4 * xy[0] * xy[1]
    return result


def generate_swarm(population, v_max, lower_bound, upper_bound):
    swarm = Swarm(population, v_max, lower_bound, upper_bound)
    return swarm


def PSO(swarm, iteration_num, personal_coef, social_coef, v_max, lower_bound, upper_bound, inertia,
        modification_flag, iteration_number_hist):
    # x = np.linspace(lower_bound, upper_bound, 50)
    # y = np.linspace(lower_bound, upper_bound, 50)
    # fig = plt.figure("PSO")

    inertia_weight = inertia

    curr_iter = 0
    while curr_iter < iteration_num:

        # fig.clf()
        # ax = fig.add_subplot(1, 1, 1)

        for particle in swarm.particles:

            for i in range(0, 2):
                r1 = np.random.uniform(0, 1)
                r2 = np.random.uniform(0, 1)

                personal_coefficient = personal_coef * r1 * (particle.best_pos[i] - particle.pos[i])
                social_coefficient = social_coef * r2 * (swarm.best_pos[i] - particle.pos[i])

                if modification_flag is True:
                    if personal_coef + social_coef > 4.0:
                        phi: float = personal_coef + social_coef
                        constriction_factor: float = 2 / abs(2 - phi - math.sqrt(pow(phi, 2) - 4 * phi))
                    else:
                        constriction_factor = 0.729
                else:
                    constriction_factor = 1

                new_velocity = constriction_factor * (
                        inertia_weight * particle.velocity[i] +
                        personal_coefficient +
                        social_coefficient
                )

                particle.velocity[i] = np.clip(new_velocity, -v_max, v_max)

                # ax.scatter(particle.pos[0], particle.pos[1], marker='o', c='g')
                # ax.arrow(particle.pos[0], particle.pos[1], particle.velocity[0], particle.velocity[1], head_width=0.0001,
                #          head_length=0.0001, width=0.001, length_includes_head=False, color='k')
                # ax.set_xlim(lower_bound, upper_bound)
                # ax.set_ylim(lower_bound, upper_bound)
                particle.pos += particle.velocity
                particle.best_solution = evaluate([particle.pos[0], particle.pos[1]])

                if particle.best_solution < evaluate([particle.best_pos[0], particle.best_pos[1]]):
                    particle.best_pos = particle.pos.copy()

                    if particle.best_solution < swarm.best_solution:
                        swarm.best_pos = particle.pos.copy()
                        swarm.best_solution = particle.best_solution
                        print(
                            f'Best solution found! {swarm.best_solution + 12.0} coordinates are {swarm.best_pos} iteration number {curr_iter + iteration_number_hist}')

                np.clip(particle.pos, lower_bound, upper_bound)

        # plt.subplots_adjust(right=0.95)
        # plt.pause(0.00001)

        curr_iter += 1
    return swarm

#
# population = 50
# v_max = 15
# iteration_num = 100
# personal_coef = 2.05
# social_coef = 2.05
# swarm = Swarm(population, v_max, -10, 10)
# swarm = PSO(swarm, iteration_num, personal_coef, social_coef, v_max, -10, 10, 0.3)
