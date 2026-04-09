import smbus

class MCP3021:
    bus = smbus.SMBus(1)
    

    def __init__(self, address = 0x4B):
        self.address = address

    def read_raw(self):
        # Reads word (16 bits) as int
        rd = self.bus.read_word_data(self.address, 0)
        # Exchanges upper and lower bytes
        data = ((rd & 0xFF) << 8) | ((rd & 0xFF00) >> 8)
        # Ignores two least significiant bits
        return data >> 2
    
    def read_percent(self):
        dry = 770
        wet = 284
        raw = self.read_raw()
        # Maps raw value to percentage
        return (dry - raw) * 100 / (dry - wet)
    
adc = MCP3021()
# Fuld våd: 284
# Fuld tør: 770

# while True:
#     raw = adc.read_raw()
#     print("Raw :", raw)
#     print("Percent :", adc.read_percent())
#     time.sleep(1)