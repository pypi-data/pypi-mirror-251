from enum import Enum

class SystemMessageOpcode(Enum):
    OK                          = 0
    OPEN_CONNECTION_FAIL        = 1
    CLOSE_CONNECTION_REQUEST    = 2
    INVALID_CALLBACK_SIGNATURE  = 3
    UNEXPECTED_DISCONNECTION    = 4
    # TODO: Add as many system message opcodes as needed.

class SystemMessage:
    '''
    This class represent a system message.
    '''
    def __init__(self, opcode: SystemMessageOpcode, message: str) -> None:
        self.opcode = opcode
        self.message = message
    
    def toDictionary(self) -> dict:
        return {
            "type" : "system_message",
            "code" : self.opcode.name,
            "message" : self.message
        }

    def __str__(self) -> str:
        return str(self.toDictionary())
