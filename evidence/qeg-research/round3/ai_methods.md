# What AI-assisted breakthroughs actually teach this project

Three documented examples show how AI can improve difficult research problems when proposals face an independent, executable correctness criterion. Their achievements concern specified mathematical objects and algorithms. They provide useful methods for our project, but no evidence that generating persuasive explanations solves quantum gravity. The transfer recommendations below are this project's methodological synthesis. Sources and repository contents were checked on 9 September 2026; none of these research engines was executed in this run.

## FunSearch: discover a construction, then inspect its structure

FunSearch produced a cap set containing 512 vectors in eight dimensions over the three-element field, improving the previous construction of size 496. This established a better lower bound; it did not establish the optimal size or solve the unrestricted cap-set problem. A frozen language model proposed priority functions inside a supplied construction procedure. Executable evaluation rejected invalid outputs and scored valid sets; evolutionary selection retained useful programs. Inspecting the resulting program helped the authors derive an explicit structured construction. Only four of 140 reported experiments reached 512, illustrating why failed searches and total search budget matter. [@A01]

Its public repository includes the evolutionary pipeline and examples, while omitting the language models, execution sandbox, and distributed infrastructure. It supplies reusable components rather than a complete reproduction environment. [@A02]

## AlphaTensor: exact residuals separate discovery from proof

AlphaTensor found a 47-multiplication algorithm for multiplying two 4-by-4 matrices over the field with two elements, improving the 49-multiplication Strassen-square construction in that arithmetic. TensorGame subtracts proposed rank-one tensors from the fixed multiplication tensor. Reaching the exact zero residual supplies a correctness certificate; reinforcement learning and tree search guide the difficult search. This certificate does not prove minimum rank. Restricting permissible factor coefficients can exclude better algorithms, a limitation the authors explicitly identify. The finite-field result also cannot be relabelled a 47-multiplication real-arithmetic algorithm. [@A03]

The public repository supplies factorizations, loading and verification notebooks, recombination code, and hardware benchmarking material. These are valuable independent-check artifacts; their presence should not be described as release of the entire training system. [@A04]

## AlphaEvolve: improve the search algorithm under staged evaluation

The 2025 report describes evolving code that searches for tensor decompositions, including optimizer, initialization, and loss changes. Candidate programs encounter increasingly demanding evaluations and multiple random seeds. It reports a 48-scalar-multiplication construction for two 4-by-4 complex matrices, improving 49 in that setting. The complex field distinguishes this result from AlphaTensor's finite-field result. Discretized factors permit exact reconstruction checks; a small floating-point fitting loss alone would not certify an algorithm. [@A05]

The official results repository contains correctness-checking code, expressly excludes the AlphaEvolve engine, and includes only instances outperforming earlier constructions. That selection limits assessment of overall success from the notebook alone. A May 2026 official update reports broader applications; it is a developer report, not independent validation of our electromagnetic–gravitational model. [@A06; @A07]

## Transfer to the next physics iteration

1. Freeze an advisor-reviewed contract: action, units, quantum state, renormalization conditions, sources, boundary conditions, and approximation domain. Candidate agents may improve numerical methods; changing this contract creates a separately labelled hypothesis.
2. Use inexpensive coding agents to propose reductions, asymptotic expansions, quadrature, and integrators. Keep the evaluator independently maintained and inaccessible to candidate edits.
3. Reject dimensional inconsistencies, broken identities, wrong analytic limits, and charge or energy accounting failures before costly evolution. Then require independent implementations, grid and cutoff convergence, and regulator checks appropriate to the claimed observable.
4. Reserve untouched parameter cases and adversarial limits. Optimize speed only after correctness gates. Preserve all failures, seeds, budgets, and discrepancies; use disagreements to reopen assumptions rather than average incompatible answers.
5. Separate evidence levels: an exact identity verifies mathematics; numerical convergence supports a declared continuum model; experimental discrimination tests its physical relevance. No level automatically establishes the next.

A flawed evaluator can efficiently select a wrong closure. The useful lesson is therefore to strengthen falsification alongside search. Our executed counterexamples and solver checks are local validation artifacts, not a claimed reproduction of these AI discovery systems.
