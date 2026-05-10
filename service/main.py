from jnius import autoclass
import time

def run_vpn():
    VpnService = autoclass('android.net.VpnService')
    PythonService = autoclass('org.kivy.android.PythonService')
    service = PythonService.mService
    builder = VpnService().Builder()
    builder.setSession("SwillWayVPN")
    builder.addAddress("10.0.0.2", 32)
    builder.addRoute("0.0.0.0", 0)
    try:
        interface = builder.establish()
        while True:
            time.sleep(1)
    except:
        pass

if __name__ == '__main__':
    run_vpn()

