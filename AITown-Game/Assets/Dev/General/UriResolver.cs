using Mosaic.Feather.Runtime.DependencyLocation;

namespace General
{
    public static class UriResolver
    {
        public static string Resolve(string api)
        {
            var gameState = FeatherDL.Resolve<GameState>().Any();
            return gameState.IP + "/" + api;
        }
    }
}