using System;
using System.Collections;
using UnityEngine.Networking;

namespace General
{
    public static class BackendHelper
    {
        public static IEnumerator GetRequest(string uri, Action<string> onSuccess, Action<string> onError = null)
        {
            using var webRequest = UnityWebRequest.Get(uri);
            yield return webRequest.SendWebRequest();

            if (webRequest.result is UnityWebRequest.Result.ConnectionError or UnityWebRequest.Result.ProtocolError)
                onError?.Invoke($"{webRequest.error}");
            else
                onSuccess?.Invoke($"{webRequest.downloadHandler.text}");
        }
        
        public static IEnumerator PostRequest(string uri, string jsonData, Action<string> onSuccess, Action<string> onError = null)
        {
            using var webRequest = UnityWebRequest.PostWwwForm(uri, "");
            var jsonToSend = new System.Text.UTF8Encoding().GetBytes(jsonData);
            webRequest.uploadHandler = new UploadHandlerRaw(jsonToSend);
            webRequest.downloadHandler = new DownloadHandlerBuffer();
            webRequest.SetRequestHeader("Content-Type", "application/json");
            
            yield return webRequest.SendWebRequest();

            if (webRequest.result is UnityWebRequest.Result.ConnectionError or UnityWebRequest.Result.ProtocolError)
                onError?.Invoke($"{webRequest.error}");
            else
                onSuccess?.Invoke($"{webRequest.downloadHandler.text}");
        }
    }
}
