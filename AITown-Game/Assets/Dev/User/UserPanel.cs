using Cases;
using Flow;
using General;
using Mosaic.Feather.Runtime.DependencyInjection.Abstractions.Attributes;
using Mosaic.Feather.Runtime.DependencyInjection.Attributes.Injection;
using Mosaic.Feather.Runtime.DependencyInjection.Extensions;
using Newtonsoft.Json;
using TMPro;
using UnityEngine;
using UnityEngine.UI;

namespace User
{
    public class UserPanel : MonoBehaviour
    {
        [SerializeField] private Transform previousCasesParent;
        [SerializeField] private TMP_Text userTitle;
        [SerializeField] private TMP_Text previousCaseTitle;
        [SerializeField] private TMP_Text previousCaseDescription;
        [SerializeField] private GameObject caseButtonPrefab;
        
        [SerializeField] private string previousCasesApi = "recent_cases/{0}";
        
        [Inject(BucketMode.Scene)]
        private GameState _gameState;
        
        [Inject(BucketMode.Scene)]
        private FlowManager _flowManager;
        
        private void OnEnable() => this.ProvideAndInject();
        
        public void Initialize()
        {
            ClearPreviousCases();
            SetUserTitle();
            GetPreviousCases();
        }

        private void ClearPreviousCases()
        {
            var children = previousCasesParent.GetComponentsInChildren<Button>();
            foreach (var child in children)
                Destroy(child.gameObject);
            
            previousCaseTitle.text = "";
            previousCaseDescription.text = "";
        }

        private void SetUserTitle()
        {
            userTitle.text = $"Welcome, {_gameState.UserData.Username}!";
        }
        
        private void GetPreviousCases()
        {
            var uriSuffix = string.Format(previousCasesApi, _gameState.UserData.Username);
            var uri = UriResolver.Resolve(uriSuffix);
            StartCoroutine(BackendHelper.GetRequest(uri, OnSuccess, OnError));

            return;
            
            void OnSuccess(string response)
            {
                if (response.ToLower().Contains("error"))
                    return;
                
                _gameState.PreviousCasesData = JsonConvert.DeserializeObject<PreviousCasesData>(response);
                CreatePreviousCases();
            }
        
            void OnError(string error)
            {
                Debug.Log(error);
            }
        }

        private void CreatePreviousCases()
        {
            var previousCases = _gameState.PreviousCasesData.GetPreviousCases();
            foreach (var caseData in previousCases)
            {
                var caseButton = Instantiate(caseButtonPrefab, previousCasesParent).GetComponent<CaseButton>();
                caseButton.Initialize(this, caseData);
            }
        }

        public void CreateCase()
        {
            _flowManager.SetupCase();
        }

        public void ShowCase(CaseData caseData)
        {
            previousCaseTitle.text = caseData.CaseName;
            var description = "";

            description += $"Convict Name: {caseData.ConvictName}\n\n";
            description += $"Story: {caseData.Story}\n\n";
            description += $"Verdict: {caseData.Verdict}\n\n";
            description += $"\nQuestions:\n\n\n";

            for (var i = 0; i < caseData.Questions.Count; i++)
            {
                description += $"Question {i + 1}: {caseData.Questions[i].Question}\n\n";
                description += $"Answer {i + 1}: {caseData.Questions[i].Answer}\n\n\n";
            }
            
            previousCaseDescription.text = description;
        }
    }
}
