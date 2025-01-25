using Newtonsoft.Json;

namespace User
{
    public class UserData
    {
        [JsonProperty("username")]
        public string Username;
        
        [JsonProperty("password")]
        public string Password;
    }
}
