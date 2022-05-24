"""
CSAPX Lab 1: Secret Messages

A program that encodes/decodes a message by applying a set of transformation operations.
The transformation operations are:
    shift - Sa[,n] changes letter at index a by moving it n letters fwd in the alphabet
    rotate - R[n] rotates the string n positions to the right
    duplicate - Da[,n] follows character at index a with n copies of itself
    trade - T[(g)]a,b swaps the places of the a-th and b-th groups of g total

All indices and group numbers are 0-based.

author: Miguel Reyes
"""


def rotate(msg: str) -> str:
    """
    R rotates the string one position to the right. So, TOPS→ R → STOP.
    Look at pss sheet for rotate description
    :param msg: str
    :return: str
    """
    # 1st slice = last letter of word + 2nd slice = beg of word up until the end(exclusive)
    string = msg[-1] + msg[:-1]
    return string


def rotate2(msg: str, i: int) -> str:
    """
    Rotate function Ri can also be used with an exponent (positive or negative). For example,
    TRAIN→ R2 → INTRA.
    :param msg: str
    :param i: int
    :return: str
    """
    # Since rotation is always forward 1st slice = [-i :] & 2nd slice = [ : -i ]
    string = msg[-i:] + msg[:-i]
    return string


def rotate3(msg: str) -> str:
    """
    Inverse of rotate()
    :param msg: str
    :return: str
    """
    string = msg[1:] + msg[: 1]
    return string


# The trick for shift is to know that we have to check
# if the unicode to our new char is > "z" because if it is we have to
# subtract it by 26 in order for us to wrap around the alphabet again. lowercase alphabet deci is 97-122

def shift(msg: str, i: int) -> str:
    """
    Si shifts the letter at index i forward one letter in the alphabet. So, BALL→ S0 → CALL.
    :param msg: str
    :param i: int
    :return: str
    """
    unicode = ord(msg[i]) + 1
    if unicode > ord("Z"):
        unicode -= 26
    elif unicode < ord("A"):
        unicode += 26
    new_letter = chr(unicode)
    return msg[:i] + new_letter + msg[i + 1:]


def shift2(msg: str, i: int, k: int) -> str:
    """
    Si,k This can be applied multiple times to shift multiple letters forward,
    and if so would be designated S(i,k) to shift letter i by k forward.
    If the shift takes the letter past the end of the alphabet, it will wrap around.
    Negative exponents shift the letter backward in the alphabet.
    :param msg: str
    :param i: int
    :param k: int
    :return: str
    """
    unicode = ord(msg[i]) + k
    if unicode > ord("Z"):
        unicode -= 26
    elif unicode < ord("A"):
        unicode += 26
    new_letter = chr(unicode)
    return msg[:i] + new_letter + msg[i + 1:]


def shift3(msg: str, i: int) -> str:
    """
    Inverse of shift()
    :param msg: str
    :param i: int
    :return: str
    """
    unicode = ord(msg[i]) - 1
    if unicode > ord("Z"):
        unicode -= 26
    elif unicode < ord("A"):
        unicode += 26
    new_letter = chr(unicode)
    return msg[: i] + new_letter + msg[i + 1:]


def duplicate(msg: str, i: int) -> str:
    """
    Di duplicates (in place) the letter at index i. So, HOPED→ D2 → HOPPED
    :param msg:
    :param i:
    :return: str
    """

    letter = msg[i]
    return msg[: i] + letter + msg[i:]


def duplicate2(msg: str, i: int, k: int) -> str:
    """
    Duplicates Di,k can also be used with a positive exponent to produce multiple duplicates,
    but not with negative exponents.
    :param msg:
    :param i:
    :param k:
    :return: str
    """
    letter = msg[i]
    newWord = msg[: i] + letter * k + msg[i:]
    return newWord


def duplicate3(msg: str, i: int) -> str:
    """
    inverse of duplicate()
    :param msg:
    :param i:
    :return: str
    """
    return msg[: i] + msg[i + 1:]


def duplicate4(msg: str, i: int, k: int) -> str:
    """
    inverse of duplicate2()
    :param msg:
    :param i:
    :param k:
    :return: str
    """
    letter = msg[i]
    newWord = msg[: i] + letter + msg[i * k:]
    return newWord


def trade(msg: str, i: int, j: int) -> str:
    """
    Ti,j swaps the letters at index i and index j. So, SAUCE→ T0,3 → CAUSE. You can
    assume that i < j.
    :param msg:
    :param i:
    :param j:
    :return: str
    """
    letter1 = msg[i]
    letter2 = msg[j]
    return msg[: i] + letter2 + msg[i + 1: j] + letter1 + msg[j + 1:]


def trade2(msg: str, i: int, j: int, g: int) -> str:
    """
    T(g)i,j operates a little differently. In this case, we conceptually divide the string to g
    equal-sized groups of letters, and then swap groups i and j. So, BACKHAND → T(4)0,2 → HACKBAND.
    :param msg:
    :param i:
    :param j:
    :param g:
    :return: str
    """
    wordLength = len(msg) // g
    newWord = ""
    for k in range(0, len(msg), wordLength):
        newWord += msg[k: wordLength + k] + " "
    listWord = newWord.split(" ")
    iIs = listWord[i]
    jIs = listWord[j]
    listWord[i] = jIs
    listWord[j] = iIs
    finalWord = ""
    for item in listWord:
        finalWord += item
    return finalWord.replace(" ", "")


def transform(msg: str, cmds: str) -> str:
    """
     Transform function takes a string message and a string of transformation operations.
     This function's responsible for reading through the string of transformation operation, storing parameters
     and passing those parameters to the transformation functions. It handles both encryption & decryption.
    :param msg: str
    :param cmds: str
    :return: str
    """
    # this if statement will deal with encoding transformations
    if cmds.find(";") != -1:
        ops = cmds.split(';')
        for op in ops:
            if op[0] == 'S':
                if op.find(',') != -1:
                    i = int(op[1:op.find(',')])
                    k = int(op[op.find(',') + 1:])
                    msg = shift2(msg, i, k)
                else:
                    i = int(op[1:])
                    msg = shift(msg, i)
            elif op[0] == 'R':
                if len(op) == 1:
                    msg = rotate(msg)
                else:
                    i = int(op[1:])
                    msg = rotate2(msg, i)
            elif op[0] == 'D':
                if op.find(',') != -1:
                    i = int(op[1:op.find(',')])
                    k = int(op[op.find(',') + 1:])
                    msg = duplicate2(msg, i, k)
                else:
                    i = int(op[1:])
                    msg = duplicate(msg, i)
            elif op[0] == 'T':
                if op.find('(') != -1:
                    g = int(op[op.find("(") + 1: op.find(")")])
                    i = int(op[op.find(")") + 1: op.find(',')])
                    j = int(op[op.find(',') + 1:])
                    msg = trade2(msg, i, j, g)
                else:
                    i = int(op[1:op.find(',')])
                    j = int(op[op.find(',') + 1:])
                    msg = trade(msg, i, j)
    else:
        # Here we will deal with decoding transformations
        ops = cmds.split()
        for op in ops:
            if op[0] == 'S':
                if op.find(',') != -1:
                    i = int(op[1:op.find(',')])
                    k = int(op[op.find(',') + 1:])
                    msg = shift2(msg, i, -k)
                else:
                    i = int(op[1:])
                    msg = shift3(msg, i)
            elif op[0] == 'R':
                if len(op) == 1:
                    msg = rotate3(msg)
                else:
                    i = int(op[1:])
                    msg = rotate2(msg, -i)
            elif op[0] == 'D':
                if op.find(',') != -1:
                    i = int(op[1:op.find(',')])
                    k = int(op[op.find(',') + 1:])
                    msg = duplicate4(msg, i, k)
                else:
                    i = int(op[1:])
                    msg = duplicate3(msg, i)
            elif op[0] == 'T':
                if op.find('(') != -1:
                    g = int(op[op.find("(") + 1: op.find(")")])
                    i = int(op[op.find(")") + 1: op.find(',')])
                    j = int(op[op.find(',') + 1:])
                    msg = trade2(msg, i, j, g)
                else:
                    i = int(op[1:op.find(',')])
                    j = int(op[op.find(',') + 1:])
                    msg = trade(msg, i, j)
    return msg


def reverseOperations(enFile: str) -> str:
    """
    This function will take each line in the operations file and convert it into a list
    which then gets reversed. In other words it gives us the inverse of the transformation operations.
    :param enFile:
    :return:
    """
    ops = enFile.split(';')
    i = 1
    j = 0
    finalOps = ""
    finalList = []
    for k in range(len(ops)):
        finalList.append(ops[-i])
        i += 1
        finalOps += finalList[j] + " "
        j += 1
    return finalOps


def main() -> None:
    """
    The main program is responsible for getting the input details from user and writing the output file with the results
    of encrypting or decrypting the message file applying the transformations from the operation file.
    :return: None
    """

    msgFile = input("Please enter the message file: ")
    cmdsFile = input("Please enter the operations file: ")
    outputFile = input("Please enter output file name: ")
    enOrDecrypt = input("(E)ncrypt or (D)ecrypt ? ")

    print("Generating output...")
    with open(msgFile) as mF, open(cmdsFile) as cF, open(outputFile, "w") as oF:
        for msg in mF:
            msg = msg.rstrip()
            cmd = cF.readline()
            cmds = cmd.rstrip()
            if enOrDecrypt == 'E':
                oF.write(transform(msg, cmds) + "\n")
                print(transform(msg, cmds))
            else:
                oF.write(transform(msg, reverseOperations(cmds)) + "\n")
                print(transform(msg, reverseOperations(cmds)))


if __name__ == '__main__':
    main()
