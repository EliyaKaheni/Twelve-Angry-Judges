using Newtonsoft.Json;

namespace Cases
{
    public class QuestionData
    {
        [JsonProperty("question")]
        public string Question;
        [JsonProperty("answer")]
        public string Answer;
    }
}