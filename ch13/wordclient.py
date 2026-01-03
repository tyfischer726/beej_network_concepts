import sys
import socket

# How many bytes is the word length?
WORD_LEN_SIZE = 2

def usage():
    print("usage: wordclient.py server port", file=sys.stderr)

packet_buffer = b''

def get_next_word_packet(s):
    """
    Return the next word packet from the stream.

    The word packet consists of the encoded word length followed by the
    UTF-8-encoded word.

    Returns None if there are no more words, i.e. the server has hung
    up.
    """

    global packet_buffer

    # TODO -- Write me!

    # on the first call, fills packet_buffer with all data from stream
    if len(packet_buffer) == 0:
        while (len(temp := s.recv(20)) > 0):
            packet_buffer += temp
    
    # buffer size is reduced after each word_packet is extracted.
    # if buffer size reaches 0, above block will execute.
    # if buffer size is still 0 after above block,
    # stream must be done sending data, return None.
    if len(packet_buffer) == 0:
        return None

    word_len = int.from_bytes(packet_buffer[:2], "big")
    packet_len = 2 + word_len

    word_packet = packet_buffer[: packet_len + 1]
    packet_buffer = packet_buffer[packet_len :]

    return word_packet


def extract_word(word_packet):
    """
    Extract a word from a word packet.

    word_packet: a word packet consisting of the encoded word length
    followed by the UTF-8 word.

    Returns the word decoded as a string.
    """

    # TODO -- Write me!
    word = word_packet[2:].decode()

    return word

# Do not modify:

def main(argv):
    try:
        host = argv[1]
        port = int(argv[2])
    except:
        usage()
        return 1

    s = socket.socket()
    s.connect((host, port))

    print("Getting words:")

    while True:
        word_packet = get_next_word_packet(s)

        if word_packet is None:
            break

        word = extract_word(word_packet)

        print(f"    {word}")

    s.close()

if __name__ == "__main__":
    sys.exit(main(sys.argv))
