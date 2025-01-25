using Mosaic.Feather.Runtime.DependencyInjection.Abstractions.Attributes;
using Mosaic.Feather.Runtime.DependencyInjection.Attributes.Injection;
using Mosaic.Feather.Runtime.DependencyInjection.Extensions;
using UnityEngine;
using UnityEngine.UI;

namespace General
{
    public class TrustSliderUpdater : MonoBehaviour
    {
        [SerializeField] private Slider slider;
        
        [Inject(BucketMode.Scene)]
        private GameState _gameState;

        private void OnEnable()
        {
            this.ProvideAndInject();
        }

        private void Update()
        {
            if (!_gameState || _gameState.CaseData == null)
                return;

            slider.value = _gameState.CaseData.Trust;
        }
    }
}
