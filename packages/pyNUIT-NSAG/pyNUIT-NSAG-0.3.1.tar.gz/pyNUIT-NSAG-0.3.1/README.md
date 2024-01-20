<!--
 * @Author: albertzhang albert.zhangweij@outlook.com
 * @Date: 2023-12-22 11:20:00
 * @Description: 
 * 
 * Copyright (c) 2024 by THU-RSAG, All Rights Reserved. 
-->
# Contents
- [Summary](#summary)
- [Install](#install)
- [Get Started](#get-started)
- [Reference](#reference)

# Summary
pyNUIT is a package in Python which wrappers the source term analysis code NUIT, and integrates various util tools for its control and management.

# Install
1. Using git clone: `git clone https://github.com/thu-inet/NUIT.git`
2. Download the zip and unzip to destination path
3. Now it is available on `Pypi`: `pip install pynuit-NSAG`

Only a few basic Python packages are required, including:
- Numpy
- Matplotlib
- Pandas

# Get Started
The most basic module is nt.Model and nt.Output, for management of pyNUIT input model and its output.
```
# import pyNUIT
import pyNUIT as nt

# define the model
model = nt.Model()
model.add_nuclide("U235", 0.85)
model.add_nuclide("U238", 4.15)

# define power history
for i in range(10):
    model.add_burnup(time=10, unit='day', val=800E-6)

# define the output
model.set_output("isotope", print_all_step=0)

# library configuration
model.set_library(r"D:\\NUIT\\NUITLib_HTGR_900k")

# run the model to get output
out = model("model.xml", nuitpath="D:\\NUIT\\NUITx.exe")

# read calculation results
burnup = out.burnups[-1]
density = out.get_nuclide_mass("Cs137")[-1]
print(f"Nuclide density of Cs137 at {burnup} MWd/kgU is {density} n/cm/barn")
```
Histogram class is used to represent the power history, and can transfer its power history into nt.Model to form a complete model.

```

# define two histogram instances
histo1 = nt.Histogram(["2019-01-15 00:00", "2019-02-26 00:00", "2019-03-26 00:00"], [(0,0), (3.7E6,3.7E6), (3.7E6, 0)])
histo2 = nt.Histogram(["2019-05-28 00:00", "2019-07-02 00:00"], [(0, 0), (3E6, 3E6)])

# concatenate two histograms
histo = histo1 + histo2

# pass the power history to model
histo.model = model
model = histo.to_model(step_length=10*86400)
```

Classes in nt.data are used to interact with data libraries.
```
# read the multi-group xs lib
mgxslib = nt.data.MGXSlib.from_datfile("D:\\NUIT\\NUITLib_HTGR_900k\\NuitMgXsLib.dat")

# use existing flux data to collapse into one-group xslib
xslib = mgxslib.to_xslib(flux)

# check the xs of Cs134, MT=102 reaction
print(f"Cross section of Cs-134 Reaction(102) is {xslib("Cs134")(102)}")

# export xslib into .dat file
xslib.to_datfile("xslib.dat")
```
# Reference
