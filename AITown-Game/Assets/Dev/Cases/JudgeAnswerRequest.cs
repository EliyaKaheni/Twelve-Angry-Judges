using Newtonsoft.Json;

namespace Cases
{
    public class JudgeAnswerRequest : JudgeRequest
    {
        [JsonProperty("question_data")]
        public QuestionData QuestionData;
    }
}