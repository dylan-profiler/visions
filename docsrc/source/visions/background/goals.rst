Goals
=====

Axioms when designing ``visions``:

- **Performant:** Efficiency as an enabler to more important things (reliability, dependability)
- **Reduce complexity:** Simplify expressing data types, saving time. This includes sensible default types and typesets.
- **Extendable:** New types are composable from other elements, extension should be simple.
- **Solid foundation:** We heavily rely on existing frameworks (Pandas, Numpy). Inconsistencies are fixed within the framework design and preferably resolved in the framework itself.

For both the package developers and our users, goal (1) and (2) are intertwined:

    My main tool for efficiency and performance actually is abstraction

    -- Barjne Stroustrup
