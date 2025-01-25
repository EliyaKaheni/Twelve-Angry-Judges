using Newtonsoft.Json;

namespace Cases
{
    public class CaseDataUsernameRequest 
    {
        [JsonProperty("username")]
        public string Username;

        [JsonProperty("case_data")]
        public string CaseData;
    }
}