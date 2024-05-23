from typing import Dict, List, ByteString
from pathlib import Path
from argparse import ArgumentParser
from enum import Enum
from dataclasses import dataclass


DEFAULT_UTMP_PATH = "/var/run/utmp"
UTMP_STRUCT_BLOCK_SIZE = 384 #Bytes
#For my system, I have these in `users` bytes,
#I think it's reservred in `utmp` file,
#So we ignore them :)
IGNORE_UTMP_RESERVED = { "reboot", "LOGIN", "runlevel"}


USAGE = "%(prog)s [Options]"
DESC = "pusers is a command that shows current users on system."

class UtmpStruct(Enum):
    """Utmp C structure,
    
    dict structure is 
    `
    {
        "start_byte": byte index of the value. (int)
        "size": how many bytes is used for that value. (int)
    }
    `
    `size` = `start_byte` + `actual_size`

    """
    UT_TYPE = {"start_byte": 0, "size": 0+4}
    UT_PID = {"start_byte": 4, "size": 4+4}
    UT_LINE = {"start_byte": 8, "size": 8+32}
    UT_ID = {"start_byte": 40, "size": 40+4}
    UT_USER = {"start_byte": 44, "size": 44+32}
    UT_HOST = {"start_byte": 76, "size": 76+256}
    UT_EXIT = {"start_byte": 332, "size": 332+4}
    UT_SESSION = {"start_byte": 336, "size": 336+4}
    UT_TV = {"start_byte": 340, "size": 340+8}
    UT_ADDR_V6 = {"start_byte": 348, "size": 348+16}


@dataclass
class UtmpBlock:
    UT_TYPE: str
    UT_PID: str
    UT_LINE: str
    UT_ID: str
    UT_USER: list
    UT_HOST: str
    UT_EXIT: str
    UT_SESSION: str
    UT_TV: str
    UT_ADDR_V6: str


def read_utmp(path: str) -> Dict[int, List[ByteString]]:
    """Reads `utmp` binary file.

    Parameters
    ----------
    path : str
        Path of `utmp` file, default `/var/run/utmp`

    Returns
    -------
    Dict[int, List[ByteString]]
        Blocks of `utmp struct` bytes, each block is `384` bytes
    """
    path = Path(path)
    blocks = dict()
    mode = "rb" #Read Binaries

    with open(path, mode=mode) as f:
        f = f.read()
        file_length = len(f)

        pointer_indx = 0
        while pointer_indx < file_length:
            blocks[pointer_indx] = list()

            for byte_indx in range(pointer_indx, pointer_indx + UTMP_STRUCT_BLOCK_SIZE):
                blocks[pointer_indx].append(f[byte_indx])

            pointer_indx = pointer_indx + UTMP_STRUCT_BLOCK_SIZE

    return blocks


def parse_utmp(utmp_blocks: Dict[int, List[ByteString]]) -> List[UtmpBlock]:
    """Parse utmp blocks into `UtmpBlock`

    Parameters
    ----------
    utmp_blocks : Dict[int, List[ByteString]]
        raw binary blocks in `utmp` file.

    Returns
    -------
    List[UtmpBlock]
        list of blocks structured in `UtmpBlock` structure.
    """
    utmp_data = list()

    for block_indx, byte_list in utmp_blocks.items():
        block = UtmpBlock(
            UT_TYPE=byte_list[UtmpStruct.UT_TYPE.value["start_byte"]:UtmpStruct.UT_TYPE.value["size"]],
            UT_PID=byte_list[UtmpStruct.UT_PID.value["start_byte"]:UtmpStruct.UT_PID.value["size"]],
            UT_LINE=byte_list[UtmpStruct.UT_LINE.value["start_byte"]:UtmpStruct.UT_LINE.value["size"]],
            UT_ID=byte_list[UtmpStruct.UT_ID.value["start_byte"]:UtmpStruct.UT_ID.value["size"]],
            UT_USER=byte_list[UtmpStruct.UT_USER.value["start_byte"]:UtmpStruct.UT_USER.value["size"]],
            UT_HOST=byte_list[UtmpStruct.UT_HOST.value["start_byte"]:UtmpStruct.UT_HOST.value["size"]],
            UT_EXIT=byte_list[UtmpStruct.UT_EXIT.value["start_byte"]:UtmpStruct.UT_EXIT.value["size"]],
            UT_SESSION=byte_list[UtmpStruct.UT_SESSION.value["start_byte"]:UtmpStruct.UT_SESSION.value["size"]],
            UT_TV=byte_list[UtmpStruct.UT_TV.value["start_byte"]:UtmpStruct.UT_TV.value["size"]],
            UT_ADDR_V6=byte_list[UtmpStruct.UT_ADDR_V6.value["start_byte"]:UtmpStruct.UT_ADDR_V6.value["size"]],
        )
        utmp_data.append(block)

    return utmp_data

def parse_user(utmp_block: UtmpBlock) -> str:
    """Parse usernames from `UtmpBlock`

    This function will ignore: {`reboot`, `LOGIN`, `runlevel`}

    Parameters
    ----------
    utmp_block : UtmpBlock
        utmp blocks.

    Returns
    -------
    str
        username of that user, if it's null returns `None`
    """
    user_bytes = utmp_block.UT_USER

    user_bytes = [chr(byte) for byte in user_bytes]
    user = "".join(user_bytes)
    user = user.replace("\x00", "") #remove `NULL` characters

    return user if not(user in IGNORE_UTMP_RESERVED) else None


if __name__ == "__main__":
    parser = ArgumentParser("pusers", usage=USAGE, description=DESC)
    parser.add_argument(
        "-f",
        "--file",
        action="store",
        dest="filepath",
        default=DEFAULT_UTMP_PATH,
    )

    args = parser.parse_args()

    utmp_file = read_utmp(args.filepath)
    utmp_blocks = parse_utmp(utmp_file)

    for block in utmp_blocks:
        user = parse_user(block)
        if user:
            print(user)