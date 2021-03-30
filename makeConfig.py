import pickle
# The bot's Discord Bot token
BOT_TOKEN = 'ODAzNDU4NzQ2NDUzNDU4OTc0.YA-FRA.qdTDgnZnHScNmKTTKZyBMdroEwk'

# The ID of the spreadsheet that contains all of ERPL's current members
SPREADSHEET_ID = '1U9mnzy_PBXcv_LMXtQNfi9LvNrUTx_n9Lz9N1D-BRaA'

# These specify when the member's data in the spreadsheet starts and ends
SHEET_NAME = 'Sheet1!'
RANGE_START = 'A2'
RANGE_END = 'D'

# This is Discord's ID that means the "Member" role
MEMBER_ROLE_ID = 805952653162709053
RECRUIT_ROLE_ID = 805952689452089384
OFFICER_ROLE_ID = 821146675556778044
PROJECT_LEAD_ID = 821145519564521522

#Use Pickle to write config.bin
with open('config.bin', 'wb') as fh:
    pickle.dump([BOT_TOKEN, SPREADSHEET_ID, SHEET_NAME, RANGE_START, RANGE_END, MEMBER_ROLE_ID, OFFICER_ROLE_ID, PROJECT_LEAD_ID, RECRUIT_ROLE_ID], fh)
exit

