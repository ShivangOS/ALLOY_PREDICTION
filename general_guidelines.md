
---

# HEA Dataset Feature Selection Guidelines

## Dataset Overview

The dataset consists of five major categories of columns.

| Category                  | Columns                                                                                                                          | Typical Usage                                                                     |
| ------------------------- | -------------------------------------------------------------------------------------------------------------------------------- | --------------------------------------------------------------------------------- |
| **Identifiers**           | Alloy ID, Alloy, References                                                                                                      | Never use as model features                                                       |
| **Composition**           | Al, Co, Cr, Fe, Ni, Cu, Mn, Ti, V, Nb, Mo, Zr, Hf, Ta, W, C, Mg, Zn, Si, Re, N, Sc, Li, Sn, Be                                   | Primary input features                                                            |
| **Derived Descriptors**   | Num_of_Elem, Density_calc, dHmix, dSmix, dGmix, Tm, n.Para, Atom.Size.Diff, Elect.Diff, VEC                                      | Optional engineered features                                                      |
| **Processing Parameters** | Sythesis_Route, Hot-Cold_Working, Homogenization_Temp, Homogenization_Time, Annealing_Temp, Annealing_Time_(min), Quenching, HPR | Use only if the prediction problem assumes manufacturing information is available |
| **Material Properties**   | Microstructure_, Multiphase, IM_Structure, Microstructure, Phases                                                                | Usually prediction targets; may also act as features in some downstream tasks     |

---

# General Principles

## Always Exclude

These columns should **never** be used as model features.

```text
Alloy ID
Alloy
References
```

Reason:

* identifiers
* no physical meaning
* cause overfitting

---

## Composition Features

These are the fundamental descriptors of an alloy.

```text
Al
Co
Cr
Fe
Ni
Cu
Mn
Ti
V
Nb
Mo
Zr
Hf
Ta
W
C
Mg
Zn
Si
Re
N
Sc
Li
Sn
Be
```

These should be considered the **default input features** for almost every model.

---

## Derived Descriptors

```text
Num_of_Elem
Density_calc
dHmix
dSmix
dGmix
Tm
n.Para
Atom.Size.Diff
Elect.Diff
VEC
```

These are calculated from composition.

They may improve prediction performance but are optional.

Contributors should clearly mention whether their model uses

* composition only
* descriptors only
* composition + descriptors

---

# Target-specific Guidelines

---

## Predicting Hardness

Recommended features

* Composition
* Derived descriptors
* Processing parameters (optional)

Exclude

```text
Hardness
Microstructure_
Multiphase
IM_Structure
Microstructure
Phases
```

Reason

Microstructure and phase are often measured after processing and may introduce information leakage if the goal is to predict hardness directly from alloy composition and processing conditions.

---

## Predicting Phase

Target

```text
Phases
```

Recommended features

* Composition
* Derived descriptors
* Processing parameters

Exclude

```text
Phases
Microstructure
Microstructure_
Multiphase
IM_Structure
```

---

## Predicting Microstructure

Target

```text
Microstructure
```

Recommended features

* Composition
* Derived descriptors
* Processing parameters

Exclude

```text
Microstructure
Microstructure_
Phases
Multiphase
IM_Structure
```

---

## Predicting Multiphase

Target

```text
Multiphase
```

Recommended features

* Composition
* Derived descriptors
* Processing parameters

Exclude

```text
Multiphase
Microstructure
Microstructure_
IM_Structure
Phases
```

---

## Predicting IM Structure

Target

```text
IM_Structure
```

Recommended features

* Composition
* Derived descriptors
* Processing parameters

Exclude

```text
IM_Structure
Microstructure
Microstructure_
Multiphase
Phases
```

---

## Predicting Density

Target

```text
Density_calc
```

Recommended features

* Composition

Exclude

```text
Density_calc
```

Since density is itself a descriptor derived from composition, including it as an input would make the task meaningless.

---

## Predicting Descriptor Values

Targets

```text
VEC
dHmix
dSmix
dGmix
Tm
Atom.Size.Diff
Elect.Diff
```

Recommended features

* Composition only

Exclude

* Target descriptor
* Other derived descriptors if the goal is to predict the descriptor from elemental composition.

---

# Processing Parameters

Processing parameters should only be used if they are known at prediction time.

```text
Sythesis_Route
Hot-Cold_Working
Homogenization_Temp
Homogenization_Time
Annealing_Temp
Annealing_Time_(min)
Quenching
HPR
```

If the prediction problem assumes

```text
Composition

↓

Predict Property
```

then processing parameters should be excluded.

If the prediction problem assumes

```text
Composition
+
Manufacturing Parameters

↓

Predict Property
```

then they may be included.

---

# Information Leakage

A feature should **not** be used if it would only become available after measuring the property being predicted.

Examples

| Target         | Should Exclude                               |
| -------------- | -------------------------------------------- |
| Hardness       | Phase, Microstructure                        |
| Phase          | Microstructure labels                        |
| Microstructure | Phase labels describing the same observation |
| Density        | Density_calc                                 |

---
