using Newtonsoft.Json;

namespace Cases
{
    public class FinalVerdictData
    {
        [JsonProperty("final_verdict")]
        public string Verdict;
    }
}