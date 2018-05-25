# CPU Sensing Project

*The scripts to run the experiments are written in python 2*

*The scripts to run the models and data cleaning are written in python 3*

*The data parsing script has to be run inside the data_cleaning directory*

I have included all of the features I want into a single csv.
All of the data for a single experiment group is placed into a single csv
so I will have 2 files (experiment 1, experiment 2).

Now for the models that we want to create:

### [1] Binary Classifier
We want to know if there has been any change to the state of the device.
Has a new app started to run?

### [2] App Classifier
Can we tell you what new app has started to run?
For this we can use the same type of data as **[1]**.

**Furthermore:**
Assumption: We KNOW that an app has started to run.
Is our classifier better than before?

### [3] Device State Classifier
Can we tell you what apps are running without any prior knowledge?
We look at current CPU usage and try to classify

**Furthermore:**
Assumption: We have just opened an app and know what app we opened.
With this additional information, can we better classify what the
device state is?
