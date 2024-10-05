# mathemapy

Python library for Symbolic Computation &amp; Pedagogy

A simple, expandable Python library for symboic math, designed to help developers build educational tools with step-by-step solutions. The library supports multilingual output for descriptive steps, and intend to cover a wide range of topics, making it ideal for creating math related educational apps.

This is created as the base protoype model for the "Mathematishia Computer Algebra System", but feel free to use this package as the way you wanted, licensed under the MIT license.

<!--
#### Code Principles & Guidelines

* Modularity:
  * Each mathematical domain (algebra, calculus, trigonometry etc) should be encapsulated in its own module. This makes the system easy to expand without breaking the existing functionality.
* Extensibility:
  * The core should handle symbolic expressions, basic types & perations, parsing ( if needed ) while individual modules (e.g. algebra) extend this core for more advanced operations.
  * The output system (steps, descriptions) should support multiple languages, which can be expanded manually by adding language modules. All lanuage modules must follow the same order as the "English (en.py)", this will be further address inside the `guide.md` in the languages folder, refer to that before making any changes.
* Pedagogy Focus:
  * Always include descriptive steps for each operation, such as showing simplification steps, solving methods, and if possible some examples ( this will also adress futher in `languages/guide.md`)
* Code Style:
  * Follow PEP8 guidelines for Python code.
  * Use type hints, and ensure functions, classes have clear docstrings explaining inputs, outputs and expected bahaviour.
* Performance:
  * While clarity and pedagogy are priorites, always consider perfomance impact of algorithms as well, since we are working with python here.
  * Use lazy evaluation or caching when dealing with more complex symbolic manipulations.



TODO ::
create more expressions to handle test cases,
add the step support to the basic operations
add language feature


Considerations -> Do we really need BinaryOperator and UnaryOperator ? instead try to get ideas from sympy or mathjs and mathsteps
-->