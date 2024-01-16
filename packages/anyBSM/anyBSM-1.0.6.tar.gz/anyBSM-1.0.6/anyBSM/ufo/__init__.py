__doc__ = """
# (Modified) UFO objects.

This is the standard UFO library. However, a few improvements have
been performed:

 * The `global all_<ufo object>` variables are dictionaries instead of lists
   This has no effect on the models initialization (particles.py etc)
   but only on how the objects are stored internally (e.g. the particle
   with name `h1` is directly accessible via `all_particles['h1']`).
 * New method `UFOBaseClass.dump()`: returns string representation to
 be interpreted by python
 * UFOBaseClass now warns if duplicate objects (same .name) are initialized
 * `nvalue` attributes have been introduced for Parameter() objects.
 They contain the numerical value obtained with the current set of
 `values` of all  external parameters.
 * `nmass` similar to `nvalue` but for Particle() objects.
 * `Particle.anti()` has been changed to avoid the duplicate creation
 of Particle() objects but rather returns the corresponding anti
 particle from `all_particles`.
 * `function_library` was completely rewritten to avoid `__exec__`ing strings of functions.
 This yields a significat performance boost for large models of up to 3 orders of magnitued in runtime.

Everything else is identical to the original UFO standard.
"""
