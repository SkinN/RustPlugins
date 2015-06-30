import re
import time
import BasePlayer
import ConVar.Server as sv
import UnityEngine.Random as random
from System import Action, Int32, String

DEV = False
LATEST_CFG = 4.0
LINE = '-' * 50
PROFILE = '76561198235146288'

class notifier:

    def __init__(self):

        self.Title = 'Notifier'
        self.Version = V(2, 8, 1)
        self.Author = 'SkinN'
        self.Description = 'Broadcasts chat messages as notifications and advertising.'
        self.ResourceId = 797

    # -------------------------------------------------------------------------
    # - CONFIGURATION / DATABASE SYSTEM
    def LoadDefaultConfig(self):
        ''' Hook called when there is no configuration file '''

        self.Config = {
            'CONFIG_VERSION': LATEST_CFG,
            'SETTINGS': {
                'PREFIX': 'NOTIFIER',
                'BROADCAST TO CONSOLE': True,
                'RULES LANGUAGE': 'AUTO',
                'HIDE ADMINS': False,
                'PLAYERS LIST ON CHAT': True,
                'PLAYERS LIST ON CONSOLE': True,
                'ADVERTS INTERVAL': 5,
                'ENABLE JOIN MESSAGE': True,
                'ENABLE LEAVE MESSAGE': True,
                'ENABLE WELCOME MESSAGE': True,
                'ENABLE ADVERTS': True,
                'ENABLE PLAYERS LIST': True,
                'ENABLE ADMINS LIST': False,
                'ENABLE PLUGINS LIST': False,
                'ENABLE RULES': True,
                'ENABLE SERVER MAP': True
            },
            'MESSAGES': {
                'JOIN MESSAGE': '{user} joined the server, from <lime>{country}<end>.',
                'LEAVE MESSAGE': '{user} left the server.',
                'CHECK CONSOLE': 'Check the console (press F1) for more info.',
                'PLAYERS ONLINE': 'There are <lime>{active}<end> players online.',
                'PLAYERS STATS': '<orange>SLEEPERS: <lime>{sleepers}<end> ALLTIME PLAYERS: <lime>{alltime}<end><end>',
                'SERVER MAP': 'See where you are on the server map at: <lime>http://{ip}:{port}<end>',
                'NO RULES': 'Error, no rules found, contact the Admins.',
                'NO LANG': 'Error, <lime>{args}<end> language not supported or does not exist.',
                'NO ADMINS': 'There are no Admins online.',
                'ADMINS LIST TITLE': 'ADMINS ONLINE',
                'PLUGINS LIST TITLE': 'SERVER PLUGINS',
                'PLAYERS LIST TITLE': 'PLAYERS ONLINE',
                'RULES TITLE': 'SERVER RULES',
                'PLAYERS LIST DESC': '<orange>/players<end> <grey>-<end> List of all players in the server.',
                'ADMINS LIST DESC': '<orange>/admins<end> <grey>-<end> List of online <cyan>Admins<end> in the server.',
                'PLUGINS LIST DESC': '<orange>/plugins<end> <grey>-<end> List of plugins installed in the server.',
                'RULES DESC': '<orange>/rules<end> <grey>-<end> List of server rules.',
                'SERVER MAP DESC': '<orange>/map<end> <grey>-<end> Server map url.'
            },
            'WELCOME MESSAGE': (
                '<size=17>Welcome {player}!</size>',
                '<grey><size=20>•</size><end> Type <orange>/help<end> for all available commands.',
                '<grey><size=20>•</size><end> Check our server <orange>/rules<end>.',
                '<grey><size=20>•</size><end> See where you are on the server map at: <lime>http://{ip}:{port}<end>'
            ),
            'ADVERTS': (
                'Want to know the available commands? Type <orange>/help<end>.',
                'Respect the server <orange>/rules<end>.',
                'This server is running <orange>Oxide 2<end>.',
                '<red>Cheat is strictly prohibited.<end>',
                'Type <orange>/map<end> for the server map link.',
                '<orange>Players Online: <lime>{players}<end> / <lime>{maxplayers}<end> Sleepers: <lime>{sleepers}<end><end>'
            ),
            'COLORS': {
                'PREFIX': '#00EEEE',
                'JOIN MESSAGE': '#BEBEBE',
                'LEAVE MESSAGE': '#BEBEBE',
                'WELCOME MESSAGE': 'white',
                'ADVERTS': '#BEBEBE',
                'SYSTEM': 'white'
            },
            'COMMANDS': {
                'PLAYERS LIST': 'players',
                'RULES': ('rules', 'regras', 'regles'),
                'PLUGINS LIST': 'plugins',
                'ADMINS LIST': 'admins',
                'SERVER MAP': 'map'
            },
            'RULES': {
                'EN': (
                    'Cheating is strictly prohibited.',
                    'Respect all players',
                    'Avoid spam in chat.',
                    'Play fair and don\'t abuse of bugs/exploits.'
                ),
                'PT': (
                    'Usar cheats e totalmente proibido.',
                    'Respeita todos os jogadores.',
                    'Evita spam no chat.',
                    'Nao abuses de bugs ou exploits.'
                ),
                'FR': (
                    'Tricher est strictement interdit.',
                    'Respectez tous les joueurs.',
                    'Évitez le spam dans le chat.',
                    'Jouer juste et ne pas abuser des bugs / exploits.'
                ),
                'ES': (
                    'Los trucos están terminantemente prohibidos.',
                    'Respeta a todos los jugadores.',
                    'Evita el Spam en el chat.',
                    'Juega limpio y no abuses de bugs/exploits.'
                ),
                'DE': (
                    'Cheaten ist verboten!',
                    'Respektiere alle Spieler',
                    'Spam im Chat zu vermeiden.',
                    'Spiel fair und missbrauche keine Bugs oder Exploits.'
                ),
                'TR': (
                    'Hile kesinlikle yasaktır.',
                    'Tüm oyuncular Saygı.',
                    'Sohbet Spam kaçının.',
                    'Adil oynayın ve böcek / açıkları kötüye yok.'
                ),
                'IT': (
                    'Cheating è severamente proibito.',
                    'Rispettare tutti i giocatori.',
                    'Evitare lo spam in chat.',
                    'Fair Play e non abusare di bug / exploit.'
                ),
                'DK': (
                    'Snyd er strengt forbudt.',
                    'Respekt alle spillere.',
                    'Undgå spam i chatten.',
                    'Play fair og ikke misbruger af bugs / exploits.'
                ),
                'RU': (
                    'Запрещено использовать читы.',
                    'Запрещено спамить и материться.',
                    'Уважайте других игроков.',
                    'Играйте честно и не используйте баги и лазейки.'
                ),
                'NL': (
                    'Vals spelen is ten strengste verboden.',
                    'Respecteer alle spelers',
                    'Vermijd spam in de chat.',
                    'Speel eerlijk en maak geen misbruik van bugs / exploits.'
                ),
                'UA': (
                    'Обман суворо заборонено.',
                    'Поважайте всіх гравців',
                    'Щоб уникнути спаму в чаті.',
                    'Грати чесно і не зловживати помилки / подвиги.'
                )
            }
        }

        self.con('* Loading default configuration file', True)

    # -------------------------------------------------------------------------
    def UpdateConfig(self):
        ''' Function to update the configuration file on plugin Init '''

        if self.Config['CONFIG_VERSION'] <= LATEST_CFG - 0.2 or DEV:

            self.con('* Configuration version is too old, reseting to default')

            adverts = self.Config['ADVERTS']
            rules = self.Config['RULES']
            welcome = self.Config['WELCOME MESSAGE']

            self.Config.clear()

            self.LoadDefaultConfig()

            # Save Adverts and Rules or config reset
            if not DEV:

                self.Config['ADVERTS'] = adverts
                self.Config['RULES'] = rules
                self.Config['WELCOME MESSAGE'] = welcome

        else:

            self.con('* Applying new changes to configuration file')

            self.Config['CONFIG_VERSION'] = LATEST_CFG

        self.SaveConfig()

    # -------------------------------------------------------------------------
    # - MESSAGE SYSTEM
    def con(self, text, f=False):
        ''' Function to send a server con message '''

        if self.Config['SETTINGS']['BROADCAST TO CONSOLE'] or f:

            print('[%s v%s] :: %s' % (self.Title, str(self.Version), self.format(text, True)))

    # --------------------------------------------------------------------------
    def pcon(self, player, text, color='#BEBEBE'):
        ''' Function to send a message to a player console '''

        player.SendConsoleCommand(self.format('echo <%s>%s<end>' % (color, text)))

    # -------------------------------------------------------------------------
    def say(self, text, color='#BEBEBE', f=True, profile=PROFILE):
        ''' Function to send a message to all players '''

        if self.prefix and f:

            rust.BroadcastChat(self.format('[ %s ] <%s>%s<end>' % (self.prefix, color, text)), None, str(profile))

        else:

            rust.BroadcastChat(self.format('<%s>%s<end>' % (color, text)), None, str(profile))

        self.con(self.format(text, True))

    # -------------------------------------------------------------------------
    def tell(self, player, text, color='#BEBEBE', f=True, profile=PROFILE):
        ''' Function to send a message to a player '''

        if self.prefix and f:

            rust.SendChatMessage(player, self.format('[ %s ] <%s>%s<end>' % (self.prefix, color, text)), None, str(profile))

        else:

            rust.SendChatMessage(player, self.format('<%s>%s<end>' % (color, text)), None, str(profile))

    # -------------------------------------------------------------------------
    def log(self, filename, text):
        ''' Logs text into a specific file '''

        filename = 'Notifier - %s - (%s)' % (filename, self.log_date())

        sv.Log('Oxide/Logs/%s.txt' % filename, text)

    # -------------------------------------------------------------------------
    # - PLUGIN HOOKS
    def Init(self):
        ''' Hook called when the plugin initializes '''

        self.con(LINE)

        # Update Config File
        if self.Config['CONFIG_VERSION'] < LATEST_CFG or DEV:

            self.UpdateConfig()

        else:

            self.con('Configuration file is up to date')

        # Global / Class Variables
        global MSG, PLUGIN, COLOR, CMDS, ADVERTS, RULES
        MSG, COLOR, PLUGIN, CMDS, ADVERTS, RULES = [self.Config[x] for x in ('MESSAGES', 'COLORS', 'SETTINGS', 'COMMANDS', 'ADVERTS', 'RULES')]

        self.prefix = '<%s>%s<end>' % (COLOR['PREFIX'], PLUGIN['PREFIX']) if PLUGIN['PREFIX'] else None
        self.p_color = '#6496E1'
        self.a_color = '#ADFF64'
        self.cache = {}
        self.connected = []
        self.lastadvert = 0
        self.cmds = []

        # Countries Data
        self.countries = data.GetData('notifier_countries_db')
        self.countries.update(self.countries_dict())
        data.SaveData('notifier_countries_db')

        # Initiate active players
        for player in self.activelist(): self.OnPlayerInit(player, False)

        # Start Adverts Loop
        if PLUGIN['ENABLE ADVERTS']:

            mins = PLUGIN['ADVERTS INTERVAL']
            secs = mins * 60 if mins else 60

            self.adverts_loop = timer.Repeat(secs, 0, Action(self.send_advert), self.Plugin)

            self.con('* Starting Adverts loop, set to %s minute/s' % mins)

        else:

            self.adverts_loop = None

            self.con('* Adverts are disabled')

        # Create Plugin Commands
        for cmd in CMDS:

            if PLUGIN['ENABLE %s' % cmd]:

                self.cmds.append(cmd)

                if isinstance(CMDS[cmd], tuple):

                    for i in CMDS[cmd]:

                        command.AddChatCommand(i, self.Plugin, '%s_CMD' % cmd.replace(' ','_').lower())

                else:

                    command.AddChatCommand(CMDS[cmd], self.Plugin, '%s_CMD' % cmd.replace(' ','_').lower())

        self.con('* Enabling commands:')

        if self.cmds:

            for cmd in self.cmds:

                if isinstance(CMDS[cmd], tuple):

                    self.con('  - /%s (%s)' % (', /'.join(CMDS[cmd]), cmd.title()))

                else:

                    self.con('  - /%s (%s)' % (CMDS[cmd], cmd.title()))

        else: self.con('  - There are no commands enabled')

        command.AddChatCommand('notifier', self.Plugin, 'plugin_CMD')

        self.con(LINE)

    # --------------------------------------------------------------------------
    def Unload(self):
        ''' Hook called on plugin unload '''

        # Destroy adverts loop
        if self.adverts_loop:

            self.adverts_loop.Destroy()

    # -------------------------------------------------------------------------
    # - PLAYER HOOKS
    def OnPlayerInit(self, player, send=True):

        # Cache player and list him to connected
        self.cache_player(player.net.connection)

        uid = self.playerid(player)

        if uid not in self.connected:

            self.connected.append(uid)

        self.webrequest_filter(player, send)

    # -------------------------------------------------------------------------
    def OnPlayerDisconnected(self, player):
        ''' Hook called when a player disconnects from the server '''

        uid = self.playerid(player)
        ply = self.cache[uid]

        # Is Player connected?
        if uid in self.connected:

            self.connected.remove(uid)

            if PLUGIN['ENABLE LEAVE MESSAGE']:
                
                if not (PLUGIN['HIDE ADMINS'] and int(ply['auth']) > 0):

                    self.say(MSG['LEAVE MESSAGE'].format(user=self.playername(player), **ply), COLOR['LEAVE MESSAGE'], uid)

            # Log disconnect
            self.log('Connections', '{player} disconnected from {country} [UID: {steamid}][IP: {ip}]'.format(**ply))

        # Decache player
        if uid in self.cache: del self.cache[uid]

    # -------------------------------------------------------------------------
    # - COMMAND FUNCTIONS
    def rules_CMD(self, player, cmd, args):
        ''' Rules command function '''

        lang = self.playerlang(player, args[0] if args else None)

        if lang:

            rules = RULES[lang]

            if rules:

                self.tell(player, '%s | %s:' % (self.prefix, MSG['RULES TITLE']), f=False)
                self.tell(player, LINE, f=False)

                if PLUGIN['RULES LANGUAGE'] != 'AUTO':

                    self.tell(player, 'DISPLAYING RULES IN: %s' % self.countries[PLUGIN['RULES LANGUAGE']], COLOR['SYSTEM'], f=False)

                for n, line in enumerate(rules):

                    self.tell(player, '%s. %s' % (n + 1, line), 'orange', f=False)

            else:

                self.tell(player, MSG['NO RULES'], COLOR['white'])

    # -------------------------------------------------------------------------
    def players_list_CMD(self, player, cmd, args):
        ''' Players List command function '''

        active = [i for i in self.activelist() if (not PLUGIN['HIDE ADMINS'] and i.IsAdmin() or player.IsAdmin()) or not i.IsAdmin()]
        sleepers = self.sleeperlist()

        title = '%s | %s:' % (self.prefix, MSG['PLAYERS LIST TITLE'])
        ply_count = MSG['PLAYERS ONLINE'].format(active=str(len(active)))
        ply_stats = MSG['PLAYERS STATS'].format(sleepers=str(len(sleepers)), alltime=str(len(active) + len(sleepers)))

        chat = PLUGIN['PLAYERS LIST ON CHAT']
        cons = PLUGIN['PLAYERS LIST ON CONSOLE']

        # Show list on chat?
        if chat:

            # Divide names in chunks before sending to chat
            names = [self.playername(i) for i in active]
            names = [names[i:i+3] for i in xrange(0, len(names), 3)]

            self.tell(player, title, f=False)
            self.tell(player, LINE, f=False)

            for i in names:
            
                self.tell(player, ', '.join(i), COLOR['SYSTEM'], f=False)
            
            self.tell(player, LINE, f=False)
            self.tell(player, ply_count, COLOR['SYSTEM'], f=False)
            self.tell(player, ply_stats, COLOR['SYSTEM'], f=False)

        if cons:

            self.tell(player, '(%s)' % MSG['CHECK CONSOLE'], 'orange', f=False)

            self.pcon(player, LINE)
            self.pcon(player, title)
            self.pcon(player, LINE)

            inv = {v: k for k, v in self.countries.items()}

            for n, ply in enumerate(active):

                i = self.cache[self.playerid(ply)]

                self.pcon(player, '<orange>{num}<end> | <yellow>{steamid}<end> | <yellow>{country}<end> | <lime>{user}<end>'.format(
                    num='%03d' % (n + 1),
                    user=self.playername(ply),
                    country=inv[i['country']],
                    steamid=i['steamid']
                ))

            self.pcon(player, LINE)
            self.pcon(player, ply_count, COLOR['SYSTEM'])
            self.pcon(player, ply_stats, COLOR['SYSTEM'])
            self.pcon(player, LINE)

    # --------------------------------------------------------------------------
    def admins_list_CMD(self, player, cmd, args):
        ''' Admins List command function '''

        names = [self.playername(i) for i in self.activelist() if i.IsAdmin()]
        names = [names[i:i+3] for i in xrange(0, len(names), 3)]

        if names and not PLUGIN['HIDE ADMINS'] or player.IsAdmin():

            self.tell(player, '%s | %s:' % (self.prefix, MSG['ADMINS LIST TITLE']), f=False)
            self.tell(player, LINE, f=False)

            for i in names:

                self.tell(player, ', '.join(i), 'white', f=False)

        else:

            self.tell(player, MSG['NO ADMINS ONLINE'], COLOR['SYSTEM'])

    # -------------------------------------------------------------------------
    def plugins_list_CMD(self, player, cmd, args):
        ''' Plugins List command function '''

        self.tell(player, '%s | %s:' % (self.prefix, MSG['PLUGINS LIST TITLE']), f=False)
        self.tell(player, LINE, f=False)

        for i in plugins.GetAll():

            if i.Author != 'Oxide Team':
                
                self.tell(player, '<lime>{plugin.Title}<end> <grey>v{plugin.Version}<end> by {plugin.Author}'.format(plugin=i), f=False)

    # --------------------------------------------------------------------------
    def server_map_CMD(self, player, cmd, args):
        ''' Server Map command function '''

        self.tell(player, MSG['SERVER MAP'].format(ip=str(sv.ip), port=str(sv.port)))

    # --------------------------------------------------------------------------
    def plugin_CMD(self, player, cmd, args):
        ''' Plugins List command function '''

        if args and args[0] == 'help':

            self.tell(player, '%s | COMMANDS DESCRIPTION:' % self.prefix, f=False)
            self.tell(player, LINE, f=False)

            for cmd in CMDS:

                i = '%s DESC' % cmd

                if i in MSG: self.tell(player, MSG[i], f=False)
        else:

            self.tell(player, '<#00EEEE><size=18>NOTIFIER</size> <grey>v%s<end><end>' % self.Version, f=False)
            self.tell(player, self.Description, f=False)
            self.tell(player, 'Plugin powered by <orange>Oxide 2<end> and developed by <#9810FF>SkinN<end>', profile='76561197999302614', f=False)

    # -------------------------------------------------------------------------
    # - PLUGIN FUNCTIONS / HOOKS
    def playerid(self, player):
        ''' Function to return the player UserID '''

        return rust.UserIDFromPlayer(player)

    # -------------------------------------------------------------------------
    def playername(self, player):
        '''
            Returns the player name with player or Admin default name color
        '''

        name = player.displayName

        if player.IsAdmin():

            return '<%s>%s<end>' % (self.a_color, name)

        else:

            return '<%s>%s<end>' % (self.p_color, name)

    # -------------------------------------------------------------------------
    def playerlang(self, player, f=None):
        ''' Rules language filter '''

        default = PLUGIN['RULES LANGUAGE']

        if f:

            if f.upper() in RULES:

                return f.upper()

            else:

                self.tell(player, MSG['NO LANG'].replace('{args}', f), COLOR['SYSTEM'])

                return False

        elif default == 'AUTO':

            inv = {v: k for k, v in self.countries.items()}
            lang = inv[self.cache[self.playerid(player)]['country']]

            if lang in ('PT','BR'): lang = 'PT'
            elif lang in ('ES','MX','AR'): lang = 'ES'
            elif lang in ('FR','BE','CH','MC','MU'): lang = 'FR'

            return lang if lang in RULES else 'EN'

        else:

            return default if default in RULES else 'EN'

    # -------------------------------------------------------------------------
    def activelist(self):
        ''' Returns the active players list '''

        return BasePlayer.activePlayerList

    # -------------------------------------------------------------------------
    def sleeperlist(self):
        ''' Returns the sleepers list '''

        return BasePlayer.sleepingPlayerList

    # -------------------------------------------------------------------------
    def log_date(self):
        ''' Get current date string for logging '''

        localtime = time.localtime()

        return '%02d-%s' % (localtime[1], localtime[0])

    # -------------------------------------------------------------------------
    def cache_player(self, con):
        ''' Caches player information '''

        if con:

            uid = rust.UserIDFromConnection(con)

            self.cache[uid] = {
                'player': con.username,
                'steamid': uid,
                'auth': con.authLevel,
                'country': 'Unknown',
                'ip': con.ipaddress
            }

    # -------------------------------------------------------------------------
    def webrequest_filter(self, player, send=True):
        '''
            Multi functional filter:
            - Player Join Message
            - Cache player country
            - Welcome Message
        '''

        country = 'undefined'
        uid = self.playerid(player)
        ply = self.cache[uid]
        pip = player.net.connection.ipaddress.split(':')[0]

        def response_handler(code, response):

            # Webrequest response
            country = response.replace('\n','')

            if country == 'undefined' or code != 200:

                country = 'undefined'

            # Cache player country output
            if country in self.countries:

                country = self.countries[country]

            else:

                country = 'Unknown'

            ply['country'] = country

            if send:

                # Join Message
                if PLUGIN['ENABLE JOIN MESSAGE']:

                    if not (PLUGIN['HIDE ADMINS'] and int(ply['auth']) > 0):

                        self.say(MSG['JOIN MESSAGE'].format(user=self.playername(player), **ply), COLOR['JOIN MESSAGE'], uid)

                # Log player connection to file
                self.log('Connections', '{player} connected from {country} [UID: {steamid}][IP: {ip}]'.format(**ply))

                # Welcome Messages
                if PLUGIN['ENABLE WELCOME MESSAGE']:

                    lines = self.Config['WELCOME MESSAGE']

                    if lines:

                        self.tell(player, '\n'*50, f=False)

                        for line in lines:

                            line = line.format(ip=str(sv.ip), port=str(sv.port), hostname=sv.hostname, player=self.playername(player))

                            self.tell(player, line, COLOR['WELCOME MESSAGE'], f=False)

                    else:

                        PLUGIN['ENABLE WELCOME MESSAGE'] = False

                        self.con('No lines found on Welcome Message, turning it off')

        webrequests.EnqueueGet('http://ipinfo.io/%s/country' % pip, Action[Int32,String](response_handler), self.Plugin)

    # -------------------------------------------------------------------------
    def send_advert(self):
        ''' Function to send adverts to chat '''

        if ADVERTS:

            index = self.lastadvert

            if len(ADVERTS) > 1:

                while index == self.lastadvert:

                    index = random.Range(0, len(ADVERTS))

                self.lastadvert = index

            self.say(ADVERTS[index].format(**{
                'ip': str(sv.ip),
                'port': str(sv.ip),
                'seed': sv.seed if sv.seed else 'Random',
                'players': len(self.activelist()),
                'sleepers': len(self.sleeperlist()),
                'maxplayers': str(sv.maxplayers),
            }), COLOR['ADVERTS'])

        else:

            self.con('The Adverts list is empty, stopping Adverts loop')

            self.adverts_loop.Destroy()

    # -------------------------------------------------------------------------
    def format(self, text, con=False):
        '''
            Replaces color names and RGB hex code into HTML code
        '''

        colors = (
            'red', 'blue', 'green', 'yellow', 'white', 'black', 'cyan',
            'lightblue', 'lime', 'purple', 'darkblue', 'magenta', 'brown',
            'orange', 'olive', 'gray', 'grey', 'silver', 'maroon'
        )

        name = r'\<(\w+)\>'
        hexcode = r'\<(#\w+)\>'
        end = 'end'

        if con:
            for x in (end, name, hexcode):
                for c in re.findall(x, text):
                    if c.startswith('#') or c in colors or x == end:
                        text = text.replace('<%s>' % c, '')
        else:
            text = text.replace('<%s>' % end, '</color>')
            for f in (name, hexcode):
                for c in re.findall(f, text):
                    if c.startswith('#') or c in colors: text = text.replace('<%s>' % c, '<color=%s>' % c)
        return text

    # -------------------------------------------------------------------------
    def SendHelpText(self, player):
        ''' Hook called from HelpText plugin when /help is triggered '''

        self.tell(player, 'For all <#00EEEE>Notifier<end>\'s commands type <orange>/notifier help<end>', f=False)

    # -------------------------------------------------------------------------
    def countries_dict(self):
        ''' Returns a dictionary with countries full name '''

        return {
            'Unknown': 'Unknown',
            'AF': 'Afghanistan',
            'AS': 'American Samoa',
            'AD': 'Andorra',
            'AO': 'Angola',
            'AR': 'Argentina',
            'AU': 'Australia',
            'AT': 'Austria',
            'BE': 'Belgium',
            'BR': 'Brazil',
            'BG': 'Bulgaria',
            'CA': 'Canada',
            'CV': 'Cape Verde',
            'CF': 'Central African Republic',
            'TD': 'Chad',
            'CL': 'Chile',
            'CN': 'China',
            'CO': 'Colombia',
            'CR': 'Costa Rica',
            'HR': 'Croatia',
            'CU': 'Cuba',
            'CZ': 'Czech Republic',
            'DK': 'Denmark',
            'DO': 'Dominican Republic',
            'EC': 'Ecuador',
            'EG': 'Egypt',
            'EE': 'Estonia',
            'FI': 'Finland',
            'FR': 'France',
            'GE': 'Georgia',
            'DE': 'Germany',
            'GR': 'Greece',
            'HN': 'Honduras',
            'HU': 'Hungary',
            'IS': 'Iceland',
            'IN': 'India',
            'IE': 'Ireland',
            'IT': 'Italy',
            'JM': 'Jamaica',
            'JP': 'Japan',
            'LU': 'Luxembourg',
            'FX': 'Metropolitan France',
            'MX': 'Mexico',
            'MD': 'Moldova',
            'MC': 'Monaco',
            'ME': 'Montenegro',
            'MA': 'Morocco',
            'MZ': 'Mozambique',
            'NO': 'Norway',
            'PL': 'Poland',
            'PT': 'Portugal',
            'PR': 'Puerto Rico',
            'RO': 'Romania',
            'RU': 'Russia',
            'SG': 'Singapore',
            'SI': 'Slovenia',
            'ZA': 'South Africa',
            'ES': 'Spain',
            'SZ': 'Swaziland',
            'SE': 'Sweden',
            'CH': 'Switzerland',
            'TN': 'Tunisia',
            'TR': 'Turkey',
            'UG': 'Uganda',
            'UA': 'Ukraine',
            'AE': 'United Arab Emirates',
            'GB': 'United Kingdom',
            'US': 'United States'
        }