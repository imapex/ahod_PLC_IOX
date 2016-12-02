# ahod_PLC_IOX
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

________
**IOx**
________

The value of the Internet of Things (IOT) is less about the "things" and
 is more about enabling digital transformation. This can mean enabling new data
 sources to provide greater context, and creating new interactions between
 people and machines.

The value of this data is not in just capturing it, but through the
creation of insights through greater understanding. Moving all this data
to a single location, either an organizations local Data Center or a
public cloud service, is not feasible for all data sources and injects
latency that can make the data too stale for real time applications.

Cisco's IOx framework enables organizations and developers to leverage
processing closer to the end devices inside network edge devices.

For more information on the IOx framework and developing applications
please see Cisco's developer community at
[developer.cisco.com](https://developer.cisco.com/media/iox-dev-guide-7-12-16/intro/conceptual-overview/)

For this application we leveraged the Industrial Switching
[IE-4000](http://www.cisco.com/c/en/us/products/switches/industrial-ethernet-4000-series-switches/index.html)
platform.

**Note to run IOx on the IE-4000 will need to be running an IOS revision
which supports it. At the time of this project 15.2.5(E1) was the first
released version which supports IOx.
_______
**IOx Tools**
_______

The IE-4000 currently only supports running LXC container style applications.

For more information on program types please see
[App Types](https://developer.cisco.com/media/iox-dev-guide-7-12-16/concepts/app-types/).

When developing IOx a user will need to leverage the IOx SDK and
ioxclient for packaging and deploying to the IE-4000.
These can be found at
[IOx Downloads](https://developer.cisco.com/media/iox-dev-guide-7-12-16/getstarted/downloads/)
.

_______
**Open Source Applications and libraries leveraged in this application**
_______
[pycomm](https://github.com/ruscito/pycomm) is a python package with a collection
of modules to communicate to PLCs and we have leveraged in our application to
read tag values from a Rockwell Automation Logix based controller.

[urllib](https://docs.python.org/2/library/urllib.html) is a python
module for http interactions. We are using this to POST the alerts
to the Web Service Application.



