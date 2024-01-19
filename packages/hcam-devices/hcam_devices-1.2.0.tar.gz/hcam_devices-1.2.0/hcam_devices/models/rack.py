# model for one thing only - temperature from Rack heat exchanger
from astropy.time import Time
from twisted.logger import Logger

try:
    from ..gtc.corba import TelescopeServer
except Exception:
    TelescopeServer = None


class FakeServer(object):
    def getCabinetTemperature1(self):
        return 20.0

    def getCabinetTemperature3(self):
        return 22.0


class Rack(object):
    # add any extra methods you want exposed here
    extra_rpc_calls = ()
    log = Logger()
    settable_attributes = ()

    def __init__(self, emulate=True):
        print("emulation mode: ", emulate)
        if emulate:
            self._server = FakeServer()
        else:
            self._server = TelescopeServer()

        # no state machine needed
        self.machines = {}

    def telemetry(self):
        """
        Called periodically to provide a telemetry package
        """
        ts = Time.now()
        try:
            temp_top = self._server.getCabinetTemperature1()
            temp_bottom = self._server.getCabinetTemperature3()
        except Exception:
            temp_bottom = None
            temp_top = None

        return dict(
            timestamp=ts,
            rack_temp_bottom=temp_bottom,
            rack_temp_top=temp_top,
            state={},
        )
