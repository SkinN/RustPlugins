namespace Oxide.Plugins
{
    [Info("Anti-Wounded", "SkinN", 2.0, ResourceId = 1045)]
    [Description("Skips the wounded state before death")]
    class AntiWounded : RustPlugin
    {
        bool CanBeWounded(BasePlayer player, HitInfo info) { return false; }
    }
}