
# Radicale CS3 API Auth Plugin

This is an Auth plugin for the Radicale CalDAV and CardDAV Server. It allows to use the Radicale server with the same users like ownCloud Infinite Scale or Reva. Users can use Radicale via the Basic Authentication method ("basic auth").

With that, users should be able to start the Radicale Server alongside with Infinite Scale. Users of Infinite Scale have an experimental CalDAV and CardDAV backend with that.

## Build

Change into the radics3 directory (where also `setup.py` is) and call:

```bash
python3 -m pip install .
```

## Usage

1. Install this module as Authentication Plugin for your Radicale server. See [this](https://radicale.org/master.html#authentication-plugins) for more details about plugins.
2. Add the following entries to the Radicale configuration:
```
[auth]
type = radics3
revagateway = localhost:9142
```
In the configuration group `[auth]`, the type is set to the authentication type `radics3`, which enables the plugin. The second line `revagateway` specifies the Reva gateway that is called for authentication via grpc.

3. Start Radicale and check that the auth plugin is really used.
4. Open the Radicale web interface at <radicalehost>:5232 and create address books or calendars.
