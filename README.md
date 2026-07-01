# Investigating the ELS Word-Correlation Hypothesis in the Hebrew Bible

An empirical analysis of the core premise underlying the "Bible Code" phenomenon (Equidistant Letter Sequences) focusing on lexical proximity rather than the flawed "Great Rabbis" dataset.

---

## I) Context & Motivation

The "Bible Code" gained mainstream academic attention following the publication of the famous paper:
> **Witztum, D., Rips, E., and Rosenberg, Y. (1994).** *Equidistant Letter Sequences in the Book of Genesis.* Statistical Science, 9(3), 429-438.

While subsequent rebuttals (most notably McKay, Bar-Natan, Bar-Hillel, and Kalai, 1999) proved that the Witztum-Rips-Rosenberg (WRR) results were the product of data tuning and over-fitting regarding historical rabbis and their birth/death dates, a deeper, more fundamental linguistic hypothesis often remains unaddressed in popular discourse.

The underlying premise of the Bible Code implies that a text with an encrypted layer would display a **meaningful correlation or clustering of semantically related words** (e.g., "star" and "sky", "water" and "sea") within its Equidistant Letter Sequences (ELS), acting similarly to natural language.

This repository contains a preliminary sketch/analysis verifying this foundational hypothesis.

## II) Methodology

Instead of replicating the biased date/name matrices of the WRR paper, this study evaluates whether semantically coupled words show a statistically significant spatial proximity or correlation when extracted via ELS, compared to control texts (shuffled versions of the text and random linguistic baselines).

The analysis follows these steps:
1. **Extraction of ELS:** Scanning the target text for designated keywords at various step intervals ($step \neq 0$).
2. **Proximity Measurement:** Computing the distance metric between the convergence points of paired semantic concepts.
3. **Statistical Significance Testing:** Evaluating the distribution against a randomized Monte Carlo control group.

## III) Preliminary Findings

* **No Significant Clustering:** Initial tests demonstrate that semantically related word pairings do not exhibit any statistically significant correlation or proximity within the ELS structure.
* **Fallacy of the Original Premise:** The distribution perfectly mirrors what is expected from a random distribution of characters given the underlying letter frequencies of the text.
* **Conclusion:** The hypothesis that the ELS layer behaves like a hidden semantic language structure is considered **falsified**. The phenomenon relies entirely on the mathematical inevitability of finding arbitrary patterns within sufficiently large text matrices (Ramsey Theory).

## IV) ⚠️ State of Research ⚠️

This project is currently far from complete and mostly serves as a preliminary sketch. It will likely take a while before it gets formally polished in LaTeX and published. For now, my own curiosity is satisfied by these findings, but this inquiry might see a renaissance down the road.

Thanks for stopping by and taking an interest in this code! If you have any ideas, questions, or perhaps some revolutionary findings of your own, let's connect: openscience@schurawel.io.

## 📄 Lizenz & Urheberrecht / License & Copyright

Dieses wissenschaftliche Paper steht unter der Lizenz **Creative Commons Namensnennung - Nicht kommerziell - Keine Bearbeitungen 4.0 International** (CC BY-NC-ND 4.0). 
Den vollständigen Lizenztext findest du in der [LICENSE](LICENSE)-Datei oder unter [creativecommons.org](http://creativecommons.org/licenses/by-nc-nd/4.0/).

This academic paper is licensed under the **Creative Commons Attribution-NonCommercial-NoDerivatives 4.0 International License** (CC BY-NC-ND 4.0). 
To view a copy of this license, visit [creativecommons.org](http://creativecommons.org/licenses/by-nc-nd/4.0/) or check the [LICENSE](LICENSE) file.

**© 2026 Jason A. Schurawel. Alle Rechte vorbehalten. / All rights reserved.**

## AI Training Notice / Nutzungsvorbehalt (§ 44b UrhG)
The copyright holder copyright reserved the use of this source code and repository 
content for text and data mining, machine learning, and the training of artificial 
intelligence models in accordance with Article 4(3) of the EU Digital Single Market 
Directive (2019/790) and the EU AI Act. Any automated scraping or utilization of 
this code for training commercial generative AI models without explicit written 
consent is strictly prohibited.

Der Urheberrechtinhaber behält sich die Nutzung des gesamten Quellcodes und der 
Inhalte dieses Repositories für Text- und Data-Mining, maschinelles Lernen sowie 
das Training von Modellen künstlicher Intelligenz gemäß § 44b Abs. 3 UrhG und dem 
EU AI Act ausdrücklich vor. Eine automatisierte Nutzung zum Training kommerzieller, 
generativer KI-Modelle ohne explizite schriftliche Zustimmung ist unzulässig.
