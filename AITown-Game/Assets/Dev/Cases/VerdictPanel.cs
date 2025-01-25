using Flow;
using General;
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
    public class VerdictPanel : MonoBehaviour
    {
        [SerializeField] private TMP_Text verdictText;
        [SerializeField] private Button acceptButton;
        [SerializeField] private StatusText statusText;

        [SerializeField] private string createCaseApi = "create_case";
        [SerializeField] private string finalVerdictApi = "final_verdict";
        
        [Inject(BucketMode.Scene)]
        private GameState _gameState;
        
        [Inject(BucketMode.Scene)]
        private FlowManager _flowManager;
        
        private void OnEnable() => this.ProvideAndInject();
        
        public void Initialize()
        {
            verdictText.text = string.Empty;
            statusText.Clear();
            acceptButton.interactable = false;
            GetVerdict();
        }

        private void GetVerdict()
        {
            var uri = UriResolver.Resolve(finalVerdictApi);
            var request = new CaseDataRequest() { CaseData = _gameState.CaseData };
            var json = JsonConvert.SerializeObject(request);
            StartCoroutine(BackendHelper.PostRequest(uri, json, OnSuccess, OnError));
            
            return;
            
            void OnSuccess(string response)
            {
                acceptButton.interactable = true;
                var data = JsonConvert.DeserializeObject<FinalVerdictData>(response);
                verdictText.text = data.Verdict;
                _gameState.CaseData.Verdict = data.Verdict;
                Debug.Log(response);
            }

            void OnError(string error)
            {
                acceptButton.interactable = true;
                Debug.LogError(error);
            }
        }

        public void AcceptVerdict()
        {
            acceptButton.interactable = false;
            SaveCase();
        }

        private void SaveCase()
        {
            var uri = UriResolver.Resolve(createCaseApi);
            var data = JsonConvert.SerializeObject(_gameState.CaseData);
            var request = new CaseDataUsernameRequest { Username = _gameState.UserData.Username, CaseData = data};
            var json = JsonConvert.SerializeObject(request);
            StartCoroutine(BackendHelper.PostRequest(uri, json, OnSuccess, OnError));

            return;

            void OnSuccess(string response)
            {
                Debug.Log(response);
                statusText.ShowSuccess(response);
                acceptButton.interactable = true;
                _flowManager.SetupUser();
                _gameState.CaseData = null;
            }

            void OnError(string error)
            {
                Debug.Log(error);
                statusText.ShowError(error);
                acceptButton.interactable = true;
            }
        }
    }
}
