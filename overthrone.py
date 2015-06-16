HELLO WORLD

import re
import time
import BasePlayer

DEV = True
LATEST_CFG = 0.1
LINE = '-'*50

class overthrone:

    def __init__(self):

        self.Title = 'OverThrone'
        self.Author = 'SkinN & OMNI-Hollow'
        self.Version = V(0, 0, 1)
        #self.ResourceId = 0

    # -------------------------------------------------------------------------
    def LoadDefaultConfig(self):asa
        ''' Hook called when there is no configuration file '''

        self.Config = {
            'CONFIG_VERSION': LATEST_CFG,
            'SETTINGS': {
                'PREFIX': 'OverThrone',
                'BROADCAST TO CONSOLE': True,
                'KING TAG': '<#663399>[ <#7B68EE>KING<end> ]<end>',
                'ENABLE KING CMD': True
            },
            'MESSAGES': {
                'CHECK CONSOLE NOTE': 'Check the console (press F1) for more info.',
                'KING NO MORE': 'You have lost your throne! You no longer are the <red>King<end>!',
                'NO LONGER KING': 'You were killed by <red>{attacker}<end>, you are no longer the King. <#7B68EE>{king}<end> is the current King.',
                'NEW KING': '<#7B68EE>{attacker}<end> has killed King <lime>{lastking}<end>, <#7B68EE>{attacker}<end> is now the new King. All hail the King!',
                'FIRST KING': '<#7B68EE>{king}<end> is our first King. All hail the King!',
                'CURRENT KING': '<#7B68EE>{king}<end> is your King.',
                'YOU ARE KING': 'You are the King.'
            },
            'COLORS': {
                'PREFIX': 'orange',
                'SYSTEM': '#B0C4DE'
            },
            'COMMANDS': {
                'KING': 'king'
            }
        }

        self.console('* Loading default configuration file', True)

    # -------------------------------------------------------------------------
    def UpdateConfig(self):
        ''' Function to update the configuration file on plugin Init '''

        if self.Config['CONFIG_VERSION'] <= LATEST_CFG - 0.2 or DEV:

            self.console('* Configuration file is too old, replacing to default file (Current: v%s / Latest: v%s)' % (self.Config['CONFIG_VERSION'], LATEST_CFG), True)

            self.Config.clear()

            self.LoadDefaultConfig()

        else:

            self.console('* Applying new changes to configuration file (Version: %s)' % LATEST_CFG, True)

            self.Config['CONFIG_VERSION'] = LATEST_CFG

        self.SaveConfig()

    # -------------------------------------------------------------------------
    def Save(self):
        ''' Function to save the plugin database '''

        data.SaveData(self.dbname)

        self.console('Saving Database')

    # -------------------------------------------------------------------------
    # - MESSAGE SYSTEM
    def console(self, text, force=False):
        ''' Function to send a server console message '''

        if self.Config['SETTINGS']['BROADCAST TO CONSOLE'] or force:

            print('[%s v%s] :: %s' % (self.Title, str(self.Version), self._format(text, True)))

    # -------------------------------------------------------------------------
    def pconsole(self, player, text, color='white'):
        ''' Function to send a message to a player console '''

        player.SendConsoleCommand(self._format('echo <%s>%s<end>' % (color, text)))

    # -------------------------------------------------------------------------
    def say(self, text, color='white', force=True, userid=0):
        ''' Function to send a message to all players '''

        if self.prefix and force:

            rust.BroadcastChat(self._format('<yellow>[ %s ]<end> <%s>%s<end>' % (self.prefix, color, text)), None, str(userid))

        else:

            rust.BroadcastChat(self._format('<%s>%s<end>' % (color, text)), None, str(userid))

        self.console(self._format(text, True))


    # -------------------------------------------------------------------------
    def tell(self, player, text, color='white', force=True, userid=0):
        ''' Function to send a message to a player '''

        if self.prefix and force:

            rust.SendChatMessage(player, self._format('<yellow>[ %s ]<end> <%s>%s<end>' % (self.prefix, color, text)), None, str(userid))

        else:

            rust.SendChatMessage(player, self._format('<%s>%s<end>' % (color, text)), None, str(userid))

    # -------------------------------------------------------------------------
    def _format(self, text, con=False):
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
                if x.startswith('#') or x in colors:
                    text = re.sub(x, '', text)
        else:
            text = text.replace(end, '</color>')
            for f in (name, hexcode):
                for c in re.findall(f, text):
                    if c.startswith('#') or c in colors:
                        text = text.replace('<%s>' % c, '<color=%s>' % c)
        return text

    # -------------------------------------------------------------------------
    # - SERVER HOOKS
    def Init(self):
        ''' Hook called on plugin initialized '''

        self.console(LINE)

        # Configuration Update
        if self.Config['CONFIG_VERSION'] < LATEST_CFG or DEV:

            self.UpdateConfig()

        # Plugin Specific
        global MSG, PLUGIN, COLOR, CMDS
        MSG, COLOR, PLUGIN, CMDS = [self.Config[x] for x in ('MESSAGES','COLORS','SETTINGS','COMMANDS')]

        if PLUGIN['PREFIX']:
            self.prefix = '<%s>%s<end>' % (COLOR['PREFIX'], PLUGIN['PREFIX'])
        else:
            self.prefix = None

        # Load Database
        self.dbname = 'rok_db'
        self.db = data.GetData(self.dbname)

        if not self.db:
            self.db['KING'] = {}
            self.db['KINGSMEN'] = {}
            self.db['QUEUE'] = {}
            self.db['SINCE'] = 0.0

        # Plugin Commands
        for cmd in CMDS:

            if PLUGIN['ENABLE %s CMD' % cmd]:

                command.AddChatCommand(CMDS[cmd], self.Plugin, '%s_CMD' % cmd.replace(' ', '_').lower())

        self.console('* Enabling commands:')

        if CMDS:

            for cmd in CMDS:

                self.console('  - /%s (%s)' % (CMDS[cmd], cmd.title()))

        else: self.console('  - No commands enabled')

        self.console(LINE)

    # -------------------------------------------------------------------------
    def Unload(self):
        ''' Hook called on plugin unload '''

        self.Save()

    # -------------------------------------------------------------------------
    def OnServerSave(self):
        ''' Hook called on server save '''

        self.Save()

    # -------------------------------------------------------------------------
    # - ENTITY HOOKS
    def OnEntityDeath(self, vic, hitinfo):
        ''' Hook called whenever an entity dies '''

        # If victim and attacker both players?
        if 'corpse' not in str(vic) and (vic and 'player' in str(vic)) and (hitinfo and hitinfo.Initiator and 'player' in str(hitinfo.Initiator)):

            att = hitinfo.Initiator

            # Player Ids
            vic_id = self.playerid(vic)
            att_id = self.playerid(hitinfo.Initiator)

            # Check if attacker is not a NPC
            if len(str(att.userID)) == 17:

                # Is there a King?
                if self.db['KING']:

                    # Return if it's a self death and victim is not the King
                    if vic_id == att_id and db['KING'] != vic_id: return

                    since = self.get_time(self.db['SINCE'])

                    self.db['SINCE'] = time.time()
                    self.db['KING'] = att_id
                    self.db['KINGSMEN'].clear()

                    if not vic.IsConnected():

                        self.db['QUEUE'][vic_id] = att.displayName

                    self.say(MSG['NEW KING'].format(attacker=att.displayName, lastking=vic.displayName), COLOR['SYSTEM'])

                else:

                    self.db['SINCE'] = time.time()
                    self.db['KING'] = att_id
                    self.db['KINGSMEN'].clear()

                    self.say(MSG['FIRST KING'].format(king=att.displayName), COLOR['SYSTEM'])

    # -------------------------------------------------------------------------
    # - PLAYER HOOKS
    def OnPlayerInit(self, player):
        ''' Hook called when a player initiates in the server '''

        # Check if there is a message queued for the player
        uid = self.playerid(player)

        self.msg_queue(uid)

    # -------------------------------------------------------------------------
    # - FUNCTIONS
    def playerid(self, player):
        ''' Returns UID of the player '''

        return rust.UserIDFromPlayer(player)

    # -------------------------------------------------------------------------
    def get_time(self, stamp):
        ''' Returns exact hours, minutes and seconds from a time stamp '''

        m, s = divmod(stamp - time.time(), 60)
        h, m = divmod(m, 60)

        return '%d:%02d:%02d' % (h, m, s)

    # -------------------------------------------------------------------------
    def msg_queue(self, uid):
        '''
            Checks whether the player is queued to know he is no longer king,
            telling who killed him and who is the current king
        '''

        if uid in self.db['QUEUE']:

            player = BasePlayer.Find(uid)

            att = self.db['QUEUE'][uid]
            king = BasePlayer.Find(self.db['KING'])

            self.tell(player, MSG['NO LONGER KING'].format(attacker=att, king=king.displayName))

            del self.db['QUEUE'][uid]

    # -------------------------------------------------------------------------
    # - COMMANDS
    def king_CMD(self, player, cmd, args):

        uid = player.userID
        king = self.db['KING']

        if uid == int(king):

            self.tell(player, MSG['YOU ARE KING'], COLOR['SYSTEM'])

        else:

            king = BasePlayer.Find(king)

            self.tell(player, MSG['CURRENT KING'].format(king=king.displayName), COLOR['SYSTEM'], king)