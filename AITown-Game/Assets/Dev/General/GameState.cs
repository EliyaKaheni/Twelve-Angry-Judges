using System.Collections.Generic;
using Cases;
using Flow;
using Mosaic.Feather.Runtime.Abstractions.Dependency;
using Mosaic.Feather.Runtime.DependencyInjection.Abstractions.Attributes;
using Mosaic.Feather.Runtime.DependencyInjection.Attributes.Injection;
using Mosaic.Feather.Runtime.DependencyInjection.Attributes.Provision;
using UnityEngine;
using TMPro;
using User;

namespace General
{
    public class GameState : MonoBehaviour, IDependency
    {
        public string IPPrefix = "http://";
        
        [SerializeField] private TMP_InputField ipField;
        public string IP => IPPrefix + ipField.text;
        public int QuestionCount;
        public UserData UserData;
        public CaseData CaseData;
        public PreviousCasesData PreviousCasesData;

        [Provide(BucketMode.Scene)]
        private GameState Provide() => this;

        [Inject(BucketMode.Scene)]
        private FlowManager _flow;

        public void AcceptUser(UserData userData)
        {
            UserData = userData;
            _flow.SetupUser();
        }

        public void AcceptCase(CaseData caseData)
        {
            CaseData = caseData;
            _flow.SetupQuestion();
        }

        public void AcceptQuestion(QuestionData questionData)
        {
            CaseData.Questions ??= new List<QuestionData>();
            CaseData.Questions.Add(questionData);
            
            if(CaseData.Questions.Count >= QuestionCount)
                _flow.SetupVerdict();
            else
                _flow.SetupQuestion();
        }
    }
}