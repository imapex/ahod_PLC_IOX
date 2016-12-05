# All Hands on Deck! - AHOD IOx
AHOD - All Hands on Deck!, is demonstration of running an application
via Cisco's IOx framework to notify appropriate users of issues occuring
on the plant floor.

The full information related to this demo can be found at
[ahod_home](https://github.com/imapex/ahod_home)

ahod_PLC_IOX is the component of the AHOD implementation, that is a
python application which utilizes Cisco's IOx framework within Cisco's
Industrial routers and switches, leveraging open source libraries to
communicate with a Rockwell Automation Logix based controller and
restful API calls to send information to the
[Web Service Application](https://github.com/imapex/ahod_webapp).

### Table of Contents
* [Background](#Background)
* [Getting Started](#Getting-Started)
* [Downloading from GitHub](#Downloading)
* [Explanation of files in repo](#ExplanationFiles)
* [Modify Configuration for your demo / Prepare for your install](#ModifyPython)
* [Building the IOx LXC Package](#Building-the-IOx-LXC-package)
* [Deploying to the IE 4000](#Deploying-to-the-IE-4000)
* [Verification and Troubleshooting](#Verification-and-Troubleshooting)

# <a name="Background"></a>Background

## IOx


The value of the Internet of Things (IOT) is less about the "things" and
 is more about enabling digital transformation. This can mean enabling new data
 sources to provide greater context, and creating new interactions between
 people and machines.

The value of this data is not in just capturing it, but through the
creation of insights through greater understanding. Moving all this data
to a single location, either an organizations local Data Center or a
public cloud service, is not feasible for all data sources and injects
latency that can make the data too stale for real time applications. Also
sending large amounts of updates that is unused or unnecessary impacts
available resources.

Cisco's IOx framework enables organizations and developers to leverage
processing closer to the end devices inside network edge devices, thus giving
the ability to act quickly on the data, transform the data into insights,
and only send necessary updates to northbound systems, saving resources.

For more information on the IOx framework and developing applications
please see Cisco's developer community at
[developer.cisco.com](https://developer.cisco.com/media/iox-dev-guide-7-12-16/intro/conceptual-overview/)

For this application we leveraged the Industrial Switching
[IE-4000](http://www.cisco.com/c/en/us/products/switches/industrial-ethernet-4000-series-switches/index.html)
platform.

**Note to run IOx on the IE-4000 will need to be running an IOS revision
which supports it. At the time of this project 15.2.5(E1) was the first
released version which supports IOx.

## Application Concept

In this application we are monitoring the status of a value inside a PLC and alerting
all the appropriate resources if there is an error. While in this simple app we are just
looking for a value of true or 1, the ability to do complex calculations and compare against
previous values would be achievable. This is to demonstrate the power of running applications
closer to the end devices, and the flexibility of the IOx framework to deploy at scale.

## IOx Tools

The IE-4000 currently only supports running LXC container style applications.

For more information on program types please see
[App Types](https://developer.cisco.com/media/iox-dev-guide-7-12-16/concepts/app-types/).

When developing IOx a user will need to leverage the IOx SDK and
ioxclient for packaging and deploying to the IE-4000.
These can be found at
[IOx Downloads](https://developer.cisco.com/media/iox-dev-guide-7-12-16/getstarted/downloads/)
.

We are only leveraging ioxclient to deploy to a single switch for this demo, but integrating
Fog Director to manage a full scale deployment accross the entire infrastructure
would be the next step.

Version 1.2 of the framework enabled support for the IE-4000 switches.

## Open Source Applications and Libraries
[pycomm](https://github.com/ruscito/pycomm) is a python package with a collection
of modules to communicate to PLCs and we have leveraged in our application to
read tag values from a Rockwell Automation Logix based controller.

[urllib](https://docs.python.org/2/library/urllib.html) is a python
module for http interactions. We are using this to POST the alerts
to the Web Service Application.

# <a name="Getting-Started"></a>Getting Started

The steps to prepare the environemt will be

1. Install the SDK
2. source SOURCEME to prepare shell environment
3. Install a Linux Distribution Support Package - LDSP
4. Install a Platform Support Package - PSP

### Install SDK

*NOTE - While ioxclient can run on Linux, Windows and MacOS, at the time of this writing
the IOx SDK will only run on Ubuntu 14.04.1 and 14.04.3. If you are running
an older or newer version the SDK will not function.

For detailed information on installing the SDK please visit the
[SDK Installation Guide](https://developer.cisco.com/media/iox-dev-guide-6-23-16/sdk/sdk-installation/)

The SDK is a .bin so will run with ./filename.bin and the installation location.
Please note this location as it will be leveraged for our application build
and many steps in the process. For the rest of this time we will use
 `/opt/ioxsdk`.

If you install somewhere else, please modify commands accordingly.

### Preparing Shell Environment

After the SDK has been installed, there will be a SOURCEME file located in
the installation location. Source this file to prepare the shell.

`.  /opt/ioxsdk/SOURCEME`

*if you already in the folder you don't need to give the path `. SOURCEME`

### Installing LDSP

Once the SDK has been installed, you will need to install a Linux Distribution
to run on the switch. At this time the only option is yocto 1.7.
`iox ldsp install yocto-1.7`

To verify `iox ldsp show all` will give an output showing it's installed.

### Installing PSP

We will also need to install a platform support package to develop for a
specific platform. In this example we are using the IE 4000 platform
but if wanted to run this on another platform a different PSP woudl need to be
installed.

`iox psp install ie4k`

To verify `iox psp show all` should show the ie4k with yocto-1.7 in the status.

# <a name="Downloading"></a>Downloading from GitHub

For this application we are leveraging the **make** system to prep the
Yocto Linux environment that will run on the IE-4000,
including downloading and installing dependent packages ( pycomm and urllib )
and package into package to be deployed to the switch.

**make** leverages a **Makefile** to do these actions.

When you download the contents of this repository we need to place them in the appropriate location
in the Ubuntu file system. There are shared dependencies that the Makefile will leverage when
building the package.

Easiest method is to do the git call from inside the demo-apps folder.

`cd /opt/ioxsdk/demo-apps`

`git clone https://imapex/ahod_PLC_IOX.git`

This will create a folder `ahod_PLC_IOX` with all the necessary files in the correct location.
# <a name="ExplanationFiles"></a>Explanation of Files

Directly inside `ahod_PLC_IOX` there will be 3 files and the `src` directory.
Inside `src` there will be 5 files.

###### ahod_PLC_IOX
1. LICENSE ( MIT License of this application )
2. Readme.md ( This File )
3. Makefile

###### ahod_PLC_IOX/src
5. AHODCLX.py
6. AHODCLX.conf
6. AHODBASH.sh
7. app-lxc.yaml
8. iox-project-lxc.conf

The Makefile is what tells the **make** process how create and build the package. Including:

* Identify the type of package to be built - ie4k in this case.
* download the zipped source files for pycomm and urllib and unzip
* install them into the linux kernel
* move `src/AHODCLX.py` and `src/AHODCLX.conf` into the `/usr/bin` inside the image
* move `src/AHODBASH.sh` to `/etc/init.d` so that is can autostart on boot
and call on the python program.
* create appropriate symbolic links to `/etc/r_.d` (where _ is 0 - halt,1 - start and 5 - restart)

`AHODCLX.py` as stated is the python application that will call on pycomm to read from the PLC and alert if the
tag goes to 1 ( True ).

`AHODCLX.conf` is the file for setting parameters of how the program will run. If file is not found the code will run with my defaults.

`AHODBASH.sh` is the bash script to start, stop and restart AHODCLX.py ( Silent at terminal )

`app-lxc.yaml` is a definition of the resources for the LXC container that's created and installed on the switch.

`iox-project-lxc.conf` is what tells the package how to be built for the various platforms.

More information on the structure can be found at
[Native Application Anatomy](https://developer.cisco.com/media/iox-dev-guide-6-23-16/native/native-application-anatomy/)

# <a name="ModifyPython"></a>Modify Configuration File/ Prepare for your install

Currently the information for the application is read in through the `AHODCLX.conf` file.

This will require editing for your specific installation.

The most important variables are `plcip`, `tag1`, and `weburl`.

plcip tells the system the ip of the PLC to read from

tag1 is the tag name to read.

*Note the tag construct is a memory pointer in the Logix family of PLCs. This is how data points are referenced.

weburl is the address of your Web Service Application.

If the `AHODCLX.conf` file is not found, the python code will fallback
 to my defaults. If you wish to change the defaults you could edit the python code itself.


# <a name="Building-the-IOx-LXC-package"></a>Building the IOx LXC package
Once the application has been customized for our installation, we are ready to build.

`cd /opt/ioxsdk/demo-apps/ahod_PLC_IOX`

`make`

This will take time. There are a lot of components to build ( it's building a full Yocto kernel "from scratch" )

*NOTE this will require your Ubuntu server to have internet access.

The last few outputs should be "Creating the application package".

 The last line will be **Done**





# <a name="Deploying-to-the-IE-4000"></a>Deploying to the IE 4000

### Preparing the switch
On the switch, you will need to prepare the IOx environment. Note that
not every IOS image supports IOx. You will want to download and install
the IOS package that is IOS + IOx. At time of this writing the only released
version with IOx support is 15.2.5(E1).

The tar is labeled IOX COMPUTE PLATFORM
FIRMWARE WITH IOS BUNDLE.

Please leverage the `archive download-sw` method of updating the IOS on the switch.
Please see your IOS revisions release notes for more details on installation.

Once running an appropriate version of IOS you can configure IOx via CLI or Device Manager ( Web GUI ).

##### CLI

`switch(config)#    iox`

then will need to setup the ip address of the instance and a default-gateway

###### DHCP
**host ip address dhcp vlan z** where z is the vlan to place IOx image in


ie: `switch(config-iox)#    host ip address dhcp vlan 1` to leverage dhcp and put IOX image on a specific vlan
###### Static
 **host ip address ip_address subnet_mask vlan z** where ip_address is in format x.x.x.x subnet_mask is in form y.y.y.y and z is the vlan


 ie: `switch(config-iox)#    host ip address 192.168.1.30 255.255.255.0 vlan 1`

###### Default Gateway

 Last will need to tell IOx the default gateway with **host ip default-gateway ip_address**  where ip_address is in x.x.x.x format


ie: `switch(config-iox)#    host ip default gateway 192.168.1.1`


##### Device Manager

 1. Select IOx
 2. Select IOx Network Settings
 3. Select radio button for Static of DHCP
 4. Input IP Address, Default Gateway and Vlan ID


### Installing, Activating and Starting the application

Once the switch has been configured, and the package has been created, the last step is to deploy.

##### ioxclient profiles

First we need to configure a profile for ioxclient to talk to the iox instance on the IE-4000.
`ioxclient profiles create` will start a guided profile creation.

Your IOx platform's IP address is IP configured under IOX in IE switch setup.

Your IOx platform's port number is 8443

Authorized user is username configured on switch for access ( Level 15 ).

Password for user will be the usernames given in last steps password.

Leave Local Repository and URL scheme and API prefix set to defaults.

Set ssh port to 22.


To verify profile was created and activated run the command `ioxclient profiles list`.


##### ioxclient application

We are now ready to install the application on the IE-4000.
The application tar will be in the `out` folder that was created by **make**.

`cd /opt/ioxsdk/demo-apps/ahod_PLC_IOX/out`

`ioxclient application install AHOD ahod_PLC_IOX_ie4k-lxc.tar`

*Note using application name of AHOD in install command. This can be whatever you want but will use AHOD in further examples.

Once the install is complete `ioxclient application list` should show the application as installed.

We will then need to activate the application with `ioxclient application activate AHOD`

Once activated `ioxclient application list` should show the application activated.

Last we need to start the application

`ioxclient application start AHOD`

Once again `ioxclient application list` can be used to verify it worked and should show it as started.



# <a name="Verification-and-Troubleshooting"></a>Verification and Troubleshooting

To verify the application has been installed, you can access the linux image running on the IE-4000 with the command

`ioxclient application console AHOD`

The username if prompted will be ` root`.

Since the python script is running silent you won't see it at the terminal.


`ps` will show running processes and you should see /usr/bin/AHODCLX.py running ( or a python process ).
There will also be an AHODLOG.txt located in the root directory ( `cd /` )



