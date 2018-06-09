IDENTIFICATION OF THE REVENUES VS. DOWNLOADS CHARACTERISTICS OF SEVERAL WEB OBJECTS
-----------------------------------------------------------------------------------

Consider visit https://github.com/balde73/SPE-assignment-1 to read the markdown version of this file and the full repository.




PREREQUISITES
-------------

This project requires `python3` and `python3-pip`. So if they are already installed simply skip this part (pip should be shipped with Python out of box). Otherwise use the command:

```shell
make prepare
```

Or as alternative install the missing one using:

```shell
sudo apt-get install python3
sudo apt-get install python3-pip
```

If you use python v3.x as default python instead of python3 this should be handled. The default pip command will be `pip` instead of `pip3` and `python` instead of `python3`.

If you  feel **really lucky** you could skip this part and simply run the project using one rule of makefile. A subroutine will check the python version installed and will perform `make prepare` and `make install` for you if no `python3` is found.




INSTALLING
----------

Now you need to install the python library using pip

```shell
make install
```

That simply performs `pip3 install -r requirements.txt`




HOW TO RUN
----------

Type `make` or `make help` for a complete list of make rules

```
> make help

\\ will output

make prepare
    prepare development environment, use only once
make install
    install all python requirements, use only once
make start
    start the analysis and print results on console
make start-and-plot
    start the analysis and plot some graphs
make start-and-plot-all
    start the analysis and save all the graphs in a folder
```

`make start-and-plot` and `make start-and-plot-all` will save all the graphs as pdf in a new folder inside `./images` as `./images/Y-m-d_H-M-S`. To display the figures from the prompt comment line2 of `main.py` and remove `plt.close()`

Of course if you don't like makefile it is possible to run the same command using `python3`. Type `python3 main.py --help` for the list of options available.
