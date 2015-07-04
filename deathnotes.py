# ==============================================================================
# DAMAGES TABLE
# ==============================================================================
# STAB      = KNIFES / SPEARS / PICKAXES / ARROW / ICEPICK / GRENADES(?)
# SLASH     = SALVAGE AXE / HATCHETS / BARRICADES / FLOOR SPIKES
# BLUNT     = TORCH / ROCK / SALVAGE HAMMER / LANDMINE
# BITE      = ANIMALS / SNAP TRAP
# BULLET    = GUNS / BOW
# EXPLOSION = C4 / ROCKET
# ==============================================================================
# METABOLISM
# ==============================================================================
# FALL   | DROWNED | POISON | COLD | HEAT | RADIATION LEVEL/POISON
# HUNGER | THIRST | BLEEDING |
# ==============================================================================
# ANIMALS
# ==============================================================================
# HORSE | WOLF | BEAR | BOAR | STAG | CHICKEN
# ==============================================================================

import re
import BasePlayer
import StringPool
from  UnityEngine import Random
from UnityEngine import Vector3

# GLOBAL VARIABLES
DEV = False
LATEST_CFG = 4.4
LINE = '-' * 50

class deathnotes:

    # ==========================================================================
    # <>> PLUGIN
    # ==========================================================================
    def __init__(self):

        self.Title = 'Death Notes'
        self.Author = 'SkinN'
        self.Description = 'Broadcasts players/animals deaths to chat'
        self.Version = V(2, 6, 0)
        self.ResourceId = 819

    # ==========================================================================
    # <>> CONFIGURATION
    # ==========================================================================
    def LoadDefaultConfig(self):

        self.Config = {
            'CONFIG_VERSION': LATEST_CFG,
            'SETTINGS': {
                'PREFIX': self.Title.upper(),
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
                'MESSAGES RADIUS': 300.0
            },
            'COLORS': {
                'MESSAGE': '#FFFFFF',
                'PREFIX': '#FF0000',
                'ANIMAL': '#00FF00',
                'BODYPART': '#00FF00',
                'WEAPON': '#00FF00',
                'VICTIM': '#00FF00',
                'ATTACKER': '#00FF00',
                'DISTANCE': '#00FF00'
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
                'BONE_CLUB.WEAPON': 'Bone Club'
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

        self.console('Loading default configuration file', True)

    # --------------------------------------------------------------------------
    def UpdateConfig(self):

        # IS OLDER CONFIG TOO OLD?
        if self.Config['CONFIG_VERSION'] <= LATEST_CFG - 0.2 or DEV:

            self.console('Current configuration file is two or more versions older than the latest (Current: v%s / Latest: v%s)' % (self.Config['CONFIG_VERSION'], LATEST_CFG), True)

            # RESET CONFIGURATION
            self.Config.clear()

            # LOAD DEFAULTS CONFIGURATION
            self.LoadDefaultConfig()

        else:

            self.console('Applying new changes to the configuration file (Version: %s)' % LATEST_CFG, True)

            # NEW VERSION VALUE
            self.Config['CONFIG_VERSION'] = LATEST_CFG

            # NEW CHANGES
            self.Config['SETTINGS']['SHOW BARRICADE DEATHS'] = True

            self.Config['WEAPONS']['BONE_CLUB.WEAPON'] = 'Bone Club'

            self.Config['MESSAGES']['BARRICADE'] = ('{victim} died stuck on a {attacker}.',)
            self.Config['MESSAGES']['TRAP'] = ('{victim} stepped on a {attacker}.',)

            self.Config['BARRICADES'] = {
                'BARRICADE.METAL': 'Metal Barricade',
                'BARRICADE.WOOD': 'Wooden Barricade',
                'BARRICADE.WOODWIRE': 'Barbed Wooden Barricade'
            }

            self.Config['TRAPS']['LANDMINE'] = 'Landmine'

            for i in ('BARRICADE.METAL' ,'BARRICADE.WOOD' , 'BARRICADE.WOODWIRE'):

                del self.Config['TRAPS'][i]

        # SAVE CHANGES
        self.SaveConfig()

    # ==========================================================================
    # <>> PLUGIN SPECIFIC
    # ==========================================================================
    def Init(self):

        if self.Config['CONFIG_VERSION'] < LATEST_CFG or DEV:
            self.UpdateConfig()

        global MSG, PLUGIN, COLOR, PARTS, WEAPONS, TRAPS, ANIMALS, BARRICADES
        MSG, TRAPS, COLOR, PARTS, PLUGIN, WEAPONS, ANIMALS, BARRICADES = (
            self.Config[i] for i in ('MESSAGES', 'TRAPS', 'COLORS', 'BODYPARTS', 'SETTINGS', 'WEAPONS', 'ANIMALS', 'BARRICADES')
        )

        self.prefix = '<color=%s>%s</color>' % (COLOR['PREFIX'], PLUGIN['PREFIX']) if PLUGIN['PREFIX'] else None
        self.metabolism = ('DROWNED', 'HEAT', 'COLD', 'THIRST', 'POISON', 'HUNGER', 'RADIATION', 'BLEEDING', 'FALL', 'GENERIC')

        command.AddChatCommand('deathnotes', self.Plugin, 'plugin_CMD')

    # ==========================================================================
    # <>> MESSAGE FUNTIONS
    # ==========================================================================
    def console(self, text, f=False):

        if self.Config['SETTINGS']['BROADCAST TO CONSOLE'] or f:
            print('[%s v%s] :: %s' % (self.Title, str(self.Version), text))

    # --------------------------------------------------------------------------
    def debug(self, text):

        if DEV:
            self.console(text)

    # --------------------------------------------------------------------------
    def say(self, text, color='white', userid=0):

        if self.prefix:
            rust.BroadcastChat('%s <color=white>:</color> <color=%s>%s</color>' % (self.prefix, color, text), None, str(userid))
        else:
            rust.BroadcastChat('<color=%s>%s</color>' % (color, text), None, str(userid))

    # --------------------------------------------------------------------------
    def tell(self, player, text, color='white', userid=0, f=True):

        if self.prefix and f:
            rust.SendChatMessage(player, '%s <color=white>:</color> <color=%s>%s</color>' % (self.prefix, color, text), None, str(userid))
        else:
            rust.SendChatMessage(player, '<color=%s>%s</color>' % (color, text), None, str(userid))

    # --------------------------------------------------------------------------
    def say_filter(self, text, raw, vpos, attacker):

        color = COLOR['MESSAGE']
        if PLUGIN['MESSAGE IN RADIUS']:
            for player in BasePlayer.activePlayerList:
                if self.distance(player.transform.position, vpos) <= float(PLUGIN['MESSAGES RADIUS']):
                    self.tell(player, text, color)
                elif attacker and player == attacker:
                    self.tell(player, text, color)
        else:
            self.say(text, color)
        if PLUGIN['BROADCAST TO CONSOLE']:
            self.console(raw)

    # ==========================================================================
    # <>> MAIN HOOKS
    # ==========================================================================
    def OnEntityDeath(self, vic, hitinfo):

        # IS ENTITY NOT A CORPSE?
        if 'corpse' not in str(vic):

            # DEATH INFOS
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

            # ATTACKER
            if att:
                if att.ToPlayer():
                    raw['attacker'] = att.displayName
                else:
                    raw['attacker'] = str(att.LookupShortPrefabName()).upper()
            else:
                raw['attacker'] = 'None'

            if vic:

                raw['victim'] = str(vic)

                # IS VICTIM A PLAYER OR NPC PLAYER?
                if vic.ToPlayer():

                    raw['victim'] = vic.displayName

                    # IS VICTIM SLEEPING?
                    sleep = vic.IsSleeping()

                    # IS DEATHS SUICIDE OR METABOLISM TYPE?
                    if (dmg == 'SUICIDE' and PLUGIN['SHOW SUICIDES']) or (dmg in self.metabolism and PLUGIN['SHOW METABOLISM DEATHS']):

                        msg = dmg

                    # IS ATTACKER A PLAYER?
                    elif att and att.ToPlayer() and dmg in ('SLASH', 'BLUNT', 'STAB', 'BULLET') and PLUGIN['SHOW PLAYER KILLS']:

                        if 'hunting' in str(hitinfo.Weapon):
                            msg = 'ARROW SLEEP' if sleep else 'ARROW'
                        else:
                            msg = '%s SLEEP' % dmg if sleep else dmg

                    # IS ATTACKER AN EXPLOSIVE? (?)
                    elif dmg == 'EXPLOSION' or raw['attacker'].startswith('GRENADE') and PLUGIN['SHOW EXPLOSION DEATHS']:

                        raw['weapon'] = WEAPONS[raw['attacker']] if raw['attacker'] in WEAPONS else raw['attacker']
                        msg = 'EXPLOSION'

                    # IS ATTACKER A TRAP?
                    elif raw['attacker'] in ('LANDMINE', 'Snap Trap', 'FLOOR_SPIKES') and PLUGIN['SHOW TRAP DEATHS']:

                        raw['attacker'] = TRAPS[raw['attacker']] if raw['attacker'] in TRAPS else raw['attacker']
                        msg = 'TRAP'

                    # IS ATTACKER A BARRICADE?
                    elif dmg in ('SLASH', 'STAB') and PLUGIN['SHOW BARRICADE DEATHS']:

                        raw['attacker'] = BARRICADES[raw['attacker']] if raw['attacker'] in BARRICADES else raw['attacker']
                        msg = 'BARRICADE'

                    # IS ATTACKER AN ANIMAL?
                    elif dmg == 'BITE' and PLUGIN['SHOW ANIMAL KILLS']:

                        raw['attacker'] = ANIMALS[raw['attacker']] if raw['attacker'] in ANIMALS else raw['attacker']
                        msg = 'BITE SLEEP' if sleep else dmg

                # OTHERWISE IS ANIMAL (NPC?)
                elif 'animals' in str(vic) and att and att.ToPlayer() and PLUGIN['SHOW ANIMAL DEATHS']:

                    animal = str(vic.LookupShortPrefabName()).upper()
                    raw['victim'] = ANIMALS[animal] if animal in ANIMALS else animal
                    msg = 'ANIMAL DEATH'

                # DEBUG REPORT
                #self.debug(LINE)
                #self.debug(' # REPORT')
                #self.debug(LINE)
                #self.debug('- MESSAGE TYPE: %s' % msg if msg else 'None')
                #self.debug('- DAMAGE : %s' % dmg)
                #self.debug('- VICTIM : %s ( %s )' % (raw['victim'], vic))
                #self.debug('- ATTACKER : %s ( %s )' % (raw['attacker'], att))
                #self.debug('- WEAPON : %s' % raw['weapon'])
                #self.debug('- BODY PART : %s' % raw['bodypart'])
                #self.debug('- DISTANCE : %s' % raw['distance'])
                #self.debug(LINE)

            if msg:

                # MESSAGE STRING
                msg = MSG[msg]

                if isinstance(msg, tuple):
                    msg = msg[Random.Range(0, len(msg))]

                if msg:

                    # PLACE NAMES COLORS
                    for n in raw: clr[n] = '<color=%s>%s</color>' % (COLOR[n.upper()], raw[n])

                    # FILTER MESSAGE
                    try:
                        self.say_filter(msg.format(**clr), msg.format(**raw), vps, att)
                    except:
                        self.console('# NAME FORMAT ERROR')
                        self.console(LINE)
                        self.console('Unrecognized name format found in message:')
                        self.console('\'%s\'' % msg)
                        self.console(LINE)
                        self.console('You may only use these name formats in messages:')
                        self.console('{victim}, {attacker}, {weapon}, {bodypart}, {distance}')
                        self.console(LINE)

                #self.debug(LINE)

    # ==========================================================================
    # <>> SIDE FUNTIONS
    # ==========================================================================
    def distance(self, p1, p2):

        return Vector3.Distance(p1, p2)

    # --------------------------------------------------------------------------
    def bodypart(self, part):

        if part:
            part = StringPool.Get(part).upper()
            for p in PARTS:
                part = p if p in part else part
            return PARTS[part] if part in PARTS else part
        return 'None'

    # --------------------------------------------------------------------------
    def weapon(self, weapon):

        if weapon:
            x = str(weapon.LookupShortPrefabName()).upper()
            return WEAPONS[x] if x in WEAPONS else x
        return 'None'

    # ==========================================================================
    # <>> COMMANDS
    # ==========================================================================
    def plugin_CMD(self, player, cmd, args):

        self.tell(player, LINE, f=False)
        self.tell(player, '<color=lime>Death Notes v%s</color> by <color=lime>SkinN</color>' % self.Version, f=False)
        self.tell(player, self.Description, 'lime', f=False)
        self.tell(player, '| RESOURSE ID: <color=lime>%s</color> | CONFIG: v<color=lime>%s</color> |' % (self.ResourceId, self.Config['CONFIG_VERSION']), f=False)
        self.tell(player, LINE, f=False)
        self.tell(player, '<< Click the icon to contact me.', userid='76561197999302614', f=False)

# ==============================================================================