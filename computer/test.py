def chrs_from_bin(bin):
    ascii = ""
    while len(bin)!=0:
        bin_segment = bin[:5]
        bin = bin[5:]
        dec = int(bin_segment, 2)
        ascii += chr(33+dec)
    return ascii