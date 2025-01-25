using Newtonsoft.Json;

namespace Cases
{
    public class CaseDataRequest
    {
        [JsonProperty("case_data")]
        public CaseData CaseData;
    }
}