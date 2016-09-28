# # -*- coding: utf-8 -*-

import unittest, pytest, os
from declarativeunittest import raises
ontravis = 'TRAVIS' in os.environ

from construct import *
from construct.lib import *
from construct.examples.protocols.ipstack import *

from io import BytesIO
import os, random, itertools, hashlib, binascii
from binascii import hexlify, unhexlify
ident = lambda x: x



class TestProtocols(unittest.TestCase):

    def commondump(self, format, filename):
        if ontravis:
            filename = "examples/protocols/" + filename
        if not ontravis:
            filename = "tests/examples/protocols/" + filename
        with open(filename,'rb') as f:
            data = f.read()
        obj = format.parse(data)
        print(obj)
        print(hexlify(data))

    def commonhex(self, format, hexdata):
        self.commonbytes(format, binascii.unhexlify(hexdata))

    def commonbytes(self, format, bytesdata):
        obj = format.parse(bytesdata)
        print(obj)
        data = format.build(obj)
        print(hexlify(bytesdata))
        print(hexlify(data))
        assert hexlify(bytesdata) == hexlify(data)


    def test_ethernet(self):
        self.commonhex(ethernet_header, b"0011508c283c0002e34260090800")

    def test_arp(self):
        self.commonhex(arp_header, b"00010800060400010002e3426009c0a80204000000000000c0a80201")
        self.commonhex(arp_header, b"00010800060400020011508c283cc0a802010002e3426009c0a80204")

    def test_ip4(self):
        self.commonhex(ipv4_header, b"4500003ca0e3000080116185c0a80205d474a126")

    def test_ip6(self):
        self.commonhex(ipv6_header, b"6ff00000010206803031323334353637383941424344454646454443424139383736353433323130")

    def test_icmp(self):
        self.commonhex(icmp_header, b"0800305c02001b006162636465666768696a6b6c6d6e6f7071727374757677616263646566676869")
        self.commonhex(icmp_header, b"0000385c02001b006162636465666768696a6b6c6d6e6f7071727374757677616263646566676869")
        self.commonhex(icmp_header, b"0301000000001122aabbccdd0102030405060708")

    def test_igmp(self):
        self.commonhex(igmpv2_header, b"1600FA01EFFFFFFD")

    def test_dhcp4(self):
        data = b"0101060167c05f5a00000000"+b"0102030405060708090a0b0c"+b"0d0e0f10"+b"DEADBEEFBEEF"+b"000000000000000000000000000000000000000000000000000000"+b"000000000000000000000000000000000000000000000000000000"+b"000000000000000000000000000000000000000000000000000000"+b"000000000000000000000000000000000000000000000000000000"+b"000000000000000000000000000000000000000000000000000000"+b"000000000000000000000000000000000000000000000000000000"+b"000000000000000000000000000000000000000000000000000000"+b"00000000000000000000000000"+b"63825363"+b"3501083d0701DEADBEEFBEEF0c04417375733c084d53465420352e"+b"30370d010f03062c2e2f1f2179f92bfc52210117566c616e333338"+b"382b45746865726e6574312f302f32340206f8f0827348f9"
        self.commonhex(dhcp4_header, data)

    def test_dhcp6(self):
        data = b"\x03\x11\x22\x33\x00\x17\x00\x03ABC\x00\x05\x00\x05HELLO"
        self.commonbytes(dhcp6_message, data)
        test2 = b"\x0c\x040123456789abcdef0123456789abcdef\x00\x09\x00\x0bhello world\x00\x01\x00\x00"
        self.commonbytes(dhcp6_message, data)

    def test_tcp(self):
        self.commonhex(tcp_header, b"0db5005062303fb21836e9e650184470c9bc0000")

    def test_udp(self):
        self.commonhex(udp_header, b"0bcc003500280689")

    def test_dns(self):
        self.commonhex(dns, b"2624010000010000000000000377777706676f6f676c6503636f6d0000010001")

    @pytest.mark.xfail(reason="rebuilt data is different")
    def test_dns2(self):
        self.commonhex(dns, b"2624818000010005000600060377777706676f6f676c6503636f6d0000010001c00c0005000100089065000803777777016cc010c02c0001000100000004000440e9b768c02c0001000100000004000440e9b793c02c0001000100000004000440e9b763c02c0001000100000004000440e9b767c030000200010000a88600040163c030c030000200010000a88600040164c030c030000200010000a88600040165c030c030000200010000a88600040167c030c030000200010000a88600040161c030c030000200010000a88600040162c030c0c00001000100011d0c0004d8ef3509c0d0000100010000ca7c000440e9b309c080000100010000c4c5000440e9a109c0900001000100004391000440e9b709c0a0000100010000ca7c000442660b09c0b00001000100000266000440e9a709")

    def test_ip_stack(self):
        self.commonhex(ip_stack, b"0011508c283c001150886b570800450001e971474000800684e4c0a80202525eedda112a0050d98ec61d54fe977d501844705dcc0000474554202f20485454502f312e310d0a486f73743a207777772e707974686f6e2e6f72670d0a557365722d4167656e743a204d6f7a696c6c612f352e30202857696e646f77733b20553b2057696e646f7773204e5420352e313b20656e2d55533b2072763a312e382e302e3129204765636b6f2f32303036303131312046697265666f782f312e352e302e310d0a4163636570743a20746578742f786d6c2c6170706c69636174696f6e2f786d6c2c6170706c69636174696f6e2f7868746d6c2b786d6c2c746578742f68746d6c3b713d302e392c746578742f706c61696e3b713d302e382c696d6167652f706e672c2a2f2a3b713d302e350d0a4163636570742d4c616e67756167653a20656e2d75732c656e3b713d302e350d0a4163636570742d456e636f64696e673a20677a69702c6465666c6174650d0a4163636570742d436861727365743a2049534f2d383835392d312c7574662d383b713d302e372c2a3b713d302e370d0a4b6565702d416c6976653a203330300d0a436f6e6e656374696f6e3a206b6565702d616c6976650d0a507261676d613a206e6f2d63616368650d0a43616368652d436f6e74726f6c3a206e6f2d63616368650d0a0d0a")
        self.commonhex(ip_stack, b"0002e3426009001150f2c280080045900598fd22000036063291d149baeec0a8023c00500cc33b8aa7dcc4e588065010ffffcecd0000485454502f312e3120323030204f4b0d0a446174653a204672692c2031352044656320323030362032313a32363a323520474d540d0a5033503a20706f6c6963797265663d22687474703a2f2f7033702e7961686f6f2e636f6d2f7733632f7033702e786d6c222c2043503d2243414f2044535020434f52204355522041444d204445562054414920505341205053442049564169204956446920434f4e692054454c6f204f545069204f55522044454c692053414d69204f54526920554e5269205055426920494e4420504859204f4e4c20554e49205055522046494e20434f4d204e415620494e542044454d20434e542053544120504f4c204845412050524520474f56220d0a43616368652d436f6e74726f6c3a20707269766174650d0a566172793a20557365722d4167656e740d0a5365742d436f6f6b69653a20443d5f796c683d58336f444d54466b64476c6f5a7a567842463954417a49334d5459784e446b4563476c6b417a45784e6a59794d5463314e5463456447567a64414d7742485274634777446157356b5a58677462412d2d3b20706174683d2f3b20646f6d61696e3d2e7961686f6f2e636f6d0d0a436f6e6e656374696f6e3a20636c6f73650d0a5472616e736665722d456e636f64696e673a206368756e6b65640d0a436f6e74656e742d547970653a20746578742f68746d6c3b20636861727365743d7574662d380d0a436f6e74656e742d456e636f64696e673a20677a69700d0a0d0a366263382020200d0a1f8b0800000000000003dcbd6977db38b200faf9fa9cf90f88326dd9b1169212b5d891739cd84ed2936d1277a7d3cbf1a1484a624c910c4979893bbfec7d7bbfec556121012eb29d65e6be7be7762c9240a1502854150a85c2c37b87af9f9c7c7873449e9dbc7c41defcf2f8c5f327a4d1ee76dff79e74bb872787ec43bfa3e9ddeed1ab06692cd234daed762f2e2e3a17bd4e18cfbb276fbb8b74e9f7bb491a7b76da7152a7b1bff110dfed3f5cb896030f4b37b508566dbb9f56def9a4f1240c523748db275791db20367b9a3452f732a5d0f688bdb0e2c44d27bf9c1cb7470830b1632f4a490a3578c18fd6b9c5dec2f7732b2641783109dc0b7268a56e2bd527a931497b93b43f49cd493a98a4c3493a9aa4e349aa6bf01f7cd78d89d6b2ed49b3d9baf223f8b307b5004a67eea627ded2dddadedb78d8656de428f856305f5973779223b0fff05ebbbde1db67082a499289ae0f06863e1c8f4c0639eaccbdd9a3547abf798a1f0ec6c73fafd2e4f151ffd5f1c9e2f9e37ff74e74fbddd941b375eadb0942b3e3d5723a69f6060373a6cff49e6df586dac8b11c4d1f1afd81319b0df45e6fd4925a6cee6db4dbfb19e225bc1b12e56a098aed9309715c3b74dc5fde3e7f122ea3308061dac22f4018a4f8878367af5f4f2ebcc001a2d187bfffbefeb2477f75026be9269165bb93d92ab0532f0cb68264fbda9b6ddd0b92bfff867f3abe1bccd3c5f675eca6ab3820c1caf7f7be20e05363029f93c8f7d2ad46a7b1bd475ff62614f2de2c8cb7f08537d93a35fed0fe9a4c1af44363fb91beabed790f4f0d0e7a6f67c7dbbe3eedfd01e5bcbffe9a64bf289e00307bb1f7852371dadb133df0c3798efba9d93a1db44e87dbd7d8b4cf50e95c780e304be745389fbbf11ef4cddfdcf4b162d629fa94d7defbe2fa892b3ece2c78d8fb221a84517003476a73dc3ad535d6e22c7fbd0db8cf3a511ca6211d3e28933fed9d8ea54f381f66c0c7f2cb0e4c3898ad2b3b0de3c9e918bf25abc88d6ddf02d65581418f94174addc9ebe94717e67ce557207b6d45f892773ae393adc62af57c18ecd27b46e5aa2feea5b58c7c173e6d94be1d3bd5afa3fcf571d409ded9b1eb06ef3d275d00c36f25f4916c6ed2a911cef88b0e4c0ecfa7a5b627936600b3d28d9bdbe411")


