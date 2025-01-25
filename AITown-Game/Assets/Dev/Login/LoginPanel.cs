using System;
using General;
using Mosaic.Feather.Runtime.DependencyInjection.Abstractions.Attributes;
using Mosaic.Feather.Runtime.DependencyInjection.Attributes.Injection;
using Mosaic.Feather.Runtime.DependencyInjection.Extensions;
using Newtonsoft.Json;
using TMPro;
using UnityEngine;
using User;

namespace Login
{
    public class LoginPanel : MonoBehaviour
    {
        [SerializeField] private StatusText statusText;
        [SerializeField] private TMP_InputField usernameField;
        [SerializeField] private TMP_InputField passwordField;

        [SerializeField] private string signInApi = "signin";
        [SerializeField] private string signUpApi = "signup";

        private string SignUpUri => UriResolver.Resolve(signUpApi);
        private string SignInUri => UriResolver.Resolve(signInApi);
        
        [Inject(BucketMode.Scene)]
        private GameState _gameState;

        private void OnEnable() => this.ProvideAndInject();

        public void Initialize()
        {
            usernameField.text = string.Empty;
            passwordField.text = string.Empty;
            statusText.Clear();
        }
        
        public void SignUp()
        {
            var userData = new UserData { Username = usernameField.text, Password = passwordField.text };
            var json = JsonConvert.SerializeObject(userData);
            StartCoroutine(BackendHelper.PostRequest(SignUpUri, json, OnSuccess, OnError));

            return;
            
            void OnSuccess(string response)
            {
                statusText.ShowSuccess(response);
            }

            void OnError(string error)
            {
                statusText.ShowError(error);
            }
        }
        
        public void SignIn()
        {
            var userData = new UserData { Username = usernameField.text, Password = passwordField.text };
            var json = JsonConvert.SerializeObject(userData);
            StartCoroutine(BackendHelper.PostRequest(SignInUri, json, OnSuccess, OnError));
            
            return;
            
            void OnSuccess(string response)
            {
                statusText.ShowSuccess(response);
                _gameState.AcceptUser(userData);
            }

            void OnError(string error)
            {
                statusText.ShowError(error);
            }
        }

        private void CreateUserData()
        {
            var userData = new UserData();
        }
    }
}