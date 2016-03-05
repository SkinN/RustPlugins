using System.Text.RegularExpressions;
using System.Collections.Generic;
using Oxide.Game.Rust.Libraries;
using Newtonsoft.Json.Linq;
using Newtonsoft.Json;
using UnityEngine;
using System.Linq;
using Oxide.Core;
using System;


namespace Oxide.Plugins
{
    [Info("Notifier", "SkinN", 3.0, ResourceId = 797)]
    [Description("Server administration tool with chat based notifications")]

    class Notifier : RustPlugin
    {
        #region Plugin Variables

        /* The Developer mode is used mostly for debugging or testing features
           of the plugin, also forces the default configuration file
           on each load */

        // Developer Variables
        private readonly bool Dev = true;
        private readonly string Seperator = string.Join("-", new string[50 + 1]);
        private readonly string DatabaseFile = "Notifier_PlayersData"; 

        // Plugin Variables
        private Dictionary<string, PlayerCache> Players;
        private int LastAdvert = 0;

        // Players Cache Class
        public class PlayerCache
        {
            public string username;
            public string steamid;
            public string country;
            public string country_code;
            public string ipaddress;
            public bool isadmin;

            public PlayerCache()
            {
            }

            internal PlayerCache(BasePlayer player)
            {
                /* Creates the player cache info */

                steamid = player.userID.ToString();
                country = "Unknown";
                country_code = "Unknown";
                
                this.Update(player);
            }

            internal void Update(BasePlayer player)
            {
                /* Updates the player cache info */

                username = player.displayName;
                ipaddress = player.net.connection.ipaddress.Split(':')[0];
                isadmin = player.IsAdmin();
            }
        };

        #endregion Plugin Variables
// ----------------------------------------------------------------------------
        #region Configuration

        // Configuration Variables
        private string Prefix;
        private string IconProfile;
        private int AdvertsInterval;
        private bool EnableIconProfile;
        private bool EnableJoinMessage;
        private bool EnableLeaveMessage;
        private bool BroadcastToConsole;
        private bool EnablePluginPrefix;
        private bool EnableAdvertMessages;
        private bool EnableWelcomeMessage;
        private bool NotifyHelicopter;
        private bool NotifyAirdrop;
        private bool HideAdmins;

        // Lists Variables
        private List<object> Adverts;
        private List<object> WelcomeMessage;

        protected override void LoadDefaultConfig()
        {
            /* Hook called when the config for the plugin initializes */

            Puts("Creating new configuration file");

            // Clear configuration for a brand new one
            Config.Clear();

            // Load plugin variables
            LoadVariables();
        }

        void LoadVariables()
        {
            /* Method to setup the global variables with all configuration values */

            // Clear configuration if on developer mode
            if (Dev)
                Config.Clear();

            // Settings Section
            Prefix = GetConfig<string>("General Settings", "Prefix", "[ <cyan>NOTIFIER<end> ]");
            EnablePluginPrefix = GetConfig<bool>("General Settings", "Enable Plugin Prefix", true);
            EnableIconProfile = GetConfig<bool>("General Settings", "Enable Icon Profile", false);
            IconProfile = GetConfig<string>("General Settings", "Icon Profile", "76561198235146288");
            BroadcastToConsole = GetConfig<bool>("General Settings", "Broadcast To Console", true);
            EnableJoinMessage = GetConfig<bool>("General Settings", "Enable Join Message", true);
            EnableLeaveMessage = GetConfig<bool>("General Settings", "Enable Leave Message", true);
            EnableAdvertMessages = GetConfig<bool>("General Settings", "Enable Advert Messages", true);
            EnableWelcomeMessage = GetConfig<bool>("General Settings", "Enable Welcome Message", true);
            AdvertsInterval = GetConfig<int>("General Settings", "Adverts Interval (In Minutes)", 12);
            NotifyHelicopter = GetConfig<bool>("General Settings", "Notify Incoming Airdrop", false);
            NotifyAirdrop = GetConfig<bool>("General Settings", "Notify Incoming Patrol Helicopter", false);
            HideAdmins = GetConfig<bool>("General Settings", "Hide Admins", false);

            // Advert Messages
            Adverts = GetConfig<List<object>>("Advert Messages", new List<object>(new string[] {
                        "Welcome to our server, have fun!",
                        "<orange>Need help?<end> Try calling for the <cyan>Admins<end> in the chat.",
                        "Please, be respectful with to the other players.",
                        "Cheating will result in a <red>permanent<end> ban"
                    }
                )
            );

            // Welcome Message
            WelcomeMessage = GetConfig<List<object>>("Welcome Message", new List<object>(new string[] {
                        "<size=18>Welcome <lightblue>{username}<end></size>",
                        "<orange><size=20>•</size><end> Type <orange>/help<end> for all available commands",
                        "<orange><size=20>•</size><end> Please respect our server <orange>/rules<end>",
                        "<orange><size=20>•</size><end> Check our live map at <lime>http://{server.ip}:{server.port}<end>"
                    }
                )
            );

            // Command Triggers
            SetConfig("Commands", "Triggers", "Players List", new string[] { "players" });
            SetConfig("Commands", "Triggers", "Plugins List", new string[] { "plugins" });
            SetConfig("Commands", "Triggers", "Admins List", new string[] { "admins" });
            SetConfig("Commands", "Triggers", "Players Count", new string[] { "online" });
            SetConfig("Commands", "Triggers", "Server MOTD", new string[] { "motd" });
            SetConfig("Commands", "Triggers", "Server Map", new string[] { "map" });
            SetConfig("Commands", "Triggers", "Server Rules", new string[] { "rules" });

            // Command Settings
            SetConfig("Commands", "Settings", "Players List", true);
            SetConfig("Commands", "Settings", "Plugins List", false);
            SetConfig("Commands", "Settings", "Admins List", false);
            SetConfig("Commands", "Settings", "Server Rules", false);
            SetConfig("Commands", "Settings", "Server Map", false);
            SetConfig("Commands", "Settings", "Server MOTD", false);
            SetConfig("Commands", "Settings", "Players Count", false);

            // Save file
            SaveConfig();
        }

        private T GetConfig<T>(params object[] args)
        {
            /* Gets a value from the configuration file
                Method Notes:
                - Developer mode forces the default values on every setting on each load
                - This method was provided by LaserHydra and tweaked by Nogrod */

            var stringArgs = new string[args.Length - 1];
            for (var i = 0; i < args.Length - 1; i++)
                stringArgs[i] = args[i].ToString();

            if (Config.Get(stringArgs) == null || Dev)
                Config.Set(args);

            return (T)Convert.ChangeType(Config.Get(stringArgs), typeof(T));
        }

        private void SetConfig(params object[] args)
        {
            /* Method to set value to the configuration file */

            var stringArgs = new string[args.Length - 1];
            for (var i = 0; i < args.Length - 1; i++)
                stringArgs[i] = args[i].ToString();

            if (Config.Get(stringArgs) == null || Dev)
                Config.Set(args);
        }

        private void LoadMessages()
        {
            /* Method to register messages to Lang library from Oxide */

            lang.RegisterMessages(new Dictionary<string, string> {
                { "Join Message", "<lightblue>{username} <silver>joined from<end> {country}<end>" },
                { "Leave Message", "<lightblue>{username}<end> left the server" },
                { "Incoming Airdrop", "<yellow>Airdrop <silver>incoming, drop coordinates are:<end> {location}<end>."},
                { "Incoming Helicopter", "<yellow>Patrol Helicoter<end> incoming!" },
                { "Players List Description", "List of active players" },
                { "Plugins List Description", "List of plugins running in the server" },
                { "Admins List Description", "List of active Admins" },
                { "Server Rules Description", "Displays server rules (In the player Steam language if set to automatic)" },
                { "Server Map Description", "Shows the URL to the server live map (Rust:IO)" },
                { "Server MOTD Description", "Shows the Message Of The Day" },
                { "Players Count Description", "Counts active players, sleepers and admins of the server" }
            }, this);
        }

        private string GetMsg(string key, object uid = null)
        {
            /* Method to get a plugin message */ 

            return lang.GetMessage(key, this, uid == null ? null : uid.ToString());
        }

        #endregion Configuration
// ----------------------------------------------------------------------------
        #region Messages System

        private void Con(string msg)
        {
            /* Broadcasts a message to the server console */

            if (BroadcastToConsole)
                Puts(SimpleColorFormat(msg, true));
        }

        private void Say(string msg, string profile = "0", bool prefix = true)
        {
            /* Broadcasts a message to chat for all players */

            // Log message to console
            Con(msg);

            // Check whether prefix is enabled
            if (!String.IsNullOrEmpty(Prefix) && EnablePluginPrefix && prefix)
                msg = Prefix + " " + msg;

            // Check whether to use a profile
            if (profile == "0" && EnableIconProfile)
                profile = IconProfile;

            rust.BroadcastChat(SimpleColorFormat("<silver>" + msg + "<end>"), null, profile);
        }

        private void Tell(BasePlayer player, string msg, string profile = "0", bool prefix = true)
        {
            /* Broadcasts a message to chat to a player */

            // Check whether prefix is enabled
            if (!String.IsNullOrEmpty(Prefix) && EnablePluginPrefix && prefix)
                msg = Prefix + " " + msg;

            // Check whether to use a profile
            if (profile == "0" && EnableIconProfile)
                profile = IconProfile;

            rust.SendChatMessage(player, SimpleColorFormat("<silver>" + msg + "<end>"), null, profile);
        }

        public string SimpleColorFormat(string text, bool removeTags = false)
        {
            /*  Simple Color Format ( v3.0 )
                Formats simple color tags to HTML */

            // All patterns
            Regex end = new Regex(@"\<(end?)\>"); // End tags
            Regex hex = new Regex(@"\<(#\w+?)\>"); // Hex codes
            Regex names = new Regex(@"\<(\w+?)\>"); // Names

            if (removeTags)
            {   
                // Remove tags
                text = end.Replace(text, "");
                text = names.Replace(text, "");
                text = hex.Replace(text, "");
            }
            else
            {   
                // Replace tags
                text = end.Replace(text, "</color>");
                text = names.Replace(text, "<color=$1>");
                text = hex.Replace(text, "<color=$1>");
            }

            return text;
        }

        #endregion Messages System
// ----------------------------------------------------------------------------
        #region Plugin Hooks

        void Init()
        {
            // Load plugin variables and messages
            LoadVariables();
            LoadMessages();

            // Players cache database
            try
            {
                Players = Interface.Oxide.DataFileSystem.ReadObject<Dictionary<string, PlayerCache>>(DatabaseFile);
            }
            catch { Players = new Dictionary<string, PlayerCache>(); }

            // Cache active players
            foreach (BasePlayer ply in BasePlayer.activePlayerList)
                OnPlayerInit(ply, false);

            // Start Adverts timer
            timer.Repeat(AdvertsInterval * 60, 0, () => SendAdvert());
            Puts("Starting Advert Messages timer, set to " + AdvertsInterval + " minute/s");

            // Enable Plugin Commands
            var command = Oxide.Core.Interface.Oxide.GetLibrary<Command>();
            Dictionary<string, object> Settings = (Dictionary<string, object>) Config.Get("Commands", "Settings");

            foreach (var cmd in Settings)
            {
                if ((bool) cmd.Value)
                {
                    // Get command triggers
                    string[] triggers = (string[]) Config.Get("Commands", "Triggers", cmd.Key);

                    // Enable triggers
                    foreach (string item in triggers)
                        command.AddChatCommand(item, this, cmd.Key.Replace(" ", string.Empty) + "_Command");
                }
            }
        }

        void Unload()
        {
            // Save Database
            Interface.Oxide.DataFileSystem.WriteObject(DatabaseFile, Players);
        }

        #endregion Plugin Hooks
// ----------------------------------------------------------------------------
        #region Player Hooks

        void OnPlayerInit(BasePlayer player, bool sendJoinMessages = true)
        {
            /* Called when the player is initializing */

            string uid = player.userID.ToString();

            // Is player cached? If not add him
            if (!(Players.ContainsKey(uid)))
                Players.Add(uid, new PlayerCache(player));
            // Otherwise update the player info
            else
                Players[uid].Update(player);

            // Check if the player country hasn't been updated yet
            if (Players[uid].country == "Unknown")
                webrequest.EnqueueGet("http://ip-api.com/json/" + Players[uid].ipaddress + "?fields=3",
                    (code, response) => WebrequestFilter(code, response, player, sendJoinMessages), this);
            else
            {
                if (sendJoinMessages)
                    JoinMessages(player);
            }
        }

        void OnPlayerDisconnected(BasePlayer player, string reason)
        {
            /* Called after the player has disconnected from the server */

            string uid = player.userID.ToString();

            // Is player cached?
            if (Players.ContainsKey(uid))
            {   
                string LeaveMessage = GetMsg("Leave Message");

                // Clear the text better
                if (reason.StartsWith("Kicked: "))
                    reason = "Kicked: " + reason.Replace(reason.Split()[0], "").Trim();

                // Send disconnected message
                if (EnableLeaveMessage && NotHide(player))
                    Say(ReplaceDic(LeaveMessage.Replace("{reason}", reason), GetNameFormats(player)));
            }
        }

        #endregion Player Hooks
// ----------------------------------------------------------------------------
        #region Entity Hooks

        void OnAirdrop(CargoPlane plane, Vector3 location)
        {
            /* Hook called when an airdrop has been called */

            // Notify Airdrop?
            if (NotifyAirdrop)
            {
                // Get drop location
                string loc = location.ToString().Replace("(", "").Replace(")", "");

                Say(GetMsg("Incoming Airdrop").Replace("{location}", loc));
            }
        }

        void OnEntitySpawned(BaseNetworkable entity)
        {
            /* Hook called after any networked entity has spawned (including trees) */

            // Notify Helicopters?
            if (NotifyHelicopter)
            {
                // Is entity and Patrol Helicopter?
                if (entity.ToString().Contains("/patrolhelicopter.prefab"))
                    Say(GetMsg("Incoming Helicopter"));
            }
        }

        #endregion Entity Hook
// ----------------------------------------------------------------------------
        #region Plugin Commands

        void PlayersList_Command(BasePlayer player, string command, string[] args)
        {
            Puts("Hello World");
        }

        [ChatCommand("notifier")]
        void Plugin_Command(BasePlayer player, string command, string[] args)
        {
            // Get arguments as one
            string arg = string.Join(" ", args);

            if (arg == "help")
            {
                Dictionary<string, object> Settings = (Dictionary<string, object>) Config.Get("Commands", "Settings");

                foreach (var cmd in Settings)
                {
                    if ((bool) cmd.Value)
                    {
                        //string triggers = string.Join("<silver>,<end> /");

                        //Tell(player, "<orange>/ <end> - <lightblue>" + GetMsg(cmd.Key + " Description") + "<end>");
                    }
                }
            else
            {
                Tell(player, "<cyan><size=18>NOTIFIER</size><end> <grey>v" + this.Version + "<end>", profile: "76561198235146288", prefix: false);
                Tell(player, this.Description, prefix: false);
                Tell(player, "Powered by <orange>Oxide 2<end> and developed by <#9810FF>SkinN<end>", profile: "76561197999302614", prefix: false);
            }
        }

        #endregion Plugin Commands
// ----------------------------------------------------------------------------
        #region Plugin Methods

        private void WebrequestFilter(int code, string response, BasePlayer player, bool sendJoinMessages)
        {
            /* Method to send a web-request to get a player country info */ 

            // Add an exception in case any connection or parsing occur meanwhile
            try
            {
                string uid = player.userID.ToString();

                // Check for any web errors
                if (!(response == null || code != 200))
                {
                    // Is Player cached?
                    if (Players.ContainsKey(uid))
                    {
                        var json = JObject.Parse(response);

                        // Save information to player cache
                        Players[uid].country = (string) json["country"];
                        Players[uid].country_code = (string) json["countryCode"];
                    }
                }
            } catch {}

            // Send joining messages
            if (sendJoinMessages)
                JoinMessages(player);
        }

        private void JoinMessages(BasePlayer player)
        {
            /* Method to send both Join and Welcome message to a player */

            // Join Message
            if (EnableJoinMessage && NotHide(player))
            {
                Say(ReplaceDic(GetMsg("Join Message"), GetNameFormats(player)));

                string sep = string.Join("\n", new string[50 + 1]);

                Tell(player, sep, prefix: false);
            }

            // Welcome Message
            if (EnableWelcomeMessage)
            {
                foreach (string line in WelcomeMessage)
                    Tell(player, ReplaceDic(line, GetNameFormats(player)), prefix: false);
            }
        }

        private bool NotHide(BasePlayer player)
        {
            /* Method to determine whether or not
               to hide an Admin, if the Hide Admins feature is on */

            return (!(HideAdmins && player.IsAdmin()));
        }

        private void SendAdvert()
        {
            /* Method to send a random advert message */

            int index = LastAdvert;

            // Is there more than one message?
            if (Adverts.Count > 0)
            {
                // Make sure next advert is not the same as the last
                while (LastAdvert == index)
                    index = UnityEngine.Random.Range(0, Adverts.Count);

                // Store index value as the last advert
                LastAdvert = index;
            }

            // Send message
            Say((string) Adverts[index]);
        }

        private Dictionary<string, object> GetNameFormats(BasePlayer player, bool userInfo = true)
        {
            /* Method to return a dictionary with all available
               name formats for:
               - Join/Leave Messages
               - Welcome Message
               - Advert Messages */

            int Active = BasePlayer.sleepingPlayerList.Count;
            int Sleepers = BasePlayer.sleepingPlayerList.Count;

            // Make player information available?
            Dictionary<string, object> Dict = new Dictionary<string, object> {
                { "{server.ip}", ConVar.Server.ip },
                { "{server.port}", ConVar.Server.port },
                { "{active}", Active },
                { "{sleepers}", Sleepers },
                { "{total}", Active + Sleepers }
            };

            // Make player information available?
            if (userInfo)
            {
                PlayerCache ply = Players[player.userID.ToString()];

                Dict.Add("{username}", ply.username);
                Dict.Add("{country}", ply.country);
                Dict.Add("{country_code}", ply.country_code);
                Dict.Add("{userip}", ply.ipaddress);
                Dict.Add("{steamid}", ply.steamid);
            }

            return Dict;
        }

        private string ReplaceDic(string source, Dictionary<string, object> dic)
        {
            /* Method to replace name formats from messages */

            foreach (var kvp in dic)
                source = source.Replace(kvp.Key, kvp.Value.ToString());

            return source;
        }

        #endregion Plugin Methods
    }
}