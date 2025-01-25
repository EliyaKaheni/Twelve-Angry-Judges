using General;
using Mosaic.Feather.Runtime.DependencyInjection.Abstractions.Attributes;
using Mosaic.Feather.Runtime.DependencyInjection.Attributes.Injection;
using Mosaic.Feather.Runtime.DependencyInjection.Extensions;
using TMPro;
using UnityEngine;

namespace Cases
{
    public class CasePanel : MonoBehaviour
    {
        [SerializeField] private TMP_InputField caseNameText;
        [SerializeField] private TMP_InputField convictNameText;
        [SerializeField] private TMP_InputField caseStoryText;
        
        [Inject(BucketMode.Scene)]
        private GameState _gameState;
        
        private void OnEnable() => this.ProvideAndInject();

        public void Initialize()
        {
            caseNameText.text = string.Empty;
            convictNameText.text = string.Empty;
            caseStoryText.text = string.Empty;
        }

        public void CreateCase()
        {
            var caseData = new CaseData
            {
                CaseName = caseNameText.text,
                ConvictName = convictNameText.text,
                Story = caseStoryText.text,
            };
            
            _gameState.AcceptCase(caseData);
        }
    }
}