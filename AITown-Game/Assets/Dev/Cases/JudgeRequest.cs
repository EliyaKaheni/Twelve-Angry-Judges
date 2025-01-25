using Newtonsoft.Json;

namespace Cases
{
    public class JudgeRequest : CaseDataRequest
    {
        [JsonProperty("judge_traits")]
        public string JudgeTraits;
    }
}