# signal-application-python-sdk

# Setup

### Add Signal-Application-SDK as a dependency to requirements.txt
```
signal-application-python-sdk==<latest>
```

### Install dependencies
```
python setup.py install
```

Entry point for Signal Application SDK
* Creates a bi-directional communication between device shadow and application

### Initialize SDK
```
self.app = SignalApp()
self.app.initialize(self.onConfigChange, self.onEvent)
```

### Provide a callback method to get notified when a configuration change is requested
```
def onConfigChange(self, config):
```
* Will be triggered when a new configuration change requested from the cloud


### Provide a callback method to get notified when an event is received from event bus
```
def onEvent(self, event):
```
* Will be triggered when a new event received from application's subscribed topic


### Call next to forward the event to the next node (application), if next_app_id(optional) is specified, it forwards the event to the specified application
```
self.app.next(event: object, next_app_id)
```

### Call next to forward the event to the next node running on node-red.
```
self.app.nextNode(event: object)
```


### Call reportConfigurationChange to report when configuration change is applied
```
self.app.reportConfigurationChange(config: object)
```


### Sample usage
Consider adding these two params to the application detail
![Settings](settings_list.png)
![Settings](settings.png)

config object will be reveived as below

```
{
    message: 'some text message',
    param2: 101
}
```

 