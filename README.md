[![MIT License](https://img.shields.io/badge/Code-MIT-blue.svg)](LICENSE)
[![CC-BY 4.0](https://img.shields.io/badge/Data-CC--BY_4.0-lightgrey.svg)](LICENSE-data)
![Last Updated](https://img.shields.io/badge/updated-2026--08--28-success)

# philosophy-papers

Public mirror for the philosophy-of-science line of work by Dmitry Zharnikov (ORCID [0009-0000-6893-9231](https://orcid.org/0009-0000-6893-9231)).

This line asks when a claim about **where a system ends** has empirical content, and what a domain must supply for such a claim to be testable at all. It parallel-tracks but is distinct from the other programmes in this corpus: where SBT theorises perception-rendering at the brand level, OST theorises specification-rendering at the organizational level, and the meaningfulness programme theorises substrate-and-rendering at the knowledge-artifact level, this line is concerned with the epistemology of boundaries and measurement as such — including, where it helps, using organizations as instruments rather than as subjects.

## 1 | Papers

### [boundary-adjudication/](boundary-adjudication/) — 2026bo

**When a Boundary Claim Becomes Testable: A Criterion for Adjudicating Scale-Relative Claims, with One Coded Case**

- Concept DOI: [10.5281/zenodo.22148374](https://doi.org/10.5281/zenodo.22148374) (always resolves to the latest version)
- v1.0.0 DOI: [10.5281/zenodo.22148375](https://doi.org/10.5281/zenodo.22148375)
- Data of record: [10.57967/hf/10145](https://doi.org/10.57967/hf/10145)
- Licence: CC BY 4.0 (paper and data) + MIT (code)

Claims that a self-maintaining or cognitive system extends to some scale are chronically underdetermined, because in the cases usually discussed the investigator draws the boundary and can redraw it around whatever is interesting. The paper specifies three conditions under which that is not so — a perimeter fixed by a party indifferent to the hypothesis under test, observable to someone who did not draw it, and moving only by dated recorded events — and shows that within such a domain the measurable quantity inverts: not whether a boundary is drawn correctly, but what a hypothesis-independent perimeter fails to contain. One acquisition, coded from two document sets that share no document, is the existence proof.

## 2 | Getting Started

```bash
git clone https://github.com/spectralbranding/philosophy-papers.git
cd philosophy-papers
```

Python dependencies are managed via [`uv`](https://docs.astral.sh/uv/). The project anchor is `pyproject.toml` at the repository root; resolve all paths relative to the anchor.

## 3 | Reproducing

`./reproduce.sh` runs every paper's own `reproduce.sh` in turn. To reproduce a single paper, run the one in its directory:

```bash
cd boundary-adjudication && ./reproduce.sh
```

Each paper's script fetches its data of record and then runs the analysis. **The fetch and the analysis are deliberately separate steps**, so that the analysis scripts themselves perform no network access and can be audited as offline and deterministic.

## 4 | Project Layout

```
.
├── <paper-slug>/           # One directory per paper
│   ├── paper.md            # The paper
│   ├── SPINE.yaml          # Propositions, evidence, dependency graph
│   ├── ONTOLOGY.yaml       # Terms this paper owns, imports, refines
│   ├── paper.yaml          # Machine-readable projection of the spine
│   ├── DATA_MANIFEST.yaml  # Where each data artifact lives, and why
│   ├── code/               # Analysis scripts
│   └── reproduce.sh        # Fetch data, then run the analysis
├── output/{figures,tables,logs}/
├── reproduce.sh            # Runs every paper's reproduce.sh
└── pyproject.toml
```

## 5 | Data Availability

Data follows one rule: **one canonical home per artifact, chosen by type rather than by size.**

- **Script-regenerable outputs** are not stored anywhere. The seeded, deterministic script is committed and regenerates them on demand. A stored second copy is how a table and its data come apart.
- **Primary data of record** — measurements and archival snapshots that cannot be regenerated — lives in a citable Hugging Face dataset with a DOI, named in that paper's `DATA_MANIFEST.yaml`, and is never vendored into this repository.
- **Hand-authored inputs** — specifications, prompt templates, ontology modules — are kept here in git alongside the code.

## 6 | Licence

Code is MIT ([LICENSE](LICENSE)). Papers and data are CC BY 4.0 ([LICENSE-data](LICENSE-data)).

## 7 | Citation

See [CITATION.cff](CITATION.cff), or the per-paper `CITATION.cff` in each directory. Cite the concept DOI unless a specific version is meant.
