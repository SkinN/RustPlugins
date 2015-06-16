DEV = True
LATEST_CFG = 0.1
LINE = '-'*50

class rok:

    def __init__(self):

        self.Title = 'Reign Of Kings'
        self.Author = 'SkinN'
        self.Version = V(0, 0, 1)
        #self.ResourceId = 0

    def LoadDefaultConfig(self):

        self.Config = {
            'CONFIG_VERSION': LATEST_CFG,
            'SETTINGS': {
                'PREFIX': 'ROK',
                'BROADCAST TO CONSOLE': True,
                'KING TAG': '<#663399>[ <#7B68EE>KING<end> ]<end>'
            },
            'MESSAGES': {
                'CHECK CONSOLE NOTE': 'Check the console (press F1) for more info.',
                'KING NO MORE': 'You have lost your throne! You no longer are the <red>King<end>!'
            },
            'COLORS': {
                'PREFIX': 'orange',
                'MESSAGES': '#B0C4DE'
            },
            'COMMANDS': {
            }
        }

        self.console('* Loading default configuration file', True)

    def UpdateConfig(self):

        if self.Config['CONFIG_VERSION'] <= LATEST_CFG - 0.2 or DEV:

            self.console('* Configuration file is too old, replacing to default file (Current: v%s / Latest: v%s)' % (self.Config['CONFIG_VERSION'], LATEST_CFG), True)

            self.Config.clear()

            self.LoadDefaultConfig()

        else:

            self.console('* Applying new changes to configuration file (Version: %s)' % LATEST_CFG, True)

            self.Config['CONFIG_VERSION'] = LATEST_CFG

        self.SaveConfig()

    # - MESSAGE SYSTEM

    def console(self, text, force=False):

        if self.Config['SETTINGS']['BROADCAST TO CONSOLE'] or force:

            print('[%s v%s] :: %s' % (self.Title, str(self.Version), self._format(text, True)))

    def pconsole(self, player, text, color='white'):

        player.SendConsoleCommand(self._format('echo <%s>%s<end>' % (color, text)))

    def say(self, text, color='white', force=True, userid=0):

        if self.prefix and force:

            rust.BroadcastChat(self._format('<yellow>[ %s ]<end> <%s>%s<end>' % (self.prefix, color, text)), None, str(userid))

        else:

            rust.BroadcastChat(self._format('<%s>%s<end>' % (color, text)), None, str(userid))

        self.console(self._format(text, True))


    def tell(self, player, text, color='white', force=True, userid=0):

        if self.prefix and force:

            rust.SendChatMessage(player, self._format('<yellow>[ %s ]<end> <%s>%s<end>' % (self.prefix, color, text)), None, str(userid))

        else:

            rust.SendChatMessage(player, self._format('<%s>%s<end>' % (color, text)), None, str(userid))

    def _format(self, text, con=False):

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

    # - SERVER HOOKS

    def Init(self):

        self.console('Loading Plugin')
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
        self.db = data.GetData('rok_db')

        if not self.db:

            self.console('* Setting up the database')

            self.db = {
                'KING': None,
                'KINGSMEN': [],
                'SINCE': 0.000
            }

        else: self.console('* Loading the database')

        # Plugin Commands
        for cmd in CMDS:

            if PLUGIN['ENABLE %s CMD']:

                command.AddChatCommand(CMDS[cmd], self.Plugin, '%s_CMD' % cmd.replace(' ', '_').lower())

        self.console('* Enabling commands:')

        if CMDS:

            for cmd in CMDS:

                self.console('  - /%s (%s)' % (CMDS[cmd], cmd.title()))

        else: self.console('  - No commands enabled')

        self.console(LINE)

    def Unload(self):

        # Save Database
        data.SaveData('rok_db')

    def OnEntityDeath(self, victim, hitinfo):

        if victim and victim.IsPlayer() and hitinfo:

            # Player Ids
            vic_id = self.playerid(victim)
            att_id = self.playerid(hitinfo.Initiator)

            # Hello World





