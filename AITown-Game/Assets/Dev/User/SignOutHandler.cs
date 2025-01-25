using Flow;
using Mosaic.Feather.Runtime.DependencyInjection.Abstractions.Attributes;
using Mosaic.Feather.Runtime.DependencyInjection.Attributes.Injection;
using Mosaic.Feather.Runtime.DependencyInjection.Extensions;
using UnityEngine;

namespace User
{
    public class SignOutHandler : MonoBehaviour
    {
        [Inject(BucketMode.Scene)]
        private FlowManager _flowManager;

        private void OnEnable() => this.ProvideAndInject();

        public void SignOut()
        {
            _flowManager.SetupLogin();
        }
    }
}
