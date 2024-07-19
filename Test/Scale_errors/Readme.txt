This folder contains tests and data related to CTJ's scale errors for the following elements:
[('black', 0), ('g1', 160), ('g2', 106), ('g3', 209), ('g4', 80), ('g5', 135), ('white', 255)].
Tests were conducted with a 50% probability of introducing an error at each iteration of the algorithm.
If the introduced error causes the value to exceed the CTJ scale, the value is adjusted to the maximum (or minimum) limit of the scale.
Furthermore, the error is randomly chosen to be positive or negative with equal probability.
The algorithms were allowed up to 200 iterations, excluding calibration iterations, with a required minimum accuracy of 0.95.
