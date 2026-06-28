# Design Notes and Lessons Learned While Designing the Genetic Algorithm Framework

## 1. Follow the Single Responsibility Principle (SRP)

Every function should perform exactly one conceptual task.

Avoid methods that both compute a value and decide whether or not to modify internal state.

Instead of writing

```python
evaluate(change_state=True)
```

split the responsibilities into

```python
evaluate()
```

* Computes and returns a value.

and

```python
update()
```

* Updates the object's internal state.

This makes the interface simpler, avoids boolean flags, and makes each function easier to understand and reuse.

---

## 2. Separate Algorithms from State Mutation

Whenever possible, separate

* "How something is computed"

from

* "Whether the object's internal state should change."

Example:

Instead of embedding the genetic algorithm directly inside methods that modify `self.population`, extract the algorithm into a reusable helper.

```
_generate_next_population(population)
```

Then provide wrappers around it.

```
next_generation()
```

* Mutates the optimizer.

```
predict_nth_generation()
```

* Simulates evolution without modifying the optimizer.

This avoids code duplication and makes the core algorithm reusable.

---

## 3. Separate Query Operations from Mutating Operations

The public API should clearly distinguish between

Query methods

* Return information
* Do not modify internal state

Examples

```
predict_nth_generation()
evaluate()
```

Mutating methods

* Permanently change object state

Examples

```
next_generation()
advance_n_generations()
update_fitness()
```

Users should immediately know whether calling a function changes the object.

---

## 4. Keep Responsibilities at the Correct Abstraction Level

Each class should only know what it is responsible for.

Chromosome

Responsible for

* storing genetic information
* computing its own fitness

Should not know

* populations
* selection
* crossover
* mutation

---

Population

Responsible for

* storing chromosomes
* behaving like a collection

Should not know

* predictors
* objectives
* optimization algorithms

---

Genetic Algorithm

Responsible for

* evaluating populations
* selecting parents
* generating offspring
* evolving populations

Should not know dataset loading or machine learning details.

---

Base Optimizer

Responsible only for defining the interface common to optimization algorithms.

---

## 5. Reduce Coupling Between Components

Every component should receive only the information it actually needs.

Bad design

Selector receives the fitness function and computes fitness itself.

```
selector(population, fitness_function)
```

The selector now needs to understand evaluation.

Better design

```
selector(population, fitness_scores)
```

Now the selector simply performs selection.

It has no knowledge of

* predictors
* objective functions
* property evaluation

This greatly reduces coupling.

---

## 6. Pass Data Instead of Behavior Whenever Possible

Rather than giving another component a function that it must call correctly,

prefer giving it the already computed information.

Example

Instead of

```
selector(population, evaluate_fitness)
```

use

```
selector(population, fitness_scores)
```

This separates responsibilities and makes each component simpler.

---

## 7. Avoid Temporary Mutation Followed by Restoration

An object should generally not modify itself only to restore its previous state later.

Example

Bad pattern

```
copy current state

modify self

read result

restore self
```

This becomes error-prone as more internal state variables are introduced.

Better pattern

Create a local copy and perform all computation on the copy.

```
population_copy

↓

simulate

↓

return simulated population
```

The original object remains untouched.

---

## 8. Design Public APIs Around User Expectations

Method names should communicate whether they mutate state.

Examples

```
next_generation()
```

Clearly advances the optimizer.

```
advance_n_generations()
```

Clearly modifies the optimizer.

```
predict_nth_generation()
```

Clearly performs a simulation.

Avoid names whose behavior is ambiguous.

---

## 9. Build Reusable Internal Algorithms

Whenever multiple public methods perform almost identical work,

extract the common algorithm into a private helper.

Example

```
_generate_next_population()
```

can be reused by

* next_generation()
* advance_n_generations()
* predict_nth_generation()

Only one implementation of the genetic algorithm now exists.

Future improvements only need to be made in one place.

---

## 10. Keep Objects Consistent

Public methods that mutate an object should leave the object in a valid state.

If an optimizer says it advanced five generations,

its internal population should actually represent generation five.

Simulation methods should never accidentally leave behind modified internal state.

---

## 11. Avoid Duplicate Sources of Truth

If a value is stored inside an object,

avoid maintaining another independent version elsewhere.

Example

If every chromosome stores

```
chromosome.fitness
```

then population evaluation should update this value instead of computing unrelated temporary fitness values.

Multiple independent copies eventually become inconsistent.

---

## 12. Design for Future Extension

Whenever introducing a new optimizer,

the existing architecture should require minimal modification.

New optimizers should simply inherit from

```
BaseOptimizer
```

and implement

```
optimize()
```

without changing existing code.

Similarly,

new selectors,

mutation operators,

crossover operators,

or objective functions

should plug into the framework without requiring modifications to the genetic algorithm implementation.

---

## 13. Prefer Composition Over Hardcoding

The Genetic Algorithm should not hardcode

* selection strategy
* crossover strategy
* mutation strategy
* predictor
* objective

Instead, receive them as constructor dependencies.

This allows users to easily swap algorithms without changing the optimizer itself.

---

## 14. Write Comments That Explain "Why"

Comments should explain

Why a design decision exists

rather than

What the code is doing.

Good

```
Selectors receive precomputed fitness scores to remain independent of evaluation logic.
```

Less useful

```
Loop over all chromosomes.
```

The code already explains *what* it is doing.

Comments should capture design reasoning instead.

---

## 15. A Good Architecture Feels Layered

The final design naturally forms layers.

```
BaseOptimizer
        │
        ▼
GeneticAlgorithm
        │
        ▼
Population
        │
        ▼
Chromosome
```

Each layer depends only on the layer below it.

Responsibilities remain clearly separated, making the project easier to extend, maintain, and test.

---

## Overall Design Philosophy

The primary goal of the architecture is **separation of concerns**.

Every class should have one well-defined responsibility.

Every method should perform one conceptual task.

Components should communicate through simple data rather than knowing each other's internal implementation.

Algorithms should be reusable independently of object state.

If a future feature can be added by creating a new class instead of modifying existing ones, the design is likely following good object-oriented principles.
