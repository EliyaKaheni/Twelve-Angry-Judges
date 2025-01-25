using System.Collections.Generic;
using System.Linq;
using Cases;
using Newtonsoft.Json;

namespace General
{
    public class PreviousCasesData
    {
        [JsonProperty("cases")]
        public List<PreviousCaseDataResponse> PreviousCasesJson;

        public List<CaseData> GetPreviousCases()
        {
            return PreviousCasesJson.Select(item => item.GetCaseData()).ToList();
        }
    }
}