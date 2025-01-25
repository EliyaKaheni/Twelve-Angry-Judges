using Cases;
using Login;
using Mosaic.Feather.Runtime.Abstractions.Dependency;
using Mosaic.Feather.Runtime.DependencyInjection.Abstractions.Attributes;
using Mosaic.Feather.Runtime.DependencyInjection.Attributes.Provision;
using Newtonsoft.Json;
using UnityEngine;
using User;

namespace Flow
{
    public class FlowManager : MonoBehaviour, IDependency
    {
        [SerializeField] private GameObject intro;
        [SerializeField] private LoginPanel login;
        [SerializeField] private UserPanel user;
        [SerializeField] private CasePanel createCase;
        [SerializeField] private GameObject trust;
        [SerializeField] private QuestionPanel question;
        [SerializeField] private VerdictPanel verdict;
        
        [Provide(BucketMode.Scene)]
        private FlowManager Provide() => this;

        private void Awake()
        {
            TurnAllOff();
        }
        
        private void Start()
        {
            SetupIntro();
        }

        public void SetupIntro()
        {
            TurnAllOff();
            intro.gameObject.SetActive(true);
        }

        public void SetupLogin()
        {
            TurnAllOff();
            login.gameObject.SetActive(true);
            login.Initialize();
        }

        public void SetupUser()
        {
            TurnAllOff();
            user.gameObject.SetActive(true);
            user.Initialize();
        }

        public void SetupCase()
        {
            TurnAllOff();
            createCase.gameObject.SetActive(true);
            createCase.Initialize();
        }

        public void SetupQuestion()
        {
            TurnAllOff();
            question.gameObject.SetActive(true);
            trust.gameObject.SetActive(true);
            question.Initialize();
        }

        public void SetupVerdict()
        {
            TurnAllOff();
            trust.gameObject.SetActive(true);
            verdict.gameObject.SetActive(true);
            verdict.Initialize();
        }

        private void TurnAllOff()
        {
            intro.gameObject.SetActive(false);
            login.gameObject.SetActive(false);
            user.gameObject.SetActive(false);
            createCase.gameObject.SetActive(false);
            question.gameObject.SetActive(false);
            trust.gameObject.SetActive(false);
            verdict.gameObject.SetActive(false);
        }
    }
}
