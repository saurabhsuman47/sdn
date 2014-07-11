'''
Coursera:
- Software Defined Networking (SDN) course
-- Network Virtualization

Professor: Nick Feamster
Teaching Assistant: Arpit Gupta
'''

from pox.core import core
from collections import defaultdict

import pox.openflow.libopenflow_01 as of
import pox.openflow.discovery
import pox.openflow.spanning_tree

from pox.lib.revent import *
from pox.lib.util import dpid_to_str
from pox.lib.util import dpidToStr
from pox.lib.addresses import IPAddr, EthAddr
from collections import namedtuple
import os

log = core.getLogger()


class TopologySlice (EventMixin):

    def __init__(self):
        self.listenTo(core.openflow)
        log.debug("Enabling Slicing Module")
        
        
    """This event will be raised each time a switch will connect to the controller"""
    def _handle_ConnectionUp(self, event):
        
        # Use dpid to differentiate between switches (datapath-id)
        # Each switch has its own flow table. As we'll see in this 
        # example we need to write different rules in different tables.
        dpid = dpidToStr(event.dpid)
        log.debug("Switch %s has come up.", dpid)
        
        if dpid[-2:]==("01" or "04"):

            fm1=of.ofp_flow_mod()
            fm1.match.in_port=3
            fm1.actions.append(of.ofp_action_output(port=1))
            event.connection.send(fm1)

            fm2=of.ofp_flow_mod()
            fm2.match.in_port=1
            fm2.actions.append(of.ofp_action_output(port=3))
            event.connection.send(fm2)

            fm3=of.ofp_flow_mod()
            fm3.match.in_port=2
            fm3.actions.append(of.ofp_action_output(port=4))
            event.connection.send(fm3)

            fm4=of.ofp_flow_mod()
            fm4.match.in_port=4
            fm4.actions.append(of.ofp_action_output(port=2))
            event.connection.send(fm4)

        if dpid[-2:]==("02" or "03"):
            
            fm5=of.ofp_flow_mod;
            fm5.match.in_port=1
            fm5.actions.append(of.ofp_action_output(port=2))
            event.connection.send(fm5)

            fm6=of.ofp_flow_mod
            fm6.match.in_port=2
            fm6.actions.append(of.ofp_action_output(port=1))
            event.connection.send(fm6)
    
        

        

def launch():
    # Run spanning tree so that we can deal with topologies with loops
    pox.openflow.discovery.launch()
    pox.openflow.spanning_tree.launch()

    '''
    Starting the Topology Slicing module
    '''
    core.registerNew(TopologySlice)
