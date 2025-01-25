using System.Collections.Generic;
using Flow;
using General;
using Judges;
using Login;
using Mosaic.Feather.Runtime.DependencyInjection.Abstractions.Attributes;
using Mosaic.Feather.Runtime.DependencyInjection.Attributes.Injection;
using Mosaic.Feather.Runtime.DependencyInjection.Extensions;
using Newtonsoft.Json;
using TMPro;
using UnityEngine;
using UnityEngine.UI;

namespace Cases
{
    public class QuestionPanel : MonoBehaviour
    {
        [SerializeField] private TMP_Text questionText;
        [SerializeField] private TMP_InputField answerText;
        [SerializeField] private Button submitButton;
        [SerializeField] private StatusText statusText;

        [SerializeField] private JudgeAppearanceContainer judgeAppearanceContainer;
        [SerializeField] private TMP_Text judgeText;
        [SerializeField] private TMP_Text judgeTraits;
        [SerializeField] private Image judgeImage;

        [SerializeField] private string questionApi = "generate_judge_question";
        [SerializeField] private string processAnswerApi = "process_answer";
        [SerializeField] private string defenseApi = "submit_defence";

        private JudgeAppearance _judge;
        
        [Inject(BucketMode.Scene)]
        private GameState _gameState;
        
        [Inject(BucketMode.Scene)]
        private FlowManager _flowManager;
        
        private void OnEnable() => this.ProvideAndInject();
        
        public void Initialize()
        {
            questionText.text = string.Empty;
            answerText.text = string.Empty;
            submitButton.interactable = false;
            statusText.Clear();

            SetupJudge();
            GetQuestionText();
        }

        private void SetupJudge()
        {
            judgeAppearanceContainer.FillNamesAndTraits();
            _judge = judgeAppearanceContainer.GetRandomAppearance();
            judgeImage.sprite = _judge.Avatar;
            judgeText.text = $"Judge {_judge.Name} is asking...";
            judgeTraits.text = _judge.Traits;
        }

        private void GetQuestionText()
        {
            if (_gameState.CaseData.Questions == null || _gameState.CaseData.Questions.Count == 0)
            {
                questionText.text = "What do you have to say for yourself?";
                submitButton.interactable = true;
                return;
            }
            
            var uri = UriResolver.Resolve(questionApi);
            var request = new JudgeQuestionRequest() { CaseData = _gameState.CaseData, JudgeTraits = _judge.Traits };
            var json = JsonConvert.SerializeObject(request);
            StartCoroutine(BackendHelper.PostRequest(uri, json, OnSuccess, OnError));
            
            return;
            
            void OnSuccess(string response)
            {
                submitButton.interactable = true;
                var data = JsonConvert.DeserializeObject<QuestionData>(response);
                questionText.text = data.Question;
                Debug.Log(response);
            }

            void OnError(string error)
            {
                submitButton.interactable = false;
                Debug.LogError(error);
            }
        }

        public void Submit()
        {
            submitButton.interactable = false;

            var isDefense = _gameState.CaseData.Questions == null || _gameState.CaseData.Questions.Count == 0;
            
            var question = new QuestionData() { Question = questionText.text, Answer = answerText.text };
            
            var uri = isDefense ? UriResolver.Resolve(defenseApi) : UriResolver.Resolve(processAnswerApi);
            var request = new JudgeAnswerRequest() { CaseData = _gameState.CaseData, QuestionData = question, JudgeTraits = _judge.Traits};
            var json = JsonConvert.SerializeObject(request);
            StartCoroutine(BackendHelper.PostRequest(uri, json, OnSuccess, OnError));

            return;

            void OnSuccess(string response)
            {
                submitButton.interactable = true;
                Debug.Log(response);
                var credibility = JsonConvert.DeserializeObject<CredibilityData>(response);
                _gameState.CaseData.Trust = credibility.Credibility;
                statusText.ShowSuccess(response);
                _gameState.AcceptQuestion(question);
            }
            
            void OnError(string error)
            {
                submitButton.interactable = true;
                Debug.Log(error);
                statusText.ShowError(error);
            }
        }
    }
}
