import sys
sys.path.append('/home/kumokay/github/mininet-wifi')
from mininet.node import RemoteController, Node, Docker
from mininet.log import setLogLevel, info
from mininet_wifi.wifi.node import OVSKernelAP, Station, DockerStation
from mininet_wifi.wifi.cli import CLI_wifi
from mininet_wifi.wifi.net import Mininet_wifi


def topology(mode='containernet', is_enable_cli=False):
    """
    create a network.

    mode (str): miminet or containernet
    is_enable_cli (bool): running CLI
    """
    c1 = RemoteController('c1', ip='172.17.20.12', port=6633)
    net = Mininet_wifi(accessPoint=OVSKernelAP)
    net.propagationModel(model="logDistance", exp=3)

    info("*** Creating nodes\n")
    # mode = 'mininet'
    if mode == 'mininet':
        h1 = net.addHost(
            'h1', cls=Node, mac='00:00:00:00:00:01', ip='10.0.0.11/8')
        sta1 = net.addStation(
            'sta1', cls=Station, mac='00:00:00:00:00:02', ip='10.0.0.12/8')
        sta2 = net.addStation(
            'sta2', cls=Station, mac='00:00:00:00:00:03', ip='10.0.0.13/8')
    else:
        dimage_name = 'kumokay/ubuntu_wifi:v2'
        h1 = net.addHost(
            'h1', cls=Docker, dimage=dimage_name,
            mac='00:00:00:00:00:01', ip='10.0.0.11/8')
        sta1 = net.addStation(
            'sta1', cls=DockerStation, dimage=dimage_name,
            mac='00:00:00:00:00:02', ip='10.0.0.12/8')
        sta2 = net.addStation(
            'sta2', cls=DockerStation, dimage=dimage_name,
            mac='00:00:00:00:00:03', ip='10.0.0.13/8')
    ap1 = net.addAccessPoint(
        'ap1', ssid='new-ssid', mode='g', channel='1', position='0,0,0')
    net.addController(c1)

    info("*** Configuring wifi nodes\n")
    net.configureWifiNodes()

    info("*** Associating and Creating links\n")
    net.addLink(ap1, h1)

    # net.plotGraph(max_x=200, max_y=200)
    net.startMobility(time=0, repetitions=1)
    net.mobility(sta1, 'start', time=1, position='0.0, 0.0, 0.0')
    net.mobility(sta2, 'start', time=1, position='0.0, 0.0, 0.0')
    net.mobility(sta1, 'stop', time=22, position='40.0, 40.0, 0.0')
    net.mobility(sta2, 'stop', time=22, position='20.0, 20.0, 0.0')
    net.stopMobility(time=23)

    info("*** Starting network\n")
    net.build()
    c1.start()
    ap1.start([c1])

    if is_enable_cli:
        info("*** Running CLI\n")
        CLI_wifi(net)

    info("*** Stopping network\n")
    net.stop()


if __name__ == '__main__':
    setLogLevel('debug')
    coord = True if '-c' in sys.argv else False
    topology()
