# coding=utf-8
#
# Copyright 2013  Red Hat, Inc.
# Giuseppe Scrivano <gscrivan@redhat.com>
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free  Software Foundation; either version 2 of the License, or
# (at your option)  any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston,
# MA 02110-1301 USA.

from virtinst.VirtualDevice import VirtualDevice
from virtinst.XMLBuilderDomain import _xml_property


class VirtualRNGDevice(VirtualDevice):

    _virtual_device_type = VirtualDevice.VIRTUAL_DEV_RNG

    TYPE_RANDOM = "random"
    TYPE_EGD = "egd"
    TYPES = [TYPE_RANDOM, TYPE_EGD]

    BACKEND_TYPE_UDP = "udp"
    BACKEND_TYPE_TCP = "tcp"
    BACKEND_TYPES = [BACKEND_TYPE_UDP, BACKEND_TYPE_TCP]

    BACKEND_MODE_BIND = "bind"
    BACKEND_MODE_CONNECT = "connect"
    BACKEND_MODES = [BACKEND_MODE_BIND, BACKEND_MODE_CONNECT]

    def __init__(self, conn=None, parsexml=None, parsexmlnode=None, caps=None):
        VirtualDevice.__init__(self, conn, parsexml, parsexmlnode, caps)
        self._type = None
        self._model = None
        self._backend_type = None
        self._bind_host = None
        self._bind_service = None
        self._connect_host = None
        self._connect_service = None
        self._rate_bytes = None
        self._rate_period = None

        self._device = None
        if self._is_parse():
            return

    @staticmethod
    def get_pretty_type(rng_type):
        if rng_type == VirtualRNGDevice.TYPE_RANDOM:
            return _("Random")
        if rng_type == VirtualRNGDevice.TYPE_EGD:
            return _("Entropy Gathering Daemon")
        return rng_type

    @staticmethod
    def get_pretty_backend_type(backend_type):
        return {"udp" : "UDP",
                "tcp": "TCP"}.get(backend_type) or backend_type

    @staticmethod
    def get_pretty_mode(mode):
        return {"bind" : "Bind",
                "connect": "Connect"}.get(mode) or mode


    def backend_mode(self):
        ret = []
        if self.bind_host or self.bind_service:
            ret.append(VirtualRNGDevice.BACKEND_MODE_BIND)
        if self.connect_host or self.connect_service:
            ret.append(VirtualRNGDevice.BACKEND_MODE_CONNECT)
        return ret

    def supports_property(self, propname):
        """
        Whether the rng dev type supports the passed property name
        """
        users = {
            "type"                   : [self.TYPE_EGD, self.TYPE_RANDOM],

            "model"                  : [self.TYPE_EGD, self.TYPE_RANDOM],
            "bind_host"              : [self.TYPE_EGD],
            "bind_service"           : [self.TYPE_EGD],
            "connect_host"           : [self.TYPE_EGD],
            "connect_service"        : [self.TYPE_EGD],
            "backend_type"           : [self.TYPE_EGD],
            "device"                 : [self.TYPE_RANDOM],
            "rate_bytes"             : [self.TYPE_EGD, self.TYPE_RANDOM],
            "rate_period"            : [self.TYPE_EGD, self.TYPE_RANDOM],
        }
        if users.get(propname):
            return self.type in users[propname]

        return hasattr(self, propname)

    def _get_type(self):
        return self._type
    def _set_type(self, m):
        self._type = m
    type = _xml_property(_get_type, _set_type, xpath="./backend/@model")

    def _get_model(self):
        return self._model
    def _set_model(self, m):
        self._model = m
    model = _xml_property(_get_model, _set_model, xpath="./@model")

    def _get_backend_type(self):
        return self._backend_type
    def _set_backend_type(self, t):
        self._backend_type = t
    backend_type = _xml_property(_get_backend_type,
                                 _set_backend_type,
                                 xpath="./backend/@type")

    def _get_bind_host(self):
        return self._bind_host
    def _set_bind_host(self, m):
        self._bind_host = m
    bind_host = _xml_property(_get_bind_host,
                              _set_bind_host,
                              xpath="./backend/source[@mode='bind']/@host")

    def _get_connect_host(self):
        return self._connect_host
    def _set_connect_host(self, m):
        self._connect_host = m
    connect_host = _xml_property(_get_connect_host,
                                 _set_connect_host,
                               xpath="./backend/source[@mode='connect']/@host")

    def _get_bind_service(self):
        return self._bind_service
    def _set_bind_service(self, m):
        self._bind_service = m
    bind_service = _xml_property(_get_bind_service,
                                 _set_bind_service,
                                xpath="./backend/source[@mode='bind']/@service")
    def _get_connect_service(self):
        return self._connect_service
    def _set_connect_service(self, m):
        self._connect_service = m
    connect_service = _xml_property(_get_connect_service,
                                    _set_connect_service,
                          xpath="./backend/source[@mode='connect']/@service")

    def _get_rate_bytes(self):
        return self._rate_bytes
    def _set_rate_bytes(self, b):
        self._rate_bytes = b
    rate_bytes = _xml_property(_get_rate_bytes,
                               _set_rate_bytes,
                               xpath="./rate/@bytes")

    def _get_rate_period(self):
        return self._rate_period
    def _set_rate_period(self, p):
        self._rate_period = p
    rate_period = _xml_property(_get_rate_period,
                                _set_rate_period,
                                xpath="./rate/@period")

    def _get_device(self):
        if self._type == self.TYPE_RANDOM:
            return self._device
        return None
    def _set_device(self, d):
        self._device = d
    device = _xml_property(_get_device, _set_device, xpath="./backend")

    def _get_xml_config(self):
        rng_model = self.model or "virtio"
        xml  = ("    <rng model='%s'>\n" % rng_model)

        if self.rate_bytes or self.rate_period:
            xml += "      <rate"
            if self.rate_period:
                xml += " period='%s'" % self.rate_period
            if self.rate_bytes:
                xml += " bytes='%s'" % self.rate_bytes
            xml += "/>\n"

        if self.type == self.TYPE_RANDOM:
            xml += "      <backend model='random'>%s</backend>\n" % self.device
        else:
            model = "model='%s'" % self.type
            backend_type = "type='%s'" % (self.backend_type or "tcp")
            xml += "      <backend %s %s>\n" % (model, backend_type)

            def add_source(mode, host, service):
                ret = "        <source mode='%s'" % mode
                if host:
                    ret += " host='%s'" % host
                if service:
                    ret += " service='%s'" % service
                return ret + "/>\n"

            if self.bind_host or self.bind_service:
                xml += add_source("bind", self.bind_host, self.bind_service)
            if self.connect_host or self.connect_service:
                xml += add_source("connect", self.connect_host, \
                                  self.connect_service)
            xml += "      </backend>\n"

        xml += "    </rng>"
        return xml
