using System.Net;
using System.Net.Security;
using System.Security.Cryptography.X509Certificates;
using UnityEngine;

namespace General
{
    public class SSLBypass : MonoBehaviour
    {
        private void Awake()
        {
            ServicePointManager.ServerCertificateValidationCallback = CertificateValidationCallback;
        }

        private bool CertificateValidationCallback(object sender, X509Certificate certificate, X509Chain chain, SslPolicyErrors sslPolicyErrors)
        {
            return true;
        }
    }
}