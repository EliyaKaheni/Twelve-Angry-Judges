using TMPro;
using UnityEngine;

namespace Login
{
    public class StatusText : MonoBehaviour
    {
        [SerializeField] private TMP_Text statusText;

        public void Clear()
        {
            statusText.text = "";
        }
        
        public void ShowError(string text)
        {
            statusText.text = text;
            statusText.color = Color.red;
        }

        public void ShowSuccess(string text)
        {
            statusText.text = text;
            statusText.color = Color.green;
        }
    }
}
