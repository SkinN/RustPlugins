import re
import time
import BasePlayer

DEV = False
LATEST_CFG = 0.1
LINE = '-'*50
PROFILE = '76561198203401038'

class overthrone:

    def __init__(self):

        self.Title = 'OverThrone'
        self.Author = 'SkinN & OMNI-Hollow'
        self.Version = V(0, 0, 1)
        #self.ResourceId=0

    # -------------------------------------------------------------------------
    # - CONFIGURATION / DATABASE SYSTEM
    def LoadDefaultConfig(self):
        ''' Hook called when there is no configuration file '''

        self.Config = {
            'CONFIG_VERSION': LATEST_CFG,
            'SETTINGS': {
                'BROADCAST TO CONSOLE': True,
                'PREFIX': '<#9B7E7A>Over<end><#CA1F0C>Throne<end>',
                'ENABLE KING CMD': True
            },
            'MESSAGES': {
                'FIRST KING': 'This land had no King until today, <#901BD4>{king}<end> is now the King of the land!',
                'ANNOUNCE NEW KING': 'Sir <red>{attacker}<end> killed King <cyan>{lastking}<end> and is now our new King, all hail the new King!',
                'TELL KINGSHIP LOST': 'You were killed by <red>{attacker}<end> and lost your throne. You are no longer King of the land!',
                'NOTIFY KINGSHIP LOSS': 'While away you were killed by <red>{attacker}<end> and lost the throne. The current king is <#901BD4>{king}<end>.',
                'YOU ARE KING': 'You are the King of the land, since <lime>{time}H<end> ago.',
                'WHO IS KING': 'The land is ruled by King <#901BD4>{king}<end>, since <lime>{time}H<end> ago.',
                'NO KING YET': 'No one is ruling the land yet. Kill someone to be the first to claim the land!'
            },
            'COMMANDS': {
                'KING': 'king'
            },
            'COLORS': {
                'PREFIX': '#CECECE',
                'SYSTEM': '#CECECE'
            }
        }

        self.con('* Setting up default configuration file')

    # -------------------------------------------------------------------------
    def UpdateConfig(self):
        ''' Function to update the configuration file on plugin Init '''

        if self.Config['CONFIG_VERSION'] <= LATEST_CFG - 0.2 or DEV:

            self.con('* Configuration version is too old, resetting to default')

            self.Config.clear()

            self.LoadDefaultConfig()

        else:

            self.Config['CONFIG_VERSION'] = LATEST_CFG

        self.SaveConfig()

    # -------------------------------------------------------------------------
    def Save(self):
        ''' Function to save the plugin database '''

        data.SaveData(self.dbname)

        self.con('Saving Database')

    # -------------------------------------------------------------------------
    # - MESSAGE SYSTEM
    def con(self, text, f=False):
        ''' Function to send a server console message '''

        if self.Config['SETTINGS']['BROADCAST TO CONSOLE'] or f:

            print('[%s v%s] :: %s' % (self.Title, str(self.Version), self.format(text, True)))

    # -------------------------------------------------------------------------
    def say(self, text, color='white', f=True, profile=PROFILE):
        ''' Function to send a message to all players '''

        if self.prefix and f:

            rust.BroadcastChat(self.format('[ %s ] <%s>%s<end>' % (self.prefix, color, text)), None, str(profile))

        else:

            rust.BroadcastChat(self.format('<%s>%s<end>' % (color, text)), None, str(profile))

        self.con(text)

    # -------------------------------------------------------------------------
    def tell(self, player, text, color='white', f=True, profile=PROFILE):
        ''' Function to send a message to a player '''

        if self.prefix and f:

            rust.SendChatMessage(player, self.format('[ %s ] <%s>%s<end>' % (self.prefix, color, text)), None, str(profile))

        else:

            rust.SendChatMessage(player, self.format('<%s>%s<end>' % (color, text)), None, str(profile))

    # -------------------------------------------------------------------------
    def format(self, text, con=False):
        '''
            * Notifier's color format system
            ---
            Replaces color names and RGB hex code into HTML format code
        '''

        colors = (
            'red', 'blue', 'green', 'yellow', 'white', 'black', 'cyan',
            'lightblue', 'lime', 'purple', 'darkblue', 'magenta', 'brown',
            'orange', 'olive', 'gray', 'grey', 'silver', 'maroon'
        )

        name = r'\<(\w+)\>'
        hexcode = r'\<(#\w+)\>'
        end = '<end>'

        if con:
            for x in (end, name, hexcode):
                for c in re.findall(x, text):
                    if c.startswith('#') or c in colors:
                        text = re.sub(x, '', text)
        else:
            text = text.replace(end, '</color>')
            for f in (name, hexcode):
                for c in re.findall(f, text):
                    if c.startswith('#') or c in colors: text = text.replace('<%s>' % c, '<color=%s>' % c)
        return text

    # -------------------------------------------------------------------------
    # - SERVER / PLUGIN HOOKS
    def Unload(self):
        ''' Hook called on plugin unload '''

        self.Save()

    # -------------------------------------------------------------------------
    def OnServerSave(self):
        ''' Hook called when server data is saved '''

        self.Save()

    # -------------------------------------------------------------------------
    def Init(self):
        ''' Hook called when the plugin initializes '''

        self.con(LINE)

        # Update Config File
        if self.Config['CONFIG_VERSION'] < LATEST_CFG or DEV:

            self.UpdateConfig()

        else:

            self.con('* Configuration file is up to date')

        # Global / Class Variables
        global MSG, PLUGIN, COLOR, STRINGS
        MSG, COLOR, PLUGIN, CMDS = [self.Config[x] for x in ('MESSAGES', 'COLORS', 'SETTINGS', 'COMMANDS')]

        self.prefix = '<%s>%s<end>' % (COLOR['PREFIX'], PLUGIN['PREFIX']) if PLUGIN['PREFIX'] else None
        self.dbname = 'overthrone_db'

        # Load Database
        self.db = data.GetData(self.dbname)

        if not self.db:

            self.db['KING'] = False
            self.db['KING_NAME'] = False 
            self.db['KINGSMEN'] = {}
            self.db['QUEUE'] = {}
            self.db['SINCE'] = 0.0

            self.con('* Creating Database')

        else:

            self.con('* Loading Database')

        # Create Plugin Commands
        for cmd in CMDS:

            if PLUGIN['ENABLE %s CMD' % cmd]:

                command.AddChatCommand(CMDS[cmd], self.Plugin, '%s_CMD' % cmd.replace(' ','_').lower())

            else:

                CMDS.remove(cmd)

        self.con('* Enabling commands:')

        if CMDS:

            for cmd in CMDS:

                self.con('  - /%s (%s)' % (CMDS[cmd], cmd.title()))

        else: self.con('  - There are no commands enabled')

        self.con(LINE)

    # -------------------------------------------------------------------------
    # - ENTITY HOOKS
    def OnEntityDeath(self, vic, hitinfo):
        ''' Hook called whenever an entity dies '''

        # Is victim a player and attacker?
        if (not 'corpse' in str(vic) and vic and 'player' in str(vic)) and (hitinfo and hitinfo.Initiator and 'player' in str(hitinfo.Initiator)):

            att = hitinfo.Initiator
            vic_id = self.playerid(vic)
            att_id = self.playerid(att)

            # Check if Victim or Attacker are NPCs
            if any(i < 17 for i in (vic_id, att_id)): return

            # Is there any King?
            if self.db['KING']:

                # Check if victim is not the attacker and is the actual King
                if vic_id != att_id and vic_id == self.db['KING']:

                    # Last King timestamp
                    since = self.db['SINCE']

                    # Replace King
                    self.db['KING'] = att_id
                    self.db['SINCE'] = time.time()
                    self.db['KINGSMEN'].clear()

                    # Announce new King to the server
                    self.say(MSG['ANNOUNCE NEW KING'].format(attacker=att.displayName, lastking=vic.displayName), COLOR['SYSTEM'])

                    # Is victim connected?
                    if vic.IsConnected():

                        self.tell(vic, MSG['TELL KINGSHIP LOST'].format(attacker=att.displayName), COLOR['SYSTEM'])

                    # Otherwise add victim to queue for later notification
                    else:

                        self.db['QUEUE'][vic_id] = att.displayName

            # Otherwise name the first King
            else:

                self.db['KING'] = att_id
                self.db['KINGSMEN'].clear()
                self.db['SINCE'] = time.time()

                self.tell(att, MSG['FIRST KING'].format(king=att.displayName), COLOR['SYSTEM'])

    # -------------------------------------------------------------------------
    # - PLAYER HOOKS
    def OnPlayerInit(self, player):
        ''' Hook called when the player has fully connected '''

        # If Kingship has been taken from the player while he was offline
        # inform the player of the event telling the attacker who took the place
        uid = self.playerid(player)

        if uid in self.db['QUEUE']:

            att = self.db['QUEUE'][uid]
            king = self.find(self.db['KING'])

            self.tell(player, MSG['NOTIFY KINGSHIP LOSS'].format(attacker=att, king=king.displayName), COLOR['SYSTEM'])

            del self.db['QUEUE'][uid]

    #--------------------------------------------------------------------------
    # - PLUGIN FUNTIONS
    def get_time(self, stamp):
        ''' Returns exact hours, minutes and seconds from a timestamp '''

        m, s = divmod(time.time() - stamp, 60)
        h, m = divmod(m, 60)

        return '%02d:%02d' % (h, m)

    # -------------------------------------------------------------------------
    def playerid(self, player):
        ''' Function to return the player UserID '''

        return rust.UserIDFromPlayer(player)

    # -------------------------------------------------------------------------
    def find(self, uid):
        ''' Function to find the BasePlayer of a player whether is On or Off '''

        ply = BasePlayer.Find(uid)

        if not ply:

            for i in BasePlayer.sleepingPlayerList:

                if self.playerid(i) == uid:

                    ply = i

        return ply

    #--------------------------------------------------------------------------
    # - COMMAND BLOCKS
    def king_CMD(self, player, cmd, args):
        ''' Command that tells who is the current King '''

        uid = self.playerid(player)

        if self.db['KING']:

            since = self.get_time(self.db['SINCE'])

            if uid == self.db['KING']:

                self.tell(player, MSG['YOU ARE KING'].format(time=since), COLOR['SYSTEM'])

            else:

                king = self.find(self.db['KING'])

                self.tell(player, MSG['WHO IS KING'].format(time=since, king=king.displayName), COLOR['SYSTEM'])

        else:

            self.tell(player, MSG['NO KING YET'], COLOR['SYSTEM'])

    # -------------------------------------------------------------------------