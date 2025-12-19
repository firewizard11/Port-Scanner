"""Contains functions to create and parse TCP/IP Packets"""
import struct

def create_ipv4_packet(src_ip: str, dest_ip: str, dscp: int, ecn: int, id: int, df: bool, mf: bool, ttl: int, protocol: int, options, data):
    pass

def parse_ipv4_packet(packet):
    pass

def ip_checksum(header):
    pass
