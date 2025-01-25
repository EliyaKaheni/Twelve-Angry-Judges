using Cases;
using Newtonsoft.Json;

namespace General
{
    public class PreviousCaseDataResponse
    {
        [JsonProperty("conversations")]
        public string Json;
        
        public CaseData GetCaseData() => JsonConvert.DeserializeObject<CaseData>(Json);
    }
}