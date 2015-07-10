import re
import BasePlayer
import StringPool
from UnityEngine import Random
from UnityEngine import Vector3

DEV = False
LATEST_CFG = 4.5
LINE = '-' * 50
PROFILE = '76561198206240711'

class deathnotes:

    def __init__(self):

        self.Title = 'Death Notes'
        self.Author = 'SkinN'
        self.Description = 'Broadcasts players/animals deaths to chat'
        self.Version = V(2, 7, 0)
        self.ResourceId = 819

    # -------------------------------------------------------------------------
    # - CONFIGURATION
    def LoadDefaultConfig(self):
        ''' Hook called if there is no configuration file '''

        self.Config = {
            'CONFIG_VERSION': LATEST_CFG,
            'SETTINGS': {
                'PREFIX': 'DEATH NOTES <color=white>:</color>',
                'BROADCAST TO CONSOLE': True,
                'SHOW SUICIDES': True,
                'SHOW METABOLISM DEATHS': True,
                'SHOW EXPLOSION DEATHS': True,
                'SHOW TRAP DEATHS': True,
                'SHOW ANIMAL DEATHS': False,
                'SHOW BARRICADE DEATHS': True,
                'SHOW PLAYER KILLS': True,
                'SHOW ANIMAL KILLS': True,
                'MESSAGE IN RADIUS': False,
                'MESSAGES RADIUS': 300.0,
                'ENABLE PLUGIN ICON': True
            },
            'COLORS': {
                'MESSAGE': '#E0E0E0',
                'PREFIX': 'grey',
                'ANIMAL': '#4B75FF',
                'BODYPART': '#4B75FF',
                'WEAPON': '#4B75FF',
                'VICTIM': '#4B75FF',
                'ATTACKER': '#4B75FF',
                'DISTANCE': '#4B75FF'
            },
            'MESSAGES': {
                'RADIATION': ('{victim} died from radiation.', '{victim} did not know that radiation kills.'),
                'HUNGER': ('{victim} starved to death.', '{victim} should learn how to hunt so he finds something to eat.'),
                'THIRST': ('{victim} died of thirst.', '{victim} died dehydrated.'),
                'DROWNED': ('{victim} drowned.', '{victim} thought he could swim.'),
                'COLD': ('{victim} froze to death.', '{victim} is an ice cold dead man.'),
                'HEAT': ('{victim} burned to death.',),
                'FALL': ('{victim} died from a big fall.', '{victim} fell to his death.'),
                'BLEEDING': ('{victim} bled to death.', '{victim} emptied in blood.'),
                'EXPLOSION': ('{victim} died from a {weapon} explosion.', 'A {weapon} blew {victim} up.'),
                'POISON': ('{victim} died poisoned.',),
                'SUICIDE': ('{victim} committed suicide.', '{victim} has put an end to his life.'),
                'GENERIC': ('{victim} died.', '{victim} has been killed by the gods.'),
                'TRAP': ('{victim} stepped on a {attacker}.',),
                'BARRICADE': ('{victim} died stuck on a {attacker}.',),
                'STAB': ('{attacker} stabbed {victim} to death with a {weapon} and hit the {bodypart}.',),
                'STAB SLEEP': ('{attacker} stabbed {victim}, while he slept.',),
                'SLASH': ('{attacker} sliced {victim} into pieces with a {weapon} and hit the {bodypart}.',),
                'SLASH SLEEP': ('{attacker} stabbed {victim}, while he slept.',),
                'BLUNT': ('{attacker} killed {victim} with a {weapon} and hit the {bodypart}.', '{attacker} killed {victim} with a {weapon} causing a blunt trauma.'),
                'BLUNT SLEEP': ('{attacker} killed {victim} with a {weapon}, while he slept.',),
                'BULLET': ('{attacker} killed {victim} with a {weapon}, hitting the {bodypart} from {distance}m.', '{attacker} made {victim} eat some bullets with a {weapon} from {distance}m.'),
                'BULLET SLEEP': ('{attacker} killed {victim}, while sleeping. (In the {bodypart} with a {weapon}, from {distance}m)', '{attacker} killed {victim} with a {weapon}, while sleeping.'),
                'ARROW': ('{attacker} killed {victim} with an arrow {distance}m, hitting the {bodypart}.',),
                'ARROW SLEEP': ('{attacker} killed {victim} with an arrow from {distance}m, while he slept.',),
                'BITE': ('A {attacker} killed {victim}.',),
                'BITE SLEEP': ('A {attacker} killed {victim}, while he slept.',),
                'ANIMAL DEATH': ('{attacker} killed a {victim} with a {weapon} from {distance}m.',)
            },
            'BODYPARTS': {
                'SPINE': 'Spine',
                'LIP': 'Lips',
                'JAW': 'Jaw',
                'NECK': 'Neck',
                'TAIL': 'Tail',
                'HIP': 'Hip',
                'FOOT': 'Feet',
                'PELVIS': 'Pelvis',
                'LEG': 'Leg',
                'HEAD': 'Head',
                'ARM': 'Arm',
                'JOINT': 'Joint',
                'PENIS': 'Penis',
                'WING': 'Wing',
                'EYE': 'Eye',
                'EAR': 'Ear',
                'STOMACH': 'Stomach',
                'MANE': 'Mane',
                'CLAVICLE': 'Clavicle',
                'FINGERS': 'Fingers',
                'THIGH': 'Thigh',
                'GROUP': 'Group',
                'SHOULDER': 'Shoulder',
                'CALF': 'Calf',
                'TOE': 'Toe',
                'HAND': 'Hand',
                'KNEE': 'Knee',
                'FOREARM': 'Forearm',
                'UPPERARM': 'Upperarm',
                'TONGUE': 'Tongue',
                'SHIN': 'Shin',
                'ULNA': 'Ulna',
                'ROOTBONE': 'Chicken Rootbone',
                'BROW': 'Brow'
            },
            'WEAPONS': {
                'WOODEN_SPEAR.WEAPON': 'Wooden Spear',
                'STONE_SPEAR.WEAPON': 'Stone Spear',
                'STONE_PICKAXE.WEAPON': 'Stone Pickaxe',
                'HUNTING.WEAPON': 'Hunting Bow',
                'AK47U.WEAPON': 'Assault Rifle',
                'ROCK.WEAPON': 'Rock',
                'HATCHET.WEAPON': 'Hatchet',
                'PICKAXE.WEAPON': 'Pickaxe',
                'BOLTRIFLE.WEAPON': 'Bolt Action Rifle',
                'SALVAGED_HAMMER.WEAPON': 'Salvaged Hammer',
                'SAWNOFFSHOTGUN.WEAPON': 'Pump Shotgun',
                'SALVAGED_AXE.WEAPON': 'Salvaged Axe',
                'BONEKNIFE.WEAPON': 'Bone Knife',
                'WATERPIPE.WEAPON': 'Waterpipe Shotgun',
                'HATCHET_STONE.WEAPON': 'Stone Hatchet',
                'EOKA.WEAPON': 'EOKA Pistol',
                'SALVAGED_ICEPICK.WEAPON': 'Salvaged Icepick',
                'TORCH.WEAPON': 'Torch',
                'THOMPSON.WEAPON': 'Thompson',
                'REVOLVER.WEAPON': 'Revolver',
                'ROCKET_BASIC': 'Rocket',
                'GRENADE.F1.DEPLOYED': 'F1 Grenade',
                'GRENADE.BEANCAN.DEPLOYED': 'Beancan Grenade',
                'TIMED.EXPLOSIVE.DEPLOYED': 'Timed Explosive Charge',
                'SMG.WEAPON': 'Custom SMG',
                'SEMI_PISTOL.WEAPON': 'Semi-Automatic Pistol',
                'BONE_CLUB.WEAPON': 'Bone Club',
                'SWORD.WEAPON': 'Salvaged Sword',
                'CLEAVER.WEAPON': 'Machete'
            },
            'TRAPS': {
                'FLOOR_SPIKES': 'Wooden Floor Spike',
                'BEARTRAP': 'Snap Trap',
                'LANDMINE': 'Landmine'
            },
            'BARRICADES': {
                'BARRICADE.METAL': 'Metal Barricade',
                'BARRICADE.WOOD': 'Wooden Barricade',
                'BARRICADE.WOODWIRE': 'Barbed Wooden Barricade'
            },
            'ANIMALS': {
                'STAG': 'Stag',
                'CHICKEN': 'Chicken',
                'WOLF': 'Wolf',
                'BEAR': 'Bear',
                'BOAR': 'Boar',
                'HORSE': 'Horse'
            }
        }

        self.con('Loading default configuration file')

    # -------------------------------------------------------------------------
    def UpdateConfig(self):
        ''' Function to update the configuration file on plugin Init '''

        if self.Config['CONFIG_VERSION'] <= LATEST_CFG - 0.2 or DEV:

            self.con('Current configuration file is two or more versions older than the latest (Current: v%s / Latest: v%s)' % (self.Config['CONFIG_VERSION'], LATEST_CFG))

            self.Config.clear()

            self.LoadDefaultConfig()

        else:

            self.con('Applying new changes to the configuration file (Version: %s)' % LATEST_CFG)

            self.Config['SETTINGS']['ENABLE PLUGIN ICON'] = True

            self.Config['WEAPONS']['SWORD.WEAPON'] = 'Salvaged Sword'
            self.Config['WEAPONS']['CLEAVER.WEAPON'] = 'Machete'

            self.Config['CONFIG_VERSION'] = LATEST_CFG

        # SAVE CHANGES
        self.SaveConfig()

    # -------------------------------------------------------------------------
    # - PLUGIN HOOKS
    def Init(self):
        ''' Hook called when the plugin initializes '''

        if self.Config['CONFIG_VERSION'] < LATEST_CFG or DEV: self.UpdateConfig()

        global MSG, PLUGIN, COLOR, PARTS, WEAPONS, TRAPS, ANIMALS, BARRICADES
        MSG, TRAPS, COLOR, PARTS, PLUGIN, WEAPONS, ANIMALS, BARRICADES = (
            self.Config[i] for i in ('MESSAGES', 'TRAPS', 'COLORS', 'BODYPARTS', 'SETTINGS', 'WEAPONS', 'ANIMALS', 'BARRICADES')
        )

        self.prefix = '<color=%s>%s</color>' % (COLOR['PREFIX'], PLUGIN['PREFIX']) if PLUGIN['PREFIX'] else None
        self.metabolism = ('DROWNED', 'HEAT', 'COLD', 'THIRST', 'POISON', 'HUNGER', 'RADIATION', 'BLEEDING', 'FALL', 'GENERIC')

        if not PLUGIN['ENABLE PLUGIN ICON']:

            global PROFILE
            PROFILE = '0'

        command.AddChatCommand('deathnotes', self.Plugin, 'plugin_CMD')

    # -------------------------------------------------------------------------
    # - MESSAGE SYSTEM
    def con(self, text):
        ''' Function to send a server con message '''

        if self.Config['SETTINGS']['BROADCAST TO CONSOLE']:

            print('[%s v%s] :: %s' % (self.Title, str(self.Version), text))

    # -------------------------------------------------------------------------
    def debug(self, text):
        ''' Function for developer debugging messages only '''

        if DEV: self.con(text)

    # -------------------------------------------------------------------------
    def say(self, text, color='white', f=True, profile=False):
        ''' Function to send a message to all players '''

        if self.prefix and f:

            rust.BroadcastChat('%s <color=%s>%s</color>' % (self.prefix, color, text), None, PROFILE if not profile else profile)

        else:

            rust.BroadcastChat('<color=%s>%s</color>' % (color, text), None, PROFILE if not profile else profile)

    # -------------------------------------------------------------------------
    def tell(self, player, text, color='white', f=True, profile=False):
        ''' Function to send a message to a player '''

        if self.prefix and f:

            rust.SendChatMessage(player, '%s <color=%s>%s</color>' % (self.prefix, color, text), None, PROFILE if not profile else profile)

        else:

            rust.SendChatMessage(player, '<color=%s>%s</color>' % (color, text), None, PROFILE if not profile else profile)

    # -------------------------------------------------------------------------
    def log(self, filename, text):
        ''' Logs text into a specific file '''

        if self.logs:

            try:

                filename = 'deathnotes_%s_%s.txt' % (filename, self.log_date())

                sv.Log('oxide/logs/%s' % filename, text)

            except:

                self.con('An error as occurred when writing a connection log to a file! ( Missing directory )')
                self.con('Logs are now off, please make sure you have the following path on your server files: .../%s/oxide/logs' % sv.identity)

    # --------------------------------------------------------------------------
    def say_filter(self, text, raw, vpos, attacker):
        ''' Message filter in case radius is set to True '''

        c = COLOR['MESSAGE']

        if PLUGIN['MESSAGE IN RADIUS']:

            for ply in BasePlayer.activePlayerList:

                if self.distance(ply.transform.position, vpos) <= float(PLUGIN['MESSAGES RADIUS']):

                    self.tell(ply, text, c)

                elif attacker and ply == attacker: self.tell(ply, text, c)

        else: self.say(text, c)

        if PLUGIN['BROADCAST TO CONSOLE']: self.con(raw)

    # -------------------------------------------------------------------------
    # - SERVER HOOKS
    def OnEntityDeath(self, vic, hitinfo):
        ''' Hook called when an entity dies '''

        if 'corpse' not in str(vic):

            clr = {}
            msg = None
            dmg = str(vic.lastDamage).upper()
            vps = vic.transform.position
            att = hitinfo.Initiator if hitinfo else None

            raw = {
                'bodypart': self.bodypart(hitinfo.HitBone) if hitinfo else 'None',
                'weapon': self.weapon(hitinfo.Weapon) if hitinfo else 'None',
                'distance': '%.2f' % self.distance(vps, att.transform.position) if att else 'None'
            }

            if att:

                if att.ToPlayer():

                    raw['attacker'] = att.displayName

                else:

                    raw['attacker'] = str(att.LookupShortPrefabName()).upper()

            else:

                raw['attacker'] = 'None'

            if vic:

                raw['victim'] = str(vic)

                if vic.ToPlayer():

                    raw['victim'] = vic.displayName

                    sleep = vic.IsSleeping()

                    # Is is Suicide or from Metabolism?
                    if (dmg == 'SUICIDE' and PLUGIN['SHOW SUICIDES']) or (dmg in self.metabolism and PLUGIN['SHOW METABOLISM DEATHS']):

                        msg = dmg

                    # Is attacker a Player?
                    elif att and att.ToPlayer() and dmg in ('SLASH', 'BLUNT', 'STAB', 'BULLET') and PLUGIN['SHOW PLAYER KILLS']:

                        if 'hunting' in str(hitinfo.Weapon):

                            msg = 'ARROW SLEEP' if sleep else 'ARROW'

                        else:  msg = '%s SLEEP' % dmg if sleep else dmg

                    # Is attacker an explosive?
                    elif dmg == 'EXPLOSION' or raw['attacker'].startswith('GRENADE') and PLUGIN['SHOW EXPLOSION DEATHS']:

                        raw['weapon'] = WEAPONS[raw['attacker']] if raw['attacker'] in WEAPONS else raw['attacker']
                        msg = 'EXPLOSION'

                    # Is attacker a trap?
                    elif raw['attacker'] in ('LANDMINE', 'Snap Trap', 'FLOOR_SPIKES') and PLUGIN['SHOW TRAP DEATHS']:

                        raw['attacker'] = TRAPS[raw['attacker']] if raw['attacker'] in TRAPS else raw['attacker']
                        msg = 'TRAP'

                    # Is attacker a Barricade?
                    elif dmg in ('SLASH', 'STAB') and PLUGIN['SHOW BARRICADE DEATHS']:

                        raw['attacker'] = BARRICADES[raw['attacker']] if raw['attacker'] in BARRICADES else raw['attacker']
                        msg = 'BARRICADE'

                    # Is attacker an Animal?
                    elif dmg == 'BITE' and PLUGIN['SHOW ANIMAL KILLS']:

                        raw['attacker'] = ANIMALS[raw['attacker']] if raw['attacker'] in ANIMALS else raw['attacker']
                        msg = 'BITE SLEEP' if sleep else dmg

                # Otherwise victim is an Animal ( Non-Human NPC )
                elif 'animals' in str(vic) and att and att.ToPlayer() and (PLUGIN['SHOW ANIMAL DEATHS'] or DEV):

                    animal = str(vic.LookupShortPrefabName()).upper()
                    raw['victim'] = ANIMALS[animal] if animal in ANIMALS else animal
                    msg = 'ANIMAL DEATH'

                #self.debug(LINE)
                #self.debug(' # DEATH REPORT')
                #self.debug(LINE)
                #self.debug('- MESSAGE TYPE: %s' % (msg if msg else 'None'))
                #self.debug('- DAMAGE : %s' % dmg)
                #self.debug('- VICTIM : %s ( %s )' % (raw['victim'], vic))
                #self.debug('- ATTACKER : %s ( %s )' % (raw['attacker'], att))
                #self.debug('- WEAPON : %s' % raw['weapon'])
                #self.debug('- BODY PART : %s' % raw['bodypart'])
                #self.debug('- DISTANCE : %s' % raw['distance'])
                #self.debug(LINE)

            if msg:

                msg = MSG[msg]

                if isinstance(msg, tuple): msg = msg[Random.Range(0, len(msg))]

                if msg:

                    for n in raw: clr[n] = '<color=%s>%s</color>' % (COLOR[n.upper()], raw[n])

                    try: self.say_filter(msg.format(**clr), msg.format(**raw), vps, att)
                    except Exception as e:

                        if type(e).__name__ == 'KeyError':

                            self.con('# NAME FORMAT ERROR')
                            self.con(LINE)
                            self.con('Unrecognized name format found in message:')
                            self.con('\'%s\'' % msg)
                            self.con(LINE)
                            self.con('You may only use these name formats in messages:')
                            self.con('{victim}, {attacker}, {weapon}, {bodypart}, {distance}')
                            self.con(LINE)

                            return

                #self.debug(LINE)

    # -------------------------------------------------------------------------
    # - PLUGIN FUNCTIONS / HOOKS
    def distance(self, p1, p2):
        ''' Function to get the distance between two points '''

        return Vector3.Distance(p1, p2)

    # -------------------------------------------------------------------------
    def bodypart(self, p):
        ''' Function to check wether the hitbone is in the config file '''

        if p:

            p = StringPool.Get(p).upper()

            for i in PARTS: p = i if i in p else p

            return PARTS[p] if p in PARTS else p

        return 'None'

    # -------------------------------------------------------------------------
    def weapon(self, w):
        ''' Function to check wether the weapon used is in the config file '''

        if w:

            w = str(w.LookupShortPrefabName()).upper()

            return WEAPONS[w] if w in WEAPONS else w

        return 'None'

    # -------------------------------------------------------------------------
    # - COMMAND FUNCTIONS
    def plugin_CMD(self, player, cmd, args):
        ''' Plugin command function '''

        self.tell(player, '<size=18><color=#808080>Death Notes</color></size> <color=grey>v%s</color>' % self.Version, profile='76561198206240711', f=False)
        self.tell(player, '<color=silver>%s</color>' % self.Description, profile='76561198206240711', f=False)
        self.tell(player, '<color=silver>Plugin developed by <color=#9810FF>SkinN</color>, powered by <color=orange>Oxide 2</color>.</color>', profile='76561197999302614', f=False)