
Codebase for the Simulation of the 'Optimizing Resource Management for Bursty Video Analytics' Project.
By: Hai Nguyen, Sam Zhang, and Lucy Newman

The project is a aprt of the course 'Introduction to Serverless and Intermitten Computing' taught by Prof. Andrew Chien.

Scenarios: We has a cluster that continuously provide resources for two workloads:
 - Bursty: Low resource consumption but when an interesting event occurs, their consumption increases exponentially for a short duration and then reduces to low consumption again.
 - Foreground(steady): Constant resource consumption

The resources of the cluser is managed by a resource manager that statically partition the resources into pools with different statistical properties:
 - Burst: Fixed-size resource, has maximum runtime (resource are foreced to be reclaimed if workload uses them for more than maximum runtime) but guarantee ramp (i.e. the minimum acceptance rate of
          resource requests over an interval such as 10 instance/min)
 - On-demand: no restriction on runtime, but no guaranteed ramp.

The simulation has two parts:
 - Find the optimal static resource parition that maximizes the total value of workloads (bursty + foreground)
 - Find the benefit of using burst + on-demand for bursty workload

Please check the 'exp' directory for usage instruction.


