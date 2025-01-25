using System.Collections.Generic;
using Newtonsoft.Json;

namespace Cases
{
    public class CaseData
    {
        [JsonProperty("case_name")]
        public string CaseName = string.Empty;
        [JsonProperty("convict_name")]
        public string ConvictName = string.Empty;
        [JsonProperty("story")]
        public string Story = string.Empty;
        [JsonProperty("questions")]
        public List<QuestionData> Questions = new();
        [JsonProperty("verdict")]
        public string Verdict = string.Empty;
        [JsonProperty("trust")]
        public float Trust;
    }
}
