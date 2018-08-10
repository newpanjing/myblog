import uuid
array = ["a", "b", "c", "d", "e", "f",
         "g", "h", "i", "j", "k", "l", "m", "n", "o", "p", "q", "r", "s",
         "t", "u", "v", "w", "x", "y", "z", "0", "1", "2", "3", "4", "5",
         "6", "7", "8", "9", "A", "B", "C", "D", "E", "F", "G", "H", "I",
         "J", "K", "L", "M", "N", "O", "P", "Q", "R", "S", "T", "U", "V",
         "W", "X", "Y", "Z"]


def get_short_id():
    id = str(uuid.uuid4()).replace("-", '')
    buffer = []

    for i in range(0, 8):
        start = i * 4
        end = i * 4 + 4
        val = int(id[start:end], 16)
        buffer.append(array[val % 62])
    return "".join(buffer)

