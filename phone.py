"""
    Phone Class Starter Code

    This code defines the basic functionality that you need from a phone.
    When these functions are called they should communicate with the
    switchboards to find a path
"""
connected_phones={}
switch_board={}


class Phone:
    def __init__(self, number, switchboard):
        """
        :param number: the phone number without area code
        :param switchboard: the switchboard to which the number is attached.
        """
        self.number = number
        self.switchboard = switchboard
        switch_board[switchboard].append(number)
        # you will need more parameters/attributes

    def connect(self, area_code, other_phone_number):
        """
        :param area_code: the area code of the other phone number
        :param other_phone_number: the other phone number without the area code
        :return: **this you must decide in your implementation**
        """
        if area_code not in switch_board:
            return "This Area Code does not exists !"
        elif other_phone_number in connected_phones:
            return "Required number is busy with someone else ! Try again after some time."
        elif other_phone_number not in switch_board[area_code]:
            return "This phone number does not exists !"
        else:
            connected_phones[self.number]=other_phone_number
            connected_phones[other_phone_number]=self.number
            return "Phones connected successfully !"

    def disconnect(self):
        """
        This function should return the connection status to disconnected.  You need
        to use new members of this class to determine how the phone is connected to
        the other phone.

        You should also make sure to disconnect the other phone on the other end of the line.
        :return: **depends on your implementation**
        """
        if self.number not in connected_phones:
            return "Phone is not in a Call, Already disconnected !"
        else:
            other_phone = connected_phones[self.number]
            del connected_phones[self.number]
            del connected_phones[other_phone]
            return "Phone is disconnected successfully !"

