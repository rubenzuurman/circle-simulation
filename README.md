# circle-simulation

Gravity simulation using circles, the circles can merge and emit smaller circles when they gain mass

# Plan

## Simulate a bunch of circles
    - The mass of a circle is proportional to its area.
        - Candidate 1: m=r^2
    - The circles are subject to the force of gravity.
    - When two circles touch, they merge into one circle with an area equal to the sum of the areas of the two merging circles.
    - Circles have a chance of emitting a particle of mass one, this chance is equal to some function of the mass, proportional to the circumference.
        - Note: the function must equal zero when the mass is equal to one.
        - Note: the function must equal one when the mass is infinite, or at some cutoff point after which it is clamped to one.
        - Note: the function will be clamped between zero and one.
        - Candidate 1: c(m)=a\*sqrt(m-1), where `a` is a constant in the interval [0, 1] determining the cutoff point from where the chance becomes one, the lower `a`, the higher the cutoff point.
    - Every timestep the state of the simulation will be saved in the following form.
        - Dictionary containing the current time, max time, current timestep, number of particles, and a list for every particle of the form [id, position, velocity, mass, radius].
        - The size of the saved data will be approximately equal to the following:
            - Every timestep: <32 bytes+<32 bytes+<32 bytes+number_of_particles\*<32 bytes, meaning the size of a timestep <96+32n bytes.
            - Thus for t timesteps the data will have a size <96t+32nt bytes.
            - Example: 100 particles for 1000000 timesteps: <96\*1000000+32\*100\*1000000=96.000.000+3.200.000.000\~3.3 billion bytes\~3.073 GB.
    - The savedata will be split into chunks of 100 MB.

## Visualize the simulation
    - Load first 100 MB chunk.
    - Render timesteps until at 50% of the loaded data, then load next chunk, unload previous chunk.

# Versions

## Version 0.1
    - Simulation of single particle moving in a straight line.
    - Visualization fully implemented.
    - Implement camera movement and zooming.

## Version 0.2
    - Implement gravity.
    - Implement merging of circles.

## Version 0.3
    - Implement emission of circles.