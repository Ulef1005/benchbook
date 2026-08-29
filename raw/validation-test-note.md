Quick note from a workshop talk on mDNS (multicast DNS, RFC 6762). It lets devices on a local
network resolve hostnames like `printer.local` without a central DNS server — each device
answers for its own name by listening on the multicast address 224.0.0.251 (or the IPv6
equivalent) on UDP port 5353. Paired with DNS-SD (RFC 6763) it's how mDNS does service
discovery too: a device can ask "who offers _http._tcp on this network?" and get a list back,
which is the mechanism Bonjour/Avahi and a lot of smart-home gear (like ESPHome devices)
build on for auto-discovery. The talk's main caution: mDNS traffic doesn't cross routers by
default (multicast is link-local), so it silently breaks the moment a device moves to a
different VLAN or a guest network — a lot of "why can't I see my printer/ESPHome device"
tickets trace back to exactly this. Some routers offer an mDNS reflector/repeater to bridge
segments on purpose.
