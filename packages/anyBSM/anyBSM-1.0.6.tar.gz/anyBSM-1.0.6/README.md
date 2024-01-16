# anyBSM / anyH3: $`\kappa_\lambda`$ (and more) in generic BSM models

[![pipeline status](https://gitlab.com/anybsm/anybsm/badges/main/pipeline.svg)](https://gitlab.com/anybsm/anybsm/commits/main) 
[![coverage report](https://gitlab.com/anybsm/anybsm/badges/main/coverage.svg)](https://gitlab.com/anybsm/anybsm/commits/main)


<div align="center">

![alt text](anyBSM/logos/anyH3_logo_large.png "anyH3 logo"){width=40% height=40%}

</div>

## program purpose
The idea of this program is to close tha gap regarding $`\kappa_\lambda`$ predictions in the landscape of BSM tool-boxes:
```mermaid
graph LR
  subgraph bsm [ ]
    direction TB
    BSM((<font size=6>BSM model))
  end

  subgraph TH [<font size=5>Theoretical constraints]
  direction LR
   theo1[<font size=5>Vacuum stability] -->|<font size=4>EVADE/Vevacious++| BSM
   theo2[<font size=5>Unitarity] -->|<font size=4>EVADE/SARAH/SPheno| BSM
   theo3[<font size=5>UV behaviour] -->|<font size=4>RGEpp/ARGES/SARAH/Pyrate| BSM
   theo4[<font size=5>Renormalisability] -->|<font size=4>GroupMath/SARAH/Susyno| BSM
   theod[<font size=5>...] -->|<font size=4>...| BSM
  end

  subgraph EX [<font size=5>Experimental constraints]
  direction LR
   BSM -->|<font size=4>FlexibleSUSY/Hdecay/SPheno + HiggsBounds| ex4[<font size=5>BSM searches]
   BSM -->|<font size=4>FlexibleSUSY/Hdecay/SPheno + HiggsSignals| ex1[<font size=5>SM-like Higgs]
   BSM -->|<font size=4>FlavorKit/Flavio| ex3[<font size=5>Flavour observables]
   BSM -->|<font size=4>FlexibleSUSY/SPheno| ex5[<font size=5>EWPO]
   BSM -->|<font size=4>DarkSUSY/MicrOmegas| ex6[<font size=5>Dark matter]
   BSM -->|<font size=4>BSMPT/PhaseTracer| ex7[<font size=5>Early universe]
   BSM -->|<font size=4>...| exd[<font size=5>...]
   BSM -->|<font size=5>???!| exq[<font size=5>kappa_lambda]
  end

  style exq fill:#f96,stroke:#333,stroke-width:4px;
  style bsm fill:#ffff,stroke:#ffff
```
## Installation
### Using pip (recommended)
```bash
pip install -U anyBSM
```

### from source
```bash
git clone https://gitlab.com/anybsm/anybsm.git
cd anybsm
pip install .
```

## Documentation

An online documentation is available at [anybsm.gitlab.io](https://anybsm.gitlab.io).

[pdoc](https://pdoc.dev) is required to generate the documentation locally:
```
pip3 install pdoc
./docs/make.py
# now open /docs/docs/index.html in your browser
```

## Journal references

Henning Bahl, Johannes Braathen, Martin Gabelmann, Georg Weiglein
<br/>*anyH3: precise predictions for the trilinear Higgs coupling in the Standard Model and beyond*  </br>                      
e-Print: [arXiv:2305.03015](https://arxiv.org/abs/2305.03015)

## program flow

### program structure

<div align="center">

![alt text](anyBSM/logos/program_structure.png "program structure"){width=90% height=90%}

</div>

### class structure 

<div align="center">

![alt text](anyBSM/logos/class_structure.png "class structure"){width=80% height=80%}

</div>
