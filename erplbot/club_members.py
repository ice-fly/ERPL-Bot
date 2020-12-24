from erplbot.sheets import retrieve_credentials, GoogleSheets

class Name:
    """
    Represents a person's name. First and Last
    """
    def __init__(self, first=None, last=None):
        """
        Creates a new Name instance with the optional values
        """
        self.first = first
        self.last = last

    @staticmethod
    def from_str(s):
        """
        Creates a new Name object from the given string.
        Will only populate the first name if that is the only one given
        """
        name = Name()

        # Split the string by spaces
        name_split = s.split(' ')
        
        name.first = name_split[0]

        # If their name has more than one word, like a name, store that too
        if len(name_split) > 1:
            name.last = name_split[1]
        
        return name
    
    def __eq__(self, other):
        """
        Overrides the == operator for this type
        """
        return self.first == other.first and self.last == other.last
    
    def __repr__(self):
        """
        The internal function called by Python when trying to print this type
        """
        return f'{self.first} {self.last}'

class ClubMember:
    """
    Represents one member of ERPL who has been documented on the Google Sheets
    """
    def __init__(self,
                row = -1,
                number = 0,
                status = None,
                date_submitted = None,
                order_summary = None,
                name = None,
                email = None,
                option = None,
                in_server = False):
        """
        Creates a new instance of ClubMember.
        """
        self.row = row
        self.number = number
        self.status = status
        self.date_submitted = date_submitted
        self.order_summary = order_summary
        self.name = name
        self.email = email
        self.option = option
        self.in_server = in_server
    
    @staticmethod
    def from_list(member_list, row = -1):
        """
        Creates a new ClubMember instance from a list.
        Also set's this member's row to the row provided, default -1.

        The list's indexes must contain data as follows:
        0           Member #
        1           Status
        2           Date Submitted
        3           Order Summary
        4           Name
        5           Email
        6           Option
        7           In Server
        """
        # Create a completely unpopulated ClubMember so everything is default
        club_member = ClubMember()

        club_member.row = row

        # We will put this in a try-expect because we need to handle the case
        # that possibly none of these are actually present in the list
        try:
            # Create an iterator so we don't have to hardcode any indices
            list_iter = iter(member_list)

            # Populate all of the fields in order
            club_member.number = next(list_iter)
            club_member.status = next(list_iter)
            club_member.date_submitted = next(list_iter)
            club_member.order_summary = next(list_iter)

            first_name = next(list_iter)
            last_name = next(list_iter)

            # Create a new name object
            club_member.name = Name(first=first_name,last=last_name)
            club_member.email = next(list_iter)
            club_member.option = next(list_iter)
            club_member.in_server = next(list_iter)

        # If we reached the end of the list before we were meant to
        except StopIteration:
            # Everything should be fine, if the last column wasn't filled in, then it is false
            # We should check if any field other than the last one is empty though
            if club_member.option is None:
                # Then print an error message
                print('Created member lacks 2 or more values')
        
        # If we have reached the end, then return the new club member
        return club_member
    
    def update_in_server(self, google_sheets: GoogleSheets, sheetId: str, col: str, in_server: bool):
        """
        Sets this member's in_server parameter to the value given
        Also updates this member in the Google Sheet provided
        """

        # Update this member's in_server value
        self.in_server = in_server

        # Check if this member was actually fetched from the spreadsheet or not, or if it has a valid row
        if self.row == -1:
            print(f'Tried to update member {self.name} in spreadsheet, but member has no valid row.')
        else:
            # If it does have a valid row
            # This 'range' is just one single cell that represents if this member is in the server or not
            value_range = f'{col}{self.row}:{col}{self.row}'
            # The new value should be a stringr
            new_value = 'true' if in_server else 'false'
            # We need to do this because this is one row, and one column
            values = [ [ new_value ] ]
            # Set the value in the sheet finally
            google_sheets.set_values(sheetId, value_range, values)

def get_members_from_spreadsheet(google_sheets, sheetId, value_range):
    """
    Retrieves a list of members from the provided Google Sheet
    """
    # Gather all values from the google sheet
    rows = google_sheets.get_values(sheetId, value_range)

    members = []

    # Loop through each row
    for (index, row) in enumerate(rows):
        # Try to turn each one into a member
        # The row is index+2 because we start at the second row
        member = ClubMember.from_list(row, row= index+2 )
        # Append it
        members.append(member)
    
    return members