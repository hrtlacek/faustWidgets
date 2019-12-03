# faustWidgets
Creates interactive widgets inside jupyter notebooks from faust dsp files and produces a (customizable) plot.
![example](image.png)

## Install
At the moment this is just a single `.py` file that has to be imported as a module. Just put it in your python search path.
This relies heavily on FAUSTPy. FAUSTPy was originally developed by Marc Joliet [here](https://github.com/marcecj/faust_python).
I ran into problems with this. I think it hasn't been updated in a while and FAUST changed a bit. You can find my fork of FAUSTPy [here](https://github.com/hrtlacek/faust_python). I basically changed very little and got it to run again.
Other than FAUSTPy the following is needed:
- numpy
- matplotlib
- [widgets](https://ipywidgets.readthedocs.io/en/latest/user_install.html)